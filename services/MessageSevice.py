from fastapi import Depends
from schemas.messageSchema import MessageSchema
from models.user import Messages, User
from sqlalchemy.orm import Session


def save_message(current_user: User, message: str, role: str, db: Session):
    new_message = Messages(role=role, message=message, user_id=current_user.id)
    db.add(new_message)
    db.commit()
    return new_message
