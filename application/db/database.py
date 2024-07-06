from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from fastapi import HTTPException, status

from ..db.connection import collection_users, collection_todos


async def insert_to_db(data: dict, collection: AsyncIOMotorCollection) -> InsertOneResult:
    try:
        inserted_data = await collection.insert_one(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to insert data to MongoDB: {str(e)}")

    return inserted_data


async def insert_user_to_db(data: dict, collection=collection_users):
    query = {"username": data.get("username")}
    match = await collection.find_one(query)
    if match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is taken")

    return await insert_to_db(data=data, collection=collection_users)


async def find_one_in_db(data: dict, collection: AsyncIOMotorCollection):
    try:
        fetched_data = await collection.find_one(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to fetch data from MongoDB: {str(e)}")

    return fetched_data


async def find_many_in_db(data: dict, collection: AsyncIOMotorCollection, skip: int = 0, limit: int = 10):
    try:
        cursor = collection.find(data).skip(skip).limit(limit)
        fetched_data = await cursor.to_list(length=limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to fetch data from MongoDB: {str(e)}")

    return fetched_data


async def update_todo_in_db(data: dict, username: str, collection=collection_todos) -> UpdateResult:
    query = {
        "username": username,
        "_id": data.get("id")
    }
    try:
        await collection.update_one(filter=query, update={"$set": data})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to update data in MongoDB: {str(e)}")

    updated_record = await find_one_in_db(data=query, collection=collection)

    return updated_record


async def delete_todo_in_db(todo_id: str, username: str, collection=collection_todos) -> DeleteResult:
    query = {
        "username": username,
        "id": todo_id
    }
    try:
        deleted_data = await collection.delete_one(filter=query)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to delete data in MongoDB: {str(e)}")

    return deleted_data.raw_result
