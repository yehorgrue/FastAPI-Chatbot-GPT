from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from schemas.user import UserPrivateSchema

from config.database import get_db_session

from models.user import User

from auth.auth import get_current_user

router = APIRouter()


@router.get("/user/all", response_model=UserPrivateSchema)
async def getAllUser(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    if current_user.role == "admin":
        pass
    return None
