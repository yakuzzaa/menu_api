from pydantic import UUID4, BaseModel


class ResponseSerializer(BaseModel):
    id: UUID4
    title: str
    description: str
