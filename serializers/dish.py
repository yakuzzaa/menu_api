from pydantic import BaseModel, UUID4


class AddDishSerializer(BaseModel):
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True


class GetDishSerializer(BaseModel):
    menu_id: UUID4
    submenu_id: UUID4
    id: UUID4
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True
