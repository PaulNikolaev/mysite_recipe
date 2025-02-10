from pydantic import BaseModel
from typing import Optional



class CategoryCreate(BaseModel):
    title: str
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    title: str
    description: str | None

    class Config:
        from_attributes = True