from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str


class DefaultOut(BaseModel):
    message: str


class UserList(BaseModel):
    users: list[UserPublic]
