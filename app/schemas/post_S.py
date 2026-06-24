from pydantic import BaseModel, Field
from datetime import datetime
from .user_S import UserResponseSchema

class BlogCreateSchema(BaseModel):
    title: str = Field(..., min_length=5, max_length=255, examples=["My First FastAPI Post"])
    content: str = Field(..., min_length=10, examples=["This is the long body content of the blog..."])
    summary: str | None = Field(None, max_length=600, examples=["A short intro to the post."])
    category_id: int = Field(..., examples=[1])
    
class BlogResponseSchema(BaseModel):
    id: int
    title: str
    content: str
    summary: str | None
    created_at: datetime
    last_updated: datetime
    category_id: int
    author: UserResponseSchema  

    model_config = {"from_attributes": True}