from pydantic import BaseModel, UUID4
from serializers.base import ResponseSerializer

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

class SubmenuResponseSerializer(ResponseSerializer):
    pass