import asyncio
import json
import os
from typing import Any

import gspread
from asgiref.sync import async_to_sync
from gspread import Client, Spreadsheet
from pydantic import UUID4

from database.redis import redis_client
from google_sheet.celery_app import celery
from repository.google_sheet import (
    check_and_delite_dish,
    check_and_delite_menu,
    check_and_delite_submenu,
    create_update_dish,
    create_update_menu,
    create_update_submenu,
)

SPREADSHEET_URL: str = 'https://docs.google.com/spreadsheets/d/1BUrzAiPP5ZVJ5VTjNHA5yTIMPNJmHVUWKSVbImB_Vb4/edit#gid=0'
global_data_path = 'google_sheet/global_data.json'

loop = asyncio.get_event_loop()


def load_sheet_data() -> list:
    gc: Client = gspread.service_account(filename='google_sheet/menuapi-414013-0bf6c7671560.json')
    sh: Spreadsheet = gc.open_by_url(SPREADSHEET_URL)
    try:
        data: list = sh.sheet1.get_all_values()
        return data
    except Exception as e:
        print(f'Error loading sheet data: {e}')
        return []


def load_global_data() -> list | list[dict]:
    if os.path.exists(global_data_path):
        try:
            with open(global_data_path, encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f'Error with loading global data: {e}')
    return []


def save_global_data(data: list[dict]) -> None:
    try:
        with open(global_data_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f'Error with saving global data: {e}')


async def get_data_from_sheet() -> list[dict]:
    data: list[dict] = load_sheet_data()
    data_list: list = []
    menu_id: UUID4 = None
    submenu_id: UUID4 = None

    for item in data:
        item_dict: dict = {}
        if item[0] != '':
            item_dict['id'] = item[0].replace('\n', '')
            item_dict['title'] = item[1].replace('\n', '')
            item_dict['description'] = item[2].replace('\n', '')

            menu_id = item[0].replace(' ', '')
            data_list.append(item_dict)
        elif item[1] != '':
            item_dict['id'] = item[1].replace('\n', '')
            item_dict['menu_id'] = menu_id
            item_dict['title'] = item[2].replace('\n', '')
            item_dict['description'] = item[3].replace('\n', '')

            submenu_id = item[1]
            data_list.append(item_dict)
        else:
            item_dict['id'] = item[2].replace('\n', '')
            item_dict['menu_id'] = menu_id.replace('\n', '')
            item_dict['submenu_id'] = submenu_id.replace('\n', '')
            item_dict['title'] = item[3].replace('\n', '')
            item_dict['description'] = item[4].replace('\n', '')
            item_dict['price'] = item[5].replace(',', '.').replace('\n', '')
            if item[6]:
                item_dict['discount'] = item[6].replace(',', '.').replace('\n', '')
            data_list.append(item_dict)
    return data_list


def get_data_type(item: dict) -> str:
    if 'menu_id' not in item:
        return 'menu'
    elif 'submenu_id' not in item:
        return 'submenu'
    else:
        return 'dish'


async def find_difference(new_data: list[dict], old_data: list[dict]) -> list[dict[Any, Any]]:
    result: list = []
    list_of_new_ids: list = [entry['id'] for entry in new_data]

    if new_data == old_data:
        return []
    if old_data is None:
        for new_item in new_data:
            data_type: str = get_data_type(new_item)
            data_dict: dict = {f'{data_type}_create': new_item}
            result.append(data_dict)
        return result
    for new_item in new_data:
        data_type = get_data_type(new_item)
        for old_item in old_data:
            if old_item['id'] == new_item['id']:
                if old_item != new_item:
                    data_dict = {f'{data_type}_update': new_item}
                    result.append(data_dict)
                break
        if new_item not in old_data:
            data_dict = {f'{data_type}_create': new_item}
            result.append(data_dict)

    for old_item in old_data:
        data_type = get_data_type(old_item)
        if old_item['id'] not in list_of_new_ids:
            data_dict = {f'{data_type}_delete': old_item}
            result.append(data_dict)

    return result


async def sheet_crud(diff_data: list[dict]) -> None:
    for data in diff_data:
        data_key: list = list(data.keys())
        action: str = data_key[0]

        action_to_function_mapping: dict = {'menu_create': create_update_menu,
                                            'menu_update': create_update_menu,
                                            'menu_delete': check_and_delite_menu,
                                            'submenu_create': create_update_submenu,
                                            'submenu_update': create_update_submenu,
                                            'submenu_delete': check_and_delite_submenu,
                                            'dish_create': create_update_dish,
                                            'dish_update': create_update_dish,
                                            'dish_delete': check_and_delite_dish
                                            }
        await action_to_function_mapping[action](data[action])


async def main_task() -> None:
    global_data: list | list[dict] = load_global_data()
    new_data: list[dict[Any, Any]] = await get_data_from_sheet()
    data_for_crud: list[dict[Any, Any]] = await find_difference(new_data=new_data, old_data=global_data)
    if not data_for_crud:
        return
    try:
        await redis_client.flushall(asynchronous=True)
    except Exception as e:
        raise e
        print(f'Error with cleaning redis: {e}')

    await sheet_crud(diff_data=data_for_crud)

    save_global_data(new_data)


@celery.task
def main():
    async_to_sync(main_task)()


if __name__ == '__main__':
    asyncio.run(main_task())
