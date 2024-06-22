from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from ..schemas.todo import TodoCreate, TodoUpdate, TodoDelete, TodoResponse
from ...core.security import get_user_by_valid_token
from ...db.connection import collection_todos
from ...db.database import insert_to_db, find_one_in_db, find_many_in_db, update_todo_in_db, delete_todo_in_db

router = APIRouter()


@router.post("/todo/", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def create_todo(todo: TodoCreate, username: str = Depends(get_user_by_valid_token)):
    todo_dict = {
        "username": username,
        "title": todo.title,
        "description": todo.description
    }
    created_todo = await insert_to_db(data=todo_dict, collection=collection_todos)

    return created_todo


@router.get("/todos/", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
async def read_todos(skip: int = 0, limit: int = 10, username: str = Depends(get_user_by_valid_token)):
    query = {"username": username}
    fetched_todos = await find_many_in_db(data=query, collection=collection_todos, skip=skip, limit=limit)

    return fetched_todos


@router.get("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def read_todo(todo_id: str, username: str = Depends(get_user_by_valid_token)):
    query = {
        "username": username,
        "id": todo_id
    }
    fetched_todo = await find_one_in_db(data=query, collection=collection_todos)

    if fetched_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return fetched_todo


@router.put("/todos/update", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def update_todo(todo_update: TodoUpdate, username: str = Depends(get_user_by_valid_token)):
    updated_data = await update_todo_in_db(data=todo_update.dict(), username=username, collection=collection_todos)

    return updated_data


@router.delete("/todos/{todo_id}", response_model=TodoDelete, status_code=status.HTTP_200_OK)
async def delete_todo(todo_id: str, username: str = Depends(get_user_by_valid_token)):
    deleted_todo = delete_todo_in_db(todo_id=todo_id, username=username)

    return deleted_todo
