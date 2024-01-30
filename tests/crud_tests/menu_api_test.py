from httpx import AsyncClient
from serializers.menu import GetMenuSerializer
from services.menu import MenuServices
from tests.conftest import base_url
from tests.data.menu import create_menu, update_menu, create_incorrect_menu, incorrect_id


async def test_get_menu_empty_list(async_client: AsyncClient):
    response = await async_client.get(base_url)
    menu = [GetMenuSerializer.model_validate(item) for item in await MenuServices.find_all()]
    json = response.json()
    assert response.status_code == 200
    assert json == menu


async def test_add_menu(async_client: AsyncClient, session):
    response = await async_client.post(base_url, json=create_menu)
    json = response.json()
    create_menu['id'] = json.get('id')
    menu: GetMenuSerializer = GetMenuSerializer.model_validate(await MenuServices.find_by_id(create_menu["id"]))
    obj_from_response = GetMenuSerializer(**json)
    assert obj_from_response == menu
    assert response.status_code == 201


async def test_add_incorrect_menu(async_client: AsyncClient):
    response = await async_client.post(base_url, json=create_incorrect_menu)
    assert response.status_code == 422


async def test_get_menu_list(async_client: AsyncClient):
    response = await async_client.get(base_url)
    menu = [GetMenuSerializer.model_validate(item) for item in await MenuServices.find_all()]
    json = response.json()
    obj_from_response = [GetMenuSerializer(**item) for item in json]
    assert response.status_code == 200
    assert obj_from_response == menu


async def test_get_menu_by_incorrect_id(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{incorrect_id}")
    assert response.status_code == 404


async def test_get_menu_by_id(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu['id']}")
    assert response.status_code == 200

    menu: GetMenuSerializer = GetMenuSerializer.model_validate(await MenuServices.find_by_id(create_menu["id"]))
    json = response.json()
    obj_from_response = GetMenuSerializer(**json)
    assert obj_from_response == menu


async def test_update_menu(async_client: AsyncClient):
    response = await async_client.patch(f"{base_url}/{create_menu['id']}", json=update_menu)
    json = response.json()
    menu: GetMenuSerializer = GetMenuSerializer.model_validate(await MenuServices.find_by_id(create_menu["id"]))
    obj_from_response = GetMenuSerializer(**json)
    assert obj_from_response == menu
    assert response.status_code == 200


async def test_update_incorrect_menu(async_client: AsyncClient):
    response = await async_client.patch(f"{base_url}/{incorrect_id}", json=update_menu)
    assert response.status_code == 404


async def test_delete_menu(async_client: AsyncClient):
    response = await async_client.delete(f"{base_url}/{create_menu['id']}")
    menu = await MenuServices.check_menu_exists(create_menu['id'])
    assert response.status_code == 200
    assert menu is False


async def test_delete_incorrect_menu(async_client: AsyncClient):
    response = await async_client.delete(f"{base_url}/{incorrect_id}")
    assert response.status_code == 404
