import openai
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from ..database import get_session

router = APIRouter()


@router.get("/health", summary="Check service health", tags=["System"])
def health_check(session: Session = Depends(get_session)):
    """
    Checks the health of the service, including:
    - Database connection.
    - GPT system availability.
    """
    try:
        session.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {e}"

    try:
        openai.Model.list()
        gpt_status = "ok"
    except Exception as e:
        gpt_status = f"error: {e}"

    return {
        "service": "ok",
        "database": db_status,
        "gpt": gpt_status
    }
