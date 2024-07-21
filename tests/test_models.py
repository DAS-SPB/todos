import pytest
import logging

from application.api.schemas.todo import TodoCreate
from application.api.schemas.user import UserCreate

from pymongo import MongoClient
from bson.objectid import ObjectId

from application.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

uri = settings.DATABASE_URL
client = MongoClient(uri)

test_db = client['test_todo_app']
collection_users = test_db['test_collection_users']
collection_todos = test_db['test_collection_todos']


@pytest.fixture(scope='function', autouse=True)
def clean_db():
    logger.info("Cleaning up collections before test run...")
    collection_todos.delete_many({})
    collection_users.delete_many({})
    yield


def test_create_user():
    user_data = {"username": "testuser", "password": "testpassword"}
    user = UserCreate(**user_data)
    assert user.username == "testuser"
    assert user.password == "testpassword"


def test_create_todo_all_fields():
    todo_data = {"title": "Test todo", "description": "Test todo creation", "completed": True}
    todo = TodoCreate(**todo_data)
    assert todo.title == "Test todo"
    assert todo.description == "Test todo creation"
    assert todo.completed is True


def test_create_todo_only_mandatory_fields():
    todo_data = {"title": "Test todo", "description": "Test todo creation without 'completed' field"}
    todo = TodoCreate(**todo_data)
    assert todo.title == "Test todo"
    assert todo.description == "Test todo creation without 'completed' field"
    assert todo.completed is False


def test_create_user_db():
    user_data = {"username": "testuser", "password": "testpassword"}
    result = collection_users.insert_one(user_data)
    inserted_id = result.inserted_id
    assert inserted_id is not None
    logger.info(f"Created user id: {inserted_id}")

    test_db_user = collection_users.find_one({"_id": ObjectId(inserted_id)})
    assert test_db_user['username'] == "testuser"
    assert test_db_user['password'] == "testpassword"


def test_create_todo_db():
    todo_data = {"title": "Test todo", "description": "Test todo creation", "completed": True}
    result = collection_todos.insert_one(todo_data)
    inserted_id = result.inserted_id
    assert inserted_id is not None
    logger.info(f"Created todo id: {inserted_id}")

    test_db_todo = collection_todos.find_one({"_id": ObjectId(inserted_id)})
    assert test_db_todo['title'] == "Test todo"
    assert test_db_todo['description'] == "Test todo creation"
    assert test_db_todo['completed'] is True
