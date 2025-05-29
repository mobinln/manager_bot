from typing import List
from pydantic import BaseModel


class Message(BaseModel):
    message: str
    assistant_response: str


class ChatCompletionBody(BaseModel):
    message: str
    history: List[Message]


class SimpleResponse(BaseModel):
    detail: str
