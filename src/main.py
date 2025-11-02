from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.core.db.database import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan,
)
