from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from models.user import User

from auth.auth import get_current_user

from utils.run_rasa import run_rasa


from sqlalchemy.orm import Session
from config.database import get_db_session
from config.config import OPENAI_ASSISTANT_ID

from pydantic import BaseModel

from models.user import Messages

from services.GPTService import (
    set_user_message,
    run_assistant,
    retrieve_run_assistant_status,
    retrieve_messages,
    text_to_speech,
)

import time

from services.MessageSevice import save_message

router = APIRouter()


class QuerySchema(BaseModel):
    query: str


# @router.post("/chat1", response_model=None)
# async def chat1(
#     query: QuerySchema,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db_session),
# ):
#     user_uuid = current_user.uuid

#     res = run_rasa(user_uuid=str(user_uuid), message=query.query)

#     if res == "_CHATGPT_":
#         thread_id = current_user.thread_id
#         message_obg = set_user_message(message=query.query, thread_id=thread_id)
#         runner = run_assistant(thread_id=thread_id, assistant_id=OPENAI_ASSISTANT_ID)
#         run_status = ""
#         while run_status != "completed":
#             run = retrieve_run_assistant_status(thread_id=thread_id, run_id=runner.id)
#             run_status = run.status
#             time.sleep(1)
#         messages = retrieve_messages(thread_id=thread_id)
#         if messages.data[0].role == "assistant":
#             message_content = messages.data[0].content[0].text.value
#             save_message(
#                 current_user=current_user,
#                 message=query.query,
#                 role="user",
#                 db=db,
#             )
#             save_message(
#                 current_user=current_user,
#                 message=message_content,
#                 role="assistant",
#                 db=db,
#             )
#             return {
#                 "user_msg": query.query,
#                 "adamo_msg": message_content,
#             }
#         else:
#             return {
#                 "user_msg": query.query,
#                 "adamo_msg": "Did not get message from Adamo",
#             }
#     else:
#         print(res)
#         # message_obg = set_assistant_message(
#         #     message=res, thread_id=current_user.thread_id
#         # )
#         save_message(
#             current_user=current_user,
#             message=query.query,
#             role="user",
#             db=db,
#         )
#         save_message(
#             current_user=current_user,
#             message=res,
#             role="assistant",
#             db=db,
#         )

#         return {"user_msg": query.query, "adamo_msg": res}


@router.post("/text_to_speech", response_model=None)
async def TTS(
    query: QuerySchema,
    current_user: User = Depends(get_current_user),
):
    res = text_to_speech(input=query.query)
    return res


@router.post("/chat", response_model=None)
async def chat(
    query: QuerySchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    try:
        user_uuid = current_user.uuid
        res = run_rasa(user_uuid=str(user_uuid), message=query.query)
        save_message(
            current_user=current_user,
            message=query.query,
            role="user",
            db=db,
        )
        save_message(
            current_user=current_user,
            message=res,
            role="assistant",
            db=db,
        )
        return {
            "user_msg": query.query,
            "adamo_msg": res,
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred from rasa server."
        )

# @router.post("/chat3", response_model=None)
# async def chat3(
#     query: QuerySchema,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db_session),
# ):
#     messages = db.query(Messages).filter(Messages.role == "assistant").first()
#     res = chatgpt(prompt=query.query, username=current_user.first_name, db=db)
#     if res.content is not "error":
#         pass
#     return res
