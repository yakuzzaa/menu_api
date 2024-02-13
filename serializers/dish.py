import decimal
from decimal import Decimal, getcontext

from pydantic import UUID4, BaseModel, field_validator

from serializers.base import ResponseSerializer


class AddDishSerializer(BaseModel):
    title: str
    description: str
    price: decimal.Decimal

    @field_validator('price')
    def make_four_digits(cls, v):
        getcontext().prec = 4
        v = Decimal(value=v) * Decimal(1)
        return v

    class Config:
        orm_mode = True


class GetDishSerializer(BaseModel):
    menu_id: UUID4
    submenu_id: UUID4
    id: UUID4
    title: str
    description: str
    price: decimal.Decimal
    price_with_discount: decimal.Decimal | str = 'Без скидки'

    class Config:
        orm_mode = True
        from_attributes = True


class DishResponseSerializer(ResponseSerializer):
    price: decimal.Decimal
    submenu_id: UUID4
    menu_id: UUID4


class DishForSubmenuSerializer(BaseModel):
    id: UUID4
    title: str
    description: str
    price: decimal.Decimal
    price_with_discount: decimal.Decimal | str

    class Config:
        orm_mode = True
        from_attributes = True
