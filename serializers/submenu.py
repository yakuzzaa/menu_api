from pydantic import UUID4, BaseModel

from serializers.base import ResponseSerializer
from serializers.dish import DishForSubmenuSerializer


class AddSubmenuSerializer(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class GetSubmenuSerializer(BaseModel):
    menu_id: UUID4
    id: UUID4
    title: str
    description: str
    dishes_count: int

    class Config:
        orm_mode = True
        from_attributes = True


class SubmenuResponseSerializer(ResponseSerializer):
    dishes_count: int
    menu_id: UUID4


class SubmenuForMenuSerializer(BaseModel):
    id: UUID4
    title: str
    description: str
    dishes: list[DishForSubmenuSerializer]

    class Config:
        orm_mode = True
        from_attributes = True
