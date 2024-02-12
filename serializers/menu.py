from pydantic import UUID4, BaseModel

from serializers.base import ResponseSerializer
from serializers.submenu import SubmenuForMenuSerializer


class AddMenuSerializer(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class GetMenuSerializer(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True
        from_attributes = True


class MenuResponseSerializer(ResponseSerializer):
    submenus_count: int
    dishes_count: int


class GetFullMenuSerializer(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus: list[SubmenuForMenuSerializer]

    class Config:
        orm_mode = True
        from_attributes = True
