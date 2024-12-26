from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_session
from ..crud import create_message, get_user_by_username, get_history_by_username
from ..utils import ask_openai

router = APIRouter()


class AskInput(BaseModel):
    username: str
    question: str


@router.post("/ask", summary="Ask a question to the chatbot", tags=["Chatbot"])
def ask(input_data: AskInput, session: Session = Depends(get_session)):
    """
    Sends a question to the chatbot and retrieves a response.

    - **username**: The username of the person asking the question.
    - **question**: The question to ask the chatbot.
    """
    user = get_user_by_username(session, input_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    response = ask_openai(input_data.username, input_data.question, user.role, session)
    create_message(session, input_data.username, input_data.question, response)
    return {"response": response}


@router.get("/history/{username}", summary="Retrieve chat history", tags=["Chatbot"])
def get_history(username: str, session: Session = Depends(get_session)):
    """
    Retrieves the chat history for a specific user.

    - **username**: The username whose chat history you want to retrieve.
    """
    user = get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    history = get_history_by_username(session, username)
    return {"history": [{"question": msg.question, "response": msg.response} for msg in history]}
