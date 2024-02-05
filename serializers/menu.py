from pydantic import UUID4, BaseModel

from serializers.base import ResponseSerializer


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
