from pydantic import BaseModel


class MessageSchema(BaseModel):
    role: str
    message: str
    user_id: str

    class Config:
        from_attributes = True
