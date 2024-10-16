from pydantic import BaseModel

class Sketch(BaseModel):
    id: str
    title: str
    description: str
    image: str
    created_at: str
    updated_at: str

