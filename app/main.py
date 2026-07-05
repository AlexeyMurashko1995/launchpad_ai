from fastapi import FastAPI
from app.routers.startups import router as startup_router

app = FastAPI()

app.include_router(startup_router)