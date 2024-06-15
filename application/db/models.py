from ..core.config import settings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = settings.DATABASE_URL

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['todo_app']
collection_users = db['users']
collection_todos = db['todos']
