from app import todo_crud
from typing import List
from fastapi import APIRouter, Depends, status
from app.schema.todo_schema import Todo, TodoCreate, TodoUpdate
from app.database import get_db


router = APIRouter()


@router.get("/", response_model=List[Todo])
async def read_todos(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return await todo_crud.get_todos(db, skip, limit)


@router.get("/{todo_id}")
async def read_one_todo(todo_id: int, db=Depends(get_db)):
    return await todo_crud.get_todo(db, todo_id)


@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, db=Depends(get_db)):
    return await todo_crud.create_todo(db, todo)


@router.patch("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: TodoUpdate, db=Depends(get_db)):
    return await todo_crud.update_todo(db, todo_id, todo)


@router.delete("/{todo_id}",
               status_code=status.HTTP_200_OK,
               summary="Delete todo",
               response_description="Successful deletion message")
async def delete_todo(todo_id: int, db=Depends(get_db)) -> dict:
    return await todo_crud.delete_todo(db, todo_id)
