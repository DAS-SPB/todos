import uuid
import pytest
import logging

from fastapi.testclient import TestClient
from pymongo import MongoClient
from main import application
from application.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# uri = settings.DATABASE_URL
# mongo_client = MongoClient(uri)
# test_db = mongo_client['test_todo_app']
# collection_users = test_db['test_collection_users']
# collection_todos = test_db['test_collection_todos']

api_client = TestClient(application)
prefix = "/api/v1"
jwt_token = None
random_uuid = None
todo_id = None


# @pytest.fixture(scope='function', autouse=True)
# def setup_teardown_db():
#     logger.info("Cleaning up collections before test run...")
#     collection_todos.delete_many({})
#     collection_users.delete_many({})
#     yield


def auth_header():
    global jwt_token

    return {"Authorization": f"Bearer {jwt_token}"}


def test_read_root():
    response = api_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to simple TODO API"}


def test_create_user():
    global random_uuid

    random_uuid = uuid.uuid4()
    json = {"username": f"{random_uuid}username", "password": "testpassword"}
    response = api_client.post(f"{prefix}/register/", json=json)
    assert response.status_code == 201
    assert "id" in response.json()
    assert "username" in response.json()
    assert response.json().get("username") == f"{random_uuid}username"

    logger.info(f"uuid: {random_uuid}")


def test_login():
    global jwt_token
    global random_uuid

    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {"username": f"{random_uuid}username", "password": "testpassword"}
    response = api_client.post(f"{prefix}/login/", data=data, headers=headers)

    logger.info(f"uuid: {random_uuid}")

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json().get("token_type") == "bearer"
    jwt_token = response.json().get("access_token")


def test_create_todo():
    global todo_id

    json = {"title": "New todo", "description": "test description"}
    response = api_client.post(f"{prefix}/todo/", json=json, headers=auth_header())
    assert response.status_code == 200
    todo = response.json()
    assert "id" in todo
    assert todo["title"] == "New todo"
    assert todo["description"] == "test description"
    assert todo["completed"] is False
    todo_id = todo.get("id")


def test_read_todos():
    response = api_client.get(f"{prefix}/todos/", headers=auth_header())
    assert response.status_code == 200
    todos = response.json()
    assert isinstance(todos, list)
    assert len(todos) > 0


def test_read_todo():
    global todo_id

    response = api_client.get(f"{prefix}/todos/{todo_id}", headers=auth_header())
    assert response.status_code == 200
    todo = response.json()
    assert todo["id"] == todo_id
    assert todo["title"] == "New todo"
    assert todo["description"] == "test description"
    assert todo["completed"] is False


def test_read_invalid_todo():
    invalid_todo_id = 999
    response = api_client.get(f"{prefix}/todos/{invalid_todo_id}", headers=auth_header())
    assert response.status_code == 404


def test_update_todo():
    global todo_id

    json = {"id": todo_id, "title": "updated title", "description": "updated description", "completed": True}
    response = api_client.put(f"{prefix}/todos/update", json=json, headers=auth_header())
    assert response.status_code == 200
    todo = response.json()
    assert todo["id"] == todo_id
    assert todo["title"] == "updated title"
    assert todo["description"] == "updated description"
    assert todo["completed"] is True


def test_delete_todo():
    global todo_id

    response = api_client.delete(f"{prefix}/todos/{todo_id}", headers=auth_header())
    assert response.status_code == 200
    todo = response.json()
    assert todo["message"] == f"Todo with id '{todo_id}' deleted"
