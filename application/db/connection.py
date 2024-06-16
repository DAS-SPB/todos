from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient

from ..core.config import settings

uri = settings.DATABASE_URL

client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

db = client['todo_app']
collection_users = db['users']
collection_todos = db['todos']
