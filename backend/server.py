from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import ChatCompletionBody, SimpleResponse

from .resources.KnowledgeBaseAgent import KnowledgeBaseAgent

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat/completion", response_model=SimpleResponse)
def create_chat_completion(body: ChatCompletionBody):
    response = KnowledgeBaseAgent.run(
        body.message,
    )
    return {"detail": response.content}
