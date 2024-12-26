from sqlmodel import Session, select
from .models import User, Message


def create_user(session: Session, username: str, role: str):
    user = User(username=username, role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(session: Session, username: str):
    return session.exec(select(User).where(User.username == username)).first()


def create_message(session: Session, username: str, question: str, response: str):
    message = Message(username=username, question=question, response=response)
    session.add(message)
    session.commit()
    return message


def get_history_by_username(session: Session, username: str):
    return session.exec(select(Message).where(Message.username == username)).all()
