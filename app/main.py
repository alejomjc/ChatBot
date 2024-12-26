from fastapi import FastAPI

from .routers import user, chatbot, system
from .database import init_db

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(user.router)
app.include_router(chatbot.router)
app.include_router(system.router)
