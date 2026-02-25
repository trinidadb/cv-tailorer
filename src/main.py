from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

from src.routers import tailorRouter, atsRouter, keywordsRouter

http_port = os.getenv("HTTP_PORT")


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
    f"http://localhost:{http_port}",
    f"http://127.0.0.1:{http_port}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tailorRouter)
app.include_router(atsRouter)
app.include_router(keywordsRouter)

app.mount("/", StaticFiles(directory="./src/static", html=True), name="static")


@app.get('/', tags=['root'])
async def read_root():
    return {
        "message": "Welcome to  API Template . Visit /docs for documentation."
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(http_port))
    #uvicorn.run("src.main:app", host="0.0.0.0", port=int(http_port), reload=True)
