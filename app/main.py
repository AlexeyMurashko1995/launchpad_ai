from fastapi import FastAPI
from app.routers.startups import router as startup_router
from app.routers.auth import router as auth_router

app = FastAPI()

app.include_router(startup_router)
app.include_router(auth_router)