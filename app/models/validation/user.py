from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
