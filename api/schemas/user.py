from typing import Optional
from pydantic import BaseModel, field_validator


class User(BaseModel):
    username: str
    password: str

class UserCreate(User):
    @field_validator("username")
    def username_no_spaces(cls, v):
        if " " in v:
            raise ValueError("Username must not contain spaces")
        return v
    
    @field_validator("password")
    def password_no_spaces(cls, v):
        if " " in v:
            raise ValueError("Password must not contain spaces")
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    success: bool = True