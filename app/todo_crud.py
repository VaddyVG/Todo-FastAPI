from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.todo_model import Todo
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime, timezone
from app.schema.todo_schema import TodoCreate, TodoUpdate


async def get_todos(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Todo]:
    """Получить список задач с пагинацией"""
    result = await db.execute(select(Todo).offset(skip).limit(limit))
    return result.scalars().all()


async def get_todo(db: AsyncSession, todo_id: int) -> Optional[Todo]:
    """Получить задачу по ID"""
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalar_one_or_none()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo


async def create_todo(db: AsyncSession, todo_data: TodoCreate) -> Todo:
    """Создать новую задачу"""
    todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        status=todo_data.status
    )
    
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update_todo(db: AsyncSession, todo_id: int, todo_data: TodoUpdate) -> Todo:
    """Обновить существующую задачу"""
    todo = await get_todo(db, todo_id)

    update_data = todo_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    
    await db.commit()
    await db.refresh(todo)
    return todo


async def delete_todo(db: AsyncSession, todo_id: int) -> dict:
    """Удалить задачу"""
    todo = await get_todo(db, todo_id)

    await db.delete(todo)
    await db.commit()

    return {"message": f"Todo with id {todo_id} has been deleted"}
