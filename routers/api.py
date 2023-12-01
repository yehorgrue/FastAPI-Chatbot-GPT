from fastapi import APIRouter
from . import auth, generalChat


api_router = APIRouter()


# Check API Health
@api_router.get("/")
async def root():
    """Check API Health"""
    return {
        "message": "Welcome to the backend API for FARM-docker operational of Adamo AI !"
    }


api_router.include_router(auth.router, prefix="", tags=["Auth"])
api_router.include_router(generalChat.router, prefix="", tags=["Chat"])
