from httpx import AsyncClient

from repository.dish import DishRepository
from serializers.dish import GetDishSerializer
from serializers.menu import GetMenuSerializer
from serializers.submenu import GetSubmenuSerializer
from services.dish import DishServices
from services.menu import MenuServices
from services.submenu import SubmenuServices
from tests.data.dish import create_dish1, incorrect_dish, incorrect_id, update_dish1
from tests.data.menu import create_menu
from tests.data.submenu import create_submenu
from utils.urls_utils import reverse_url


# Добавление меню и подменю для теста блюд
async def test_add_menu(async_client: AsyncClient, session):
    response = await async_client.post(reverse_url('post_menu'), json=create_menu)
    json = response.json()
    create_menu['id'] = json.get('id')
    menu: GetMenuSerializer = GetMenuSerializer.model_validate(await MenuServices.find_by_id(create_menu['id']))
    obj_from_response = GetMenuSerializer(**json)
    assert obj_from_response == menu
    assert response.status_code == 201


async def test_add_submenu(async_client: AsyncClient):
    response = await async_client.post(reverse_url('post_submenu', target_menu_id=create_menu['id']),
                                       json=create_submenu)
    create_submenu['id'] = response.json().get('id')
    json = response.json()
    submenu: GetSubmenuSerializer = GetSubmenuSerializer.model_validate(
        await SubmenuServices.find_by_id(create_menu['id'], create_submenu['id']))
    obj_from_response = GetSubmenuSerializer(**json)
    assert obj_from_response == submenu
    assert response.status_code == 201


async def test_get_dish_empty_list(async_client: AsyncClient):
    response = await async_client.get(
        reverse_url('get_dishes', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id']))
    dish = [GetDishSerializer.model_validate(item) for item in
            await DishServices.get_dish(create_menu['id'], create_submenu['id'])]
    json = response.json()
    assert response.status_code == 200
    assert json == dish


async def test_add_dish(async_client: AsyncClient):
    response = await async_client.post(
        reverse_url('post_dish', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id']),
        json=create_dish1)
    create_dish1['id'] = response.json().get('id')
    json = response.json()
    dish: GetDishSerializer = GetDishSerializer.model_validate(
        await DishServices.get_dish_by_id(create_menu['id'], create_submenu['id'], create_dish1['id']))
    obj_from_response = GetDishSerializer(**json)
    assert obj_from_response == dish


async def test_add_incorrect_dish(async_client: AsyncClient):
    response = await async_client.post(
        reverse_url('post_dish', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id']),
        json=incorrect_dish)
    assert response.status_code == 422


async def test_add_dish_to_incorrect_menu(async_client: AsyncClient):
    response = await async_client.post(
        reverse_url('post_dish', target_menu_id=incorrect_id, target_submenu_id=create_submenu['id']),
        json=create_dish1)
    assert response.status_code == 404


async def test_add_dish_to_incorrect_submenu(async_client: AsyncClient):
    response = await async_client.post(
        reverse_url('post_dish', target_menu_id=create_menu['id'], target_submenu_id=incorrect_id),
        json=create_dish1)
    assert response.status_code == 404


async def test_add_dish_to_all_incorrect(async_client: AsyncClient):
    response = await async_client.post(
        reverse_url('post_dish', target_menu_id=incorrect_id, target_submenu_id=incorrect_id),
        json=create_dish1)
    assert response.status_code == 404


async def test_get_dish_list(async_client: AsyncClient):
    response = await async_client.get(
        reverse_url('get_dishes', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id']))
    dish = [GetDishSerializer.model_validate(item) for item in
            await DishServices.get_dish(create_menu['id'], create_submenu['id'])]
    json = response.json()
    obj_from_response = [GetDishSerializer(**item) for item in json]
    assert response.status_code == 200
    assert obj_from_response == dish


async def test_get_dish_by_id(async_client: AsyncClient):
    response = await async_client.get(
        reverse_url('get_dish', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id'],
                    target_dish_id=create_dish1['id']))
    dish: GetDishSerializer = GetDishSerializer.model_validate(
        await DishServices.get_dish_by_id(create_menu['id'], create_submenu['id'], create_dish1['id']))
    json = response.json()
    obj_from_response = GetDishSerializer(**json)
    assert obj_from_response == dish
    assert response.status_code == 200


async def test_get_dish_by_incorrect_id(async_client: AsyncClient):
    response = await async_client.get(
        reverse_url('get_dish', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id'],
                    target_dish_id=incorrect_id))
    assert response.status_code == 404


async def test_update_dish(async_client: AsyncClient):
    response = await async_client.patch(
        reverse_url('patch_dish', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id'],
                    target_dish_id=create_dish1['id']),
        json=update_dish1)
    json = response.json()
    dish: GetDishSerializer = GetDishSerializer.model_validate(
        await DishServices.get_dish_by_id(create_menu['id'], create_submenu['id'], create_dish1['id']))
    obj_from_response = GetDishSerializer(**json)
    assert obj_from_response == dish
    assert response.status_code == 200


async def test_update_incorrect_dish(async_client: AsyncClient):
    response = await async_client.patch(
        reverse_url('patch_dish', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id'],
                    target_dish_id=incorrect_id),
        json=update_dish1)
    assert response.status_code == 404


async def test_delete_dish(async_client: AsyncClient):
    response = await async_client.delete(
        reverse_url('delete_dish', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id'],
                    target_dish_id=create_dish1['id']))
    dish = await DishRepository.check_object_exists(create_submenu['id'], create_dish1['id'])
    assert response.status_code == 200
    assert dish is False


async def test_delete_incorrect_dish(async_client: AsyncClient):
    response = await async_client.delete(
        reverse_url('delete_dish', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id'],
                    target_dish_id=incorrect_id))
    assert response.status_code == 404


async def test_delete_menu(async_client: AsyncClient):
    response = await async_client.delete(reverse_url('delete_menu', target_menu_id=create_menu['id']))
    assert response.status_code == 200
