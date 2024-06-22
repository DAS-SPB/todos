from pydantic import BaseModel, Field

from typing import Optional

TITLE_PATTERN = r'\w'
DESCRIPTION_PATTERN = r'\w'


class TodoCreate(BaseModel):
    title: str = Field(description="Title should be a string", min_length=5, max_length=250,
                       pattern=TITLE_PATTERN)
    description: str = Field(description="Description should be a string", min_length=5, max_length=250,
                             pattern=DESCRIPTION_PATTERN)
    completed: Optional[bool] = False

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Urgent todo title",
                    "description": "To take a shower"
                }
            ]
        }
    }


class TodoUpdate(BaseModel):
    id: str
    title: Optional[str] = Field(description="Title should be a string", min_length=5, max_length=250,
                                 pattern=TITLE_PATTERN)
    description: Optional[str] = Field(description="Description should be a string", min_length=5, max_length=250,
                                       pattern=DESCRIPTION_PATTERN)
    completed: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "12345",
                    "title": "Updated todo title",
                    "description": "To take a nap",
                    "completed": True
                }
            ]
        }
    }


class TodoDelete(BaseModel):
    id: str


class TodoResponse(BaseModel):
    id: str
    title: str
    description: str
    completed: bool
