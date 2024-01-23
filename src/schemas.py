from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class DefaultOut(BaseModel):
    message: str


class UserList(BaseModel):
    users: list[UserPublic]
