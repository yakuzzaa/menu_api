from decimal import Decimal

from google_sheet.sheet_parse import load_global_data


def get_price_with_discount(dish_id: str) -> None | int | Decimal:
    global_data = load_global_data()
    for item in global_data:
        keys_list = list(item.keys())
        if (item['id'] == dish_id) and ('discount' in keys_list):
            price: Decimal = Decimal(item['price'])
            discount: int = int(item['discount'])
            price_with_discount = Decimal((price / 100) * (100 - discount))
            round_price = round(price_with_discount, ndigits=2)
            return round_price
    return None
