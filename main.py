from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException

from config import database

from routers.api import api_router

from config.config import PROJECT_NAME, API_VERSION_STR


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run when starts the server.
    print("Starting server...")
    print("Connecting database...")
    await database.database.connect()
    database.drop_all_tables()
    database.create_tables()
    yield
    # Run when shutdown the server.
    print("Shutdown server..")
    await database.database.disconnect()


app = FastAPI(
    title=PROJECT_NAME,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def check_health():
    return {"response": "AdamoAI is healthy !!"}


app.include_router(api_router, prefix=API_VERSION_STR, tags=[])
