from httpx import AsyncClient

from serializers.menu import GetMenuSerializer
from serializers.submenu import GetSubmenuSerializer
from services.menu import MenuServices
from services.submenu import SubmenuServices
from tests.conftest import base_url
from tests.data.menu import create_menu
from tests.data.submenu import create_submenu, update_submenu, create_incorrect_submenu, incorrect_id


# Добавление меню для теста подменю
async def test_add_menu(async_client: AsyncClient):
    response = await async_client.post(base_url, json=create_menu)
    json = response.json()
    create_menu['id'] = json.get('id')
    menu: GetMenuSerializer = GetMenuSerializer.model_validate(await MenuServices.find_by_id(create_menu["id"]))
    obj_from_response = GetMenuSerializer(**json)
    assert obj_from_response == menu


async def test_get_submenus_empty_list(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu['id']}/submenus")
    submenu = [GetSubmenuSerializer.model_validate(item) for item in await SubmenuServices.find_all(create_menu['id'])]
    json = response.json()
    assert response.status_code == 200
    assert json == submenu


async def test_add_submenu(async_client: AsyncClient):
    response = await async_client.post(f"{base_url}/{create_menu['id']}/submenus", json=create_submenu)
    create_submenu['id'] = response.json().get('id')
    json = response.json()
    submenu: GetSubmenuSerializer = GetSubmenuSerializer.model_validate(
        await SubmenuServices.find_by_id(create_menu['id'], create_submenu['id']))
    obj_from_response = GetSubmenuSerializer(**json)
    assert obj_from_response == submenu
    assert response.status_code == 201


async def test_add_incorrect_submenu(async_client: AsyncClient):
    response = await async_client.post(f"{base_url}/{create_menu['id']}/submenus", json=create_incorrect_submenu)
    assert response.status_code == 422


async def test_add_submenu_to_incorrect_menu(async_client: AsyncClient):
    response = await async_client.post(f"{base_url}/{incorrect_id}/submenus", json=create_submenu)
    assert response.status_code == 404


async def test_get_submenus_list(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu['id']}/submenus")
    submenu = [GetSubmenuSerializer.model_validate(item) for item in await SubmenuServices.find_all(create_menu['id'])]
    json = response.json()
    obj_from_response = [GetSubmenuSerializer(**item) for item in json]
    assert response.status_code == 200
    assert obj_from_response == submenu


async def test_get_submenu_by_id(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu['id']}/submenus/{create_submenu['id']}")
    submenu: GetSubmenuSerializer = GetSubmenuSerializer.model_validate(
        await SubmenuServices.find_by_id(create_menu["id"], create_submenu['id']))
    json = response.json()
    obj_from_response = GetSubmenuSerializer(**json)
    assert obj_from_response == submenu
    assert response.status_code == 200


async def test_get_submenu_by_incorrect_id(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{incorrect_id}/submenus/{incorrect_id}")
    assert response.status_code == 404


async def test_update_submenu(async_client: AsyncClient):
    response = await async_client.patch(f"{base_url}/{create_menu['id']}/submenus/{create_submenu['id']}",
                                        json=update_submenu)

    json = response.json()
    submenu: GetSubmenuSerializer = GetSubmenuSerializer.model_validate(
        await SubmenuServices.find_by_id(create_menu["id"], create_submenu['id']))
    obj_from_response = GetSubmenuSerializer(**json)
    assert obj_from_response == submenu
    assert response.status_code == 200


async def test_update_incorrect_submenu(async_client: AsyncClient):
    response = await async_client.patch(f"{base_url}/{create_menu['id']}/submenus/{incorrect_id}",
                                        json=update_submenu)
    assert response.status_code == 404


async def test_delete_submenu(async_client: AsyncClient):
    response = await async_client.delete(f"{base_url}/{create_menu['id']}/submenus/{create_submenu['id']}")
    submenu = await SubmenuServices.check_object_exists(create_menu['id'], create_submenu['id'])
    assert response.status_code == 200
    assert submenu is False


async def test_delete_incorrect_submenu(async_client: AsyncClient):
    response = await async_client.delete(f"{base_url}/{create_menu['id']}/submenus/{incorrect_id}")
    assert response.status_code == 404


async def test_delete_menu(async_client: AsyncClient):
    response = await async_client.delete(f"{base_url}/{create_menu.get('id')}")
    assert response.status_code == 200
