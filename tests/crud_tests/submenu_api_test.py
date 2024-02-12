from fastapi import BackgroundTasks
from httpx import AsyncClient

from repository.submenu import SubmenuRepository
from serializers.menu import GetMenuSerializer
from serializers.submenu import GetSubmenuSerializer
from services.menu import MenuServices
from services.submenu import SubmenuServices
from tests.data.menu import create_menu
from tests.data.submenu import (
    create_incorrect_submenu,
    create_submenu,
    incorrect_id,
    update_submenu,
)
from utils.urls_utils import reverse_url

submenu_services = SubmenuServices(background_tasks=BackgroundTasks())
menu_services = MenuServices(background_tasks=BackgroundTasks())


# Добавление меню для теста подменю
async def test_add_menu(async_client: AsyncClient):
    response = await async_client.post(reverse_url('post_menu'), json=create_menu)
    json = response.json()
    create_menu['id'] = json.get('id')
    menu: GetMenuSerializer = GetMenuSerializer.model_validate(await menu_services.find_by_id(create_menu['id']))
    obj_from_response = GetMenuSerializer(**json)
    assert obj_from_response == menu


async def test_get_submenus_empty_list(async_client: AsyncClient):
    response = await async_client.get(reverse_url('get_submenus', target_menu_id=create_menu['id']))
    submenu = [GetSubmenuSerializer.model_validate(item) for item in await submenu_services.find_all(create_menu['id'])]
    json = response.json()
    assert response.status_code == 200
    assert json == submenu


async def test_add_submenu(async_client: AsyncClient):
    response = await async_client.post(reverse_url('post_submenu', target_menu_id=create_menu['id']),
                                       json=create_submenu)
    create_submenu['id'] = response.json().get('id')
    json = response.json()
    submenu: GetSubmenuSerializer = GetSubmenuSerializer.model_validate(
        await submenu_services.find_by_id(create_menu['id'], create_submenu['id']))
    obj_from_response = GetSubmenuSerializer(**json)
    assert obj_from_response == submenu
    assert response.status_code == 201


async def test_add_incorrect_submenu(async_client: AsyncClient):
    response = await async_client.post(reverse_url('post_submenu', target_menu_id=create_menu['id']),
                                       json=create_incorrect_submenu)
    assert response.status_code == 422


async def test_add_submenu_to_incorrect_menu(async_client: AsyncClient):
    response = await async_client.post(reverse_url('post_submenu', target_menu_id=incorrect_id), json=create_submenu)
    assert response.status_code == 404


async def test_get_submenus_list(async_client: AsyncClient):
    response = await async_client.get(reverse_url('get_submenus', target_menu_id=create_menu['id']))
    submenu = [GetSubmenuSerializer.model_validate(item) for item in await submenu_services.find_all(create_menu['id'])]
    json = response.json()
    obj_from_response = [GetSubmenuSerializer(**item) for item in json]
    assert response.status_code == 200
    assert obj_from_response == submenu


async def test_get_submenu_by_id(async_client: AsyncClient):
    response = await async_client.get(
        reverse_url('get_submenu', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id']))
    submenu: GetSubmenuSerializer = GetSubmenuSerializer.model_validate(
        await submenu_services.find_by_id(create_menu['id'], create_submenu['id']))
    json = response.json()
    obj_from_response = GetSubmenuSerializer(**json)
    assert obj_from_response == submenu
    assert response.status_code == 200


async def test_get_submenu_by_incorrect_id(async_client: AsyncClient):
    response = await async_client.get(
        reverse_url('get_submenu', target_menu_id=create_menu['id'], target_submenu_id=incorrect_id))
    assert response.status_code == 404


async def test_update_submenu(async_client: AsyncClient):
    response = await async_client.patch(
        reverse_url('patch_submenu', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id']),
        json=update_submenu)

    json = response.json()
    submenu: GetSubmenuSerializer = GetSubmenuSerializer.model_validate(
        await submenu_services.find_by_id(create_menu['id'], create_submenu['id']))
    obj_from_response = GetSubmenuSerializer(**json)
    assert obj_from_response == submenu
    assert response.status_code == 200


async def test_update_incorrect_submenu(async_client: AsyncClient):
    response = await async_client.patch(
        reverse_url('patch_submenu', target_menu_id=create_menu['id'], target_submenu_id=incorrect_id),
        json=update_submenu)
    assert response.status_code == 404


async def test_delete_submenu(async_client: AsyncClient):
    response = await async_client.delete(
        reverse_url('delete_submenu', target_menu_id=create_menu['id'], target_submenu_id=create_submenu['id']))
    submenu = await SubmenuRepository.check_object_exists(create_menu['id'], create_submenu['id'])
    assert response.status_code == 200
    assert submenu is False


async def test_delete_incorrect_submenu(async_client: AsyncClient):
    response = await async_client.delete(
        reverse_url('delete_submenu', target_menu_id=create_menu['id'], target_submenu_id=incorrect_id))
    assert response.status_code == 404


async def test_delete_menu(async_client: AsyncClient):
    response = await async_client.delete(reverse_url('delete_menu', target_menu_id=create_menu['id']))
    assert response.status_code == 200
