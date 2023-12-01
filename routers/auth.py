from typing import Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Response, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.facebook import FacebookSSO

from starlette.requests import Request

from fastapi.responses import RedirectResponse

from sqlalchemy import exc
from sqlalchemy.orm import Session
from config.database import get_db_session

from config.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    FACEBOOK_CLIENT_ID,
    FACEBOOK_CLIENT_SECRET,
    SSO_CALLBACK_HOSTNAME,
    API_VERSION_STR,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SSO_LOGIN_CALLBACK_URL,
)
import schemas
from auth.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    # get_current_user_from_cookie,
)
from utils import utils

from models.user import User
from fastapi.encoders import jsonable_encoder

router = APIRouter()


google_sso = (
    GoogleSSO(
        GOOGLE_CLIENT_ID,
        GOOGLE_CLIENT_SECRET,
        f"{SSO_CALLBACK_HOSTNAME}{API_VERSION_STR}/login/google/callback",
    )
    if GOOGLE_CLIENT_ID is not None and GOOGLE_CLIENT_SECRET is not None
    else None
)


facebook_sso = (
    FacebookSSO(
        FACEBOOK_CLIENT_ID,
        FACEBOOK_CLIENT_SECRET,
        f"{SSO_CALLBACK_HOSTNAME}{API_VERSION_STR}/login/facebook/callback",
    )
    if FACEBOOK_CLIENT_ID is not None and FACEBOOK_CLIENT_SECRET is not None
    else None
)


# Register new User - to be removed if webapp is private
@router.post(
    "/register/by-email",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponseSchema,
)
async def register(
    credentials: schemas.UserRegisterSchema, db: Session = Depends(get_db_session)
):
    """
    Register a new user.
    """
    if not utils.is_valid_email(credentials.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email"
        )
    email_exists = db.query(User).filter(User.email == credentials.email).first()
    # email_exists = await models.UserDocument.find_one({"email": credentials.email})
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account of the email already exists",
        )

    # thread = create_thread()

    new_user = User(
        first_name=credentials.first_name,
        last_name=credentials.last_name,
        email=credentials.email.lower(),
        hashed_password=utils.hashed_password(credentials.password),
        created_at=datetime.utcnow(),
     )

    try:
        db.add(new_user)
        db.commit()
        res_user = db.query(User).filter(User.email == new_user.email).first()
        return res_user
    except exc.IntegrityError:
        raise HTTPException(
            status_code=400, detail="User with that email already exists."
        )


@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.

    (!Completed)
    """
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.uuid, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/login/test-token", response_model=schemas.UserPrivateSchema)
async def test_token(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Test access token
    """
    # Convert SQLAlchemy object to JSON-serializable dictionary
    json_compatible_item_data = jsonable_encoder(current_user)

    return json_compatible_item_data


# @router.get("/login/refresh-token", response_model=schemas.Token)
# async def refresh_token(
#     current_user: User = Depends(get_current_user_from_cookie),
# ) -> Any:
#     """
#     Return a new token for current user
#     """
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         current_user.uuid, expires_delta=access_token_expires
#     )
#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#     }


@router.get("/login/google")
async def google_login():
    """
    Generate login url and redirect
    """
    with google_sso:
        return await google_sso.get_login_redirect()


@router.get("/login/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db_session)):
    """
    Process login response from Google and return user info
    """
    # Get user details from Google
    google_user = await google_sso.verify_and_process(request)

    # Check if user is already created in DB
    user = db.query(User).filter(User.email == google_user.email).first()
    # user = await models.User.find_one({"email": google_user.email})
    if user is None:
        # If user does not exist, create it in DB
        user_data = {
            "email": google_user.email,
            "first_name": google_user.first_name,
            "last_name": google_user.last_name,
            "avatar": google_user.picture,
            "provider": google_user.provider,
        }

        user = User(**user_data)

        db.add(user)
        db.commit()
        db.refresh(user)

        # res_user = db.query(User).filter(User.email == user.email).first()

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Login user by creating access_token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.uuid, expires_delta=access_token_expires)
    response = RedirectResponse(SSO_LOGIN_CALLBACK_URL)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=120,
        expires=120,
    )
    return response
