from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers import user, chatbot, system
from .database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(chatbot.router)
app.include_router(system.router)
