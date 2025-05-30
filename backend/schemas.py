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

class TrelloCard(BaseModel):
    comments: int   
    commentDescription: bool
    due: str|None                 
    start: str|None               
    dueReminder: str|None         
    dueComplete:bool         
    email: str|None               
    listName: str              
    name:str                
    desc:str                
    dateLastActivity: str|None    
    closed:bool              
