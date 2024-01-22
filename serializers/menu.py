from pydantic import BaseModel, UUID4, Extra


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
