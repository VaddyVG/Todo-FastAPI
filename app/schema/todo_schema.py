from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    status: bool = Field(default=False)
    description: Optional[str] = Field(None, max_length=500)


class TodoCreate(TodoBase):
    """Схема для создания задачи"""
    title: str = Field(..., example="Сходить за покупками")
    description: Optional[str] = Field(
        None, example="Молоко, хлеб, каша",
        max_length=500
    )


class TodoUpdate(BaseModel):
    """Схема для обновления задачи (все поля опциональны)"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[bool] = None
    description: Optional[str] = Field(None, max_length=500)


class Todo(TodoBase):
    """Схема для возврата задачи (с ID и датами)"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
