from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import InsertOneResult
from fastapi import HTTPException

from ..db.connection import collection_users


async def insert_to_db(data: dict, collection: AsyncIOMotorCollection) -> InsertOneResult:
    try:
        inserted_data = await collection.insert_one(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert data to MongoDB: {str(e)}")

    return inserted_data


async def insert_user_to_db(data: dict, collection=collection_users):
    query = {"username": data.get("username")}
    match = await collection.find_one(query)
    if match:
        raise HTTPException(status_code=400, detail="This username is taken")

    return await insert_to_db(data=data, collection=collection_users)
