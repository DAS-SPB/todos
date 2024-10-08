from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.user import UserCreate, UserResponse
from ...core.security import get_password_hash, create_access_token, get_user_by_valid_token, verify_password
from ...db.connection import collection_users
from ...db.database import insert_user_to_db, find_one_in_db

router = APIRouter()


@router.post('/register/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    user_dict = {
        "username": user.username,
        "password": get_password_hash(user.password)
    }
    created_user = await insert_user_to_db(data=user_dict)

    return UserResponse(
        id=str(created_user.inserted_id),
        username=user.username
    )


@router.post("/login/", status_code=status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    query = {"username": form_data.username}
    user = await find_one_in_db(data=query, collection=collection_users)

    if not user or not verify_password(form_data.password, user.get('password')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    jwt_token = create_access_token({"sub": form_data.username})

    return {"access_token": jwt_token, "token_type": "bearer"}


@router.get("/about_me/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def read_user(username: str = Depends(get_user_by_valid_token)):
    query = {"username": username}
    user = await find_one_in_db(data=query, collection=collection_users)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse(
        id=str(user.get("_id")),
        username=user.get("username")
    )
