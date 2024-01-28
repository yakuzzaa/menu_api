from httpx import AsyncClient

from tests.conftest import base_url
from tests.data.menu import create_menu, update_menu, create_incorrect_menu, incorrect_id


async def test_get_menu_empty_list(async_client: AsyncClient):
    response = await async_client.get(base_url)
    assert response.status_code == 200
    assert response.json() == []


async def test_add_menu(async_client: AsyncClient):
    response = await async_client.post(base_url, json=create_menu)
    assert response.status_code == 201
    assert "id" in response.json()
    assert create_menu['title'] == response.json().get('title')
    assert create_menu['description'] == response.json().get('description')

    create_menu['id'] = response.json().get('id')


async def test_add_incorrect_menu(async_client: AsyncClient):
    response = await async_client.post(base_url, json=create_incorrect_menu)
    assert response.status_code == 422


async def test_get_menu_list(async_client: AsyncClient):
    response = await async_client.get(base_url)
    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_get_menu_by_incorrect_id(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{incorrect_id}")
    assert response.status_code == 404


async def test_get_menu_by_id(async_client: AsyncClient):
    response = await async_client.get(f"{base_url}/{create_menu.get('id')}")
    assert response.status_code == 200
    assert response.json().get('id') == create_menu.get('id')


async def test_update_menu(async_client: AsyncClient):
    response = await async_client.patch(f"{base_url}/{create_menu.get('id')}", json=update_menu)
    assert response.status_code == 200
    assert response.json().get('id') == create_menu.get('id')
    assert response.json().get('title') == update_menu.get('title')
    assert response.json().get('description') == update_menu.get('description')


async def test_update_incorrect_menu(async_client: AsyncClient):
    response = await async_client.patch(f"{base_url}/{incorrect_id}", json=update_menu)
    assert response.status_code == 404


async def test_delete_menu(async_client: AsyncClient):
    response = await async_client.delete(f"{base_url}/{create_menu.get('id')}")
    assert response.status_code == 200
    delete_response = await async_client.get(f"{base_url}/{create_menu.get('id')}")
    assert delete_response.status_code == 404


async def test_delete_incorrect_menu(async_client: AsyncClient):
    response = await async_client.delete(f"{base_url}/{incorrect_id}")
    assert response.status_code == 404
