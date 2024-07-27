# Task Manager FastAPI

Simple TODO API. Pet project implemented with using of FastAPI.

It provides basic CRUD operations for todos for authorized users.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Usage](#usage)
    - [Running the Application](#running-the-application)
    - [API Endpoints](#api-endpoints)
- [Testing with SwaggerUI](#testing-the-api-with-swagger-ui)
- [Testing with pytest](#testing-the-api-with-pytest-framework)
- [Potential Improvements](#potential-improvements)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication.
- CRUD operations for todos (Create, Read, Update, Delete).
- OAuth2 authentication for API access.
- Simple and straightforward project structure.

## Project Structure

The project follows the following directory structure:

```
task_manager_fastapi/
├── application/
│   ├── api/
│   │   ├── endpoints/
│   │   ├── middleware/
│   │   ├── schemas/
│   ├── core/
│   ├── db/
├── tests/
├── .env
├── .gitignore
├── README.md
├── main.py
├── requirements.txt
```

- `application`: Contains the main application code.
    - `api`: Contains API endpoints for todos and users.
        - `endpoints`: Todo and user API endpoints.
        - `middleware`: Custom middleware (simple logging for example).
        - `schemas`: Pydantic models for request and response.
    - `core`: Core utilities and configurations.
    - `db`: Database configuration and models.
- `tests`: Unit tests.
- `.env`: Store environment variables (e.g., database credentials).
- `.gitignore`: Lists files and directories to be ignored by version control system.
- `README.md`: Documentation about the project.
- `requirements.txt`: List of project dependencies.

## Getting Started

### Prerequisites

Before running the application, make sure you have the following prerequisites installed:

- Python 3.7+ (3.12 recommended).
- MongoDB.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DAS-SPB/todos.git
   ```

2. Create a virtual environment (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate.bat
   ```

3. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

To run the FastAPI application locally, use the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Replace `0.0.0.0` and `8000` with your desired host and port.

Or you can just run `main.py`:

```bash
python3 main.py
```

### API Endpoints

The API exposes the following endpoints:

- `POST /api/v1/users/register/`: Register a new user.
- `POST /api/v1/users/login/`: Authenticate and receive a JWT token.
- `GET /api/v1/about_me/`: Retrieve user info (protected endpoint).
- `POST /api/v1/todo/`: Create a new todo (protected endpoint).
- `GET /api/v1/todos/`: Retrieve a list of todos (protected endpoint).
- `GET /api/v1/todos/{todo_id}`: Retrieve a specific todo (protected endpoint).
- `PUT /api/v1/todos/update`: Update a specific todo (protected endpoint).
- `DELETE /api/v1/todos/{todo_id}`: Delete a specific todo (protected endpoint).

## Testing the API with Swagger UI

Fast API comes with Swagger UI. This tool is automatically generated based on your API's route definitions and Pydantic
models.

### Accessing Swagger UI

Once the API is running, Swagger UI can be accessed on the following URL:

```bash
http://localhost:8000/docs
```

You can use swagger UI to:

1. **Browse Endpoints**
2. **Send Requests**
3. **View Responses**
4. **Test Validations**

**To Test with SwaggerUI, you can do the following for each endpoint explained above**

1. Open your web browser and navigate to the /docs path as mentioned above.

2. Explore the available endpoints and select the one you want to test.

3. Click on the "Try it out" button to open an interactive form where you can input data.

4. Fill in the required parameters and request body (if applicable) according to the API documentation given above.

5. Click the "Execute" button to send the request to the API.

6. The response will be displayed below, showing the status code and response data.

7. You can also view example request and response payloads, which can be helpful for understanding the expected data
   format.

## Testing the API with pytest Framework

A suite of `tests` using the pytest framework was used to help verify the functionality of the Task Manager FastAPI.

### Running the tests

1. Navigate to the `todos` (root) directory using a terminal:

```bash
cd <your_path_to_project>/todos
```

2. Run the tests by executing the following command (don't forget to activate your virtual environment if used):

```bash
pytest
```

This command will automatically discover and run the test cases defined in the `tests` directory.
