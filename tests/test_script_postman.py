from httpx import AsyncClient

from tests.conftest import base_url
from tests.data.dish import create_dish1, create_dish2
from tests.data.menu import create_menu, update_menu, create_incorrect_menu, incorrect_id
from tests.data.submenu import create_submenu


async def test_add_menu(async_client: AsyncClient):
    response = await async_client.post(base_url, json=create_menu)
    assert response.status_code == 201
    assert "id" in response.json()
    assert create_menu['title'] == response.json().get('title')
    assert create_menu['description'] == response.json().get('description')

    create_menu['id'] = response.json().get('id')


async def test_add_submenu(async_client: AsyncClient):
    response = await async_client.post(f"{base_url}/{create_menu['id']}/submenus", json=create_submenu)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json().get('title') == create_submenu['title']
    assert response.json().get('description') == create_submenu['description']

    create_submenu['id'] = response.json().get('id')


async def test_add_dish1(async_client: AsyncClient):
    response = await async_client.post(f"{base_url}/{create_menu['id']}/submenus/{create_submenu['id']}/dishes",
                                       json=create_dish1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json().get('title') == create_dish1['title']
    assert response.json().get('description') == create_dish1['description']
    assert response.json().get('price') == create_dish1['price']

    create_dish1['id'] = response.json().get('id')


async def test_add_dish2(async_client: AsyncClient):
    response = await async_client.post(f"{base_url}/{create_menu['id']}/submenus/{create_submenu['id']}/dishes",
                                       json=create_dish2)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json().get('title') == create_dish2['title']
    assert response.json().get('description') == create_dish2['description']
    assert response.json().get('price') == create_dish2['price']

    create_dish2['id'] = response.json().get('id')


async def test_get_menu_by_id(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu.get('id')}")
    assert response.status_code == 200
    assert response.json().get('id') == create_menu.get('id')
    assert response.json().get('title') == create_menu.get('title')
    assert response.json().get('description') == create_menu.get('description')
    assert response.json().get('submenus_count') == 1
    assert response.json().get('dishes_count') == 2


async def test_get_submenu_by_id(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu['id']}/submenus/{create_submenu['id']}")
    assert response.status_code == 200
    assert response.json().get('id') == create_submenu.get('id')
    assert response.json().get('menu_id') == create_menu.get('id')
    assert response.json().get('title') == create_submenu.get('title')
    assert response.json().get('description') == create_submenu.get('description')
    assert response.json().get('dishes_count') == 2


async def test_delete_submenu(async_client: AsyncClient):
    response = await async_client.delete(f"{base_url}/{create_menu['id']}/submenus/{create_submenu['id']}")
    assert response.status_code == 200
    delete_response = await async_client.get(f"{base_url}/{create_menu.get('id')}/{create_submenu['id']}")
    assert delete_response.status_code == 404


async def test_get_submenus_empty_list(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu['id']}/submenus")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_dish_empty_list(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu['id']}/submenus/{create_submenu['id']}/dishes")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_menu_by_id2(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu.get('id')}")
    assert response.status_code == 200
    assert response.json().get('id') == create_menu.get('id')
    assert response.json().get('title') == create_menu.get('title')
    assert response.json().get('description') == create_menu.get('description')
    assert response.json().get('submenus_count') == 0
    assert response.json().get('dishes_count') == 0


async def test_delete_menu(async_client: AsyncClient):
    response = await async_client.delete(f"{base_url}/{create_menu.get('id')}")
    assert response.status_code == 200
    delete_response = await async_client.get(f"{base_url}/{create_menu.get('id')}")
    assert delete_response.status_code == 404


async def test_get_menu_empty_list(async_client: AsyncClient):
    response = await async_client.get(base_url)
    assert response.status_code == 200
    assert response.json() == []
