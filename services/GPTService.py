import os
from openai import OpenAI

from config.config import OPENAI_API_KEY

from utils.utils import convertText2AudioBase64

client = OpenAI(api_key=OPENAI_API_KEY)


def create_thread():
    thread = client.beta.threads.create()
    return thread


def set_user_message(message: str, thread_id: str):
    message_obj = client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=message
    )
    return message_obj


def set_assistant_message(message: str, thread_id: str):
    message_obj = client.beta.threads.messages.create(
        thread_id=thread_id, role="assistant", content=message
    )

    return message_obj


def run_assistant(thread_id: str, assistant_id: str):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="",
    )
    return run


def retrieve_run_assistant_status(thread_id: str, run_id: str):
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run


def retrieve_messages(thread_id: str):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages


def text_to_speech(input: str):
    response = client.audio.speech.create(model="tts-1", voice="alloy", input=input)
    base64_str = convertText2AudioBase64(text=response.content)

    return base64_str
