from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str

class UserCredentials(BaseModel):
    email: str
    password: str

