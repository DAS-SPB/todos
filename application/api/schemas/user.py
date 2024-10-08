from pydantic import BaseModel, Field

USERNAME_PATTERN = r"^[\p{L}\p{N}\.'-]+(?: [\p{L}\p{N}\.'-]+)*$"
PASSWORD_PATTERN = r"^[\w\.,<>~!@#$%^&*()_+-]+$"


class UserCreate(BaseModel):
    username: str = Field(description="Username should be a string", min_length=5, max_length=250,
                          pattern=USERNAME_PATTERN)
    password: str = Field(description="Password should be a string", min_length=5, max_length=250,
                          pattern=PASSWORD_PATTERN)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "John Doe",
                    "password": "apple007.,<>~!@#$%^&*()_+"
                }
            ]
        }
    }


class UserResponse(BaseModel):
    id: str
    username: str
