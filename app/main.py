from fastapi import FastAPI
from app.routers.startups import router as startup_router
from app.routers.auth import router as auth_router
from app.core.database import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(startup_router)
app.include_router(auth_router)