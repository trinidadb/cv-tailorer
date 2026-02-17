from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from src.routers import cv_tailor


def initialize_resources():
    pass


def shutdown_resources():
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_resources()
    yield
    shutdown_resources()


app = FastAPI(
    title="API Template",
    description="API Template",
    version='1.0',
    lifespan=lifespan,
)

origins = [
    "http://localhost:8002",
    "http://127.0.0.1:8002",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(cv_tailor)

app.mount("/", StaticFiles(directory="./src/static", html=True), name="static")

@app.get('/', tags=['root'])
async def read_root():
    return {
        "message": "Welcome to  API Template . Visit /docs for documentation."
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
