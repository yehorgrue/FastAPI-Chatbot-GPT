from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2, OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from passlib.context import CryptContext

import models, schemas
from config.config import API_VERSION_STR, SECRET_KEY

from models.user import User

from config.database import get_db_session

from sqlalchemy.orm import Session

from utils.utils import verify_password

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
ALGORITHM = "HS256"


class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    Class used to get Authorization token from request HttpOnly cookie instead of
    header. Used to refresh token during SSO login process.
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_VERSION_STR}/login/access-token")
# oauth2_scheme_with_cookies = OAuth2PasswordBearerWithCookie(
#     tokenUrl=f"{API_VERSION_STR}/login/access-token"
# )

# password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def get_hashed_password(password: str) -> str:
#     return password_context.hash(password)


# def verify_password(password: str, hashed_pass: str) -> bool:
#     return password_context.verify(password, hashed_pass)


async def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(subject: Union[str, Any], expires_delta: timedelta):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)
):
    return await _get_current_user(token, db)


# async def get_current_user_from_cookie(
#     token: str = Depends(oauth2_scheme_with_cookies),
#     db: Session = Depends(get_db_session),
# ):
#     return _get_current_user(token, db)


async def _get_current_user(token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid: UUID = payload.get("sub")
        if userid is None:
            raise credentials_exception
        token_data = schemas.TokenPayload(uuid=userid)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.uuid == token_data.uuid).first()

    # user = await User.find_one({"uuid": token_data.uuid})
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_manager(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_manager:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_developer(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_developer:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
