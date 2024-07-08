from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

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
        "description": todo.description,
        "completed": todo.completed or False
    }
    created_todo = await insert_to_db(data=todo_dict, collection=collection_todos)

    return TodoResponse(
        id=str(created_todo.inserted_id),
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )


@router.get("/todos/", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
async def read_todos(skip: int = 0, limit: int = 10, username: str = Depends(get_user_by_valid_token)):
    query = {"username": username}
    fetched_todos = await find_many_in_db(data=query, collection=collection_todos, skip=skip, limit=limit)

    return [
        TodoResponse(
            id=str(todo.get("_id")),
            title=todo.get("title"),
            description=todo.get("description"),
            completed=todo.get("completed")
        )
        for todo in fetched_todos
    ]


@router.get("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def read_todo(todo_id: str, username: str = Depends(get_user_by_valid_token)):
    query = {
        "username": username,
        "_id": ObjectId(todo_id)
    }
    fetched_todo = await find_one_in_db(data=query, collection=collection_todos)

    if fetched_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    return TodoResponse(
        id=str(fetched_todo.get("_id")),
        title=fetched_todo.get("title"),
        description=fetched_todo.get("description"),
        completed=fetched_todo.get("completed")
    )


@router.put("/todos/update", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def update_todo(todo_update: TodoUpdate, username: str = Depends(get_user_by_valid_token)):
    updated_data = await update_todo_in_db(data=todo_update.dict(), username=username, collection=collection_todos)

    return TodoResponse(
        id=str(updated_data.get("_id")),
        title=updated_data.get("title"),
        description=updated_data.get("description"),
        completed=updated_data.get("completed")
    )


@router.delete("/todos/{todo_id}", response_model=TodoDelete, status_code=status.HTTP_200_OK)
async def delete_todo(todo_id: str, username: str = Depends(get_user_by_valid_token)):
    await delete_todo_in_db(todo_id=todo_id, username=username)

    return TodoDelete(message=f"Todo with id '{todo_id}' deleted")
