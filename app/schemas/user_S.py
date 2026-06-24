from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    
class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["john_doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., min_length=8, examples=["supersecret123"])
    
class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    active: bool
    created_at: datetime
    model_config = {"from_attributes": True}