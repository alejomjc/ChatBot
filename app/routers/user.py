from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_session
from ..crud import create_user, get_user_by_username

router = APIRouter()


class UserInput(BaseModel):
    username: str
    role: str


@router.post("/init_user", summary="Initialize a new user", tags=["Users"])
def init_user(user: UserInput, session: Session = Depends(get_session)):
    """
    Creates a new user with a specific role.

    - **username**: The name of the user to initialize.
    - **role**: The role assigned to the user.
    """
    if get_user_by_username(session, user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    created_user = create_user(session, user.username, user.role)
    return {"message": "User created", "user": created_user}
