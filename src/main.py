from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from src.core.db.database import db_helper
from src.routers import router as organizations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan,
    title="Organizations API",
    description="API для работы с организациями, зданиями и видами деятельности",
    version="1.0.0",
)


router = APIRouter(prefix="/api")
router.include_router(organizations_router)
app.include_router(router)
