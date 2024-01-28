from httpx import AsyncClient

from tests.conftest import base_url
from tests.data.menu import create_menu
from tests.data.submenu import create_submenu, update_submenu, create_incorrect_submenu, incorrect_id


async def test_add_menu(async_client: AsyncClient):
    response = await async_client.post(base_url, json=create_menu)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json().get('title') == create_menu['title']
    assert response.json().get('description') == create_menu['description']

    create_menu['id'] = response.json().get('id')


async def test_get_submenus_empty_list(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu['id']}/submenus")
    assert response.status_code == 200
    assert response.json() == []


async def test_add_submenu(async_client: AsyncClient):
    response = await async_client.post(f"{base_url}/{create_menu['id']}/submenus", json=create_submenu)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json().get('title') == create_submenu['title']
    assert response.json().get('description') == create_submenu['description']

    create_submenu['id'] = response.json().get('id')


async def test_add_incorrect_submenu(async_client: AsyncClient):
    response = await async_client.post(f"{base_url}/{create_menu['id']}/submenus", json=create_incorrect_submenu)
    assert response.status_code == 422


async def test_add_submenu_to_incorrect_menu(async_client: AsyncClient):
    response = await async_client.post(f"{base_url}/{incorrect_id}/submenus", json=create_submenu)
    assert response.status_code == 404


async def test_get_submenus_list(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu['id']}/submenus")
    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_get_submenu_by_id(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu['id']}/submenus/{create_submenu['id']}")
    assert response.status_code == 200
    assert response.json().get('id') == create_submenu.get('id')
    assert response.json().get('menu_id') == create_menu.get('id')


async def test_get_submenu_by_incorrect_id(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{incorrect_id}/submenus/{incorrect_id}")
    assert response.status_code == 404


async def test_update_submenu(async_client: AsyncClient):
    response = await async_client.patch(f"{base_url}/{create_menu['id']}/submenus/{create_submenu['id']}",
                                        json=update_submenu)
    assert response.status_code == 200
    assert response.json().get('id') == create_submenu.get('id')
    assert response.json().get('title') == update_submenu.get('title')
    assert response.json().get('description') == update_submenu.get('description')


async def test_update_incorrect_submenu(async_client: AsyncClient):
    response = await async_client.patch(f"{base_url}/{create_menu['id']}/submenus/{incorrect_id}",
                                        json=update_submenu)
    assert response.status_code == 404


async def test_delete_submenu(async_client: AsyncClient):
    response = await async_client.delete(f"{base_url}/{create_menu['id']}/submenus/{create_submenu['id']}")
    assert response.status_code == 200
    delete_response = await async_client.get(f"{base_url}/{create_menu.get('id')}/{create_submenu['id']}")
    assert delete_response.status_code == 404


async def test_delete_incorrect_submenu(async_client: AsyncClient):
    response = await async_client.delete(f"{base_url}/{create_menu['id']}/submenus/{incorrect_id}")
    assert response.status_code == 404


async def test_delete_menu(async_client: AsyncClient):
    response = await async_client.delete(f"{base_url}/{create_menu.get('id')}")
    assert response.status_code == 200
    delete_response = await async_client.get(f"{base_url}/{create_menu.get('id')}")
    assert delete_response.status_code == 404
