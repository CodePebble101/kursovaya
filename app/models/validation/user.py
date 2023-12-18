import re
from typing import Optional

from pydantic import BaseModel, model_validator, ValidationError


class UserCreate(BaseModel):
    username: str
    password: str

    @model_validator(mode="after")
    @classmethod
    def validate_data(cls, values):
        email_pattern=re.compile(r"^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$")
        if not email_pattern.match(values.username):
            raise ValueError("EMAIL_NOT_VALID")
        return values



class User(BaseModel):
    id: int
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
