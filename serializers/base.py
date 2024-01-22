from pydantic import BaseModel, UUID4


class ResponseSerializer(BaseModel):
    id: UUID4
    title: str
    description: str