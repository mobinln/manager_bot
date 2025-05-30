import os
from agno.agent import Agent
from agno.knowledge.pdf import PDFReader, PDFKnowledgeBase
from agno.vectordb.chroma import ChromaDb
from agno.models.openai import OpenAIChat
from agno.models.openai.like import OpenAILike
from agno.storage.sqlite import SqliteStorage
from agno.app.fastapi.app import FastAPIApp
from agno.app.fastapi.serve import serve_fastapi_app
from fastapi.middleware.cors import CORSMiddleware

from agno.embedder.openai import OpenAIEmbedder
from agno.embedder.sentence_transformer import SentenceTransformerEmbedder

from .trello import trello_search, get_trello_list_names
from .gitlab import get_git_merge_requests, get_git_merge_request_comments
import dotenv

dotenv.load_dotenv()

vector_db = ChromaDb(
    collection="documents",
    embedder=OpenAIEmbedder(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("METIS_OPENAI_BASE"),
    ),
    path=os.getcwd() + "/chromadb",
    # embedder=SentenceTransformerEmbedder(),
)

knowledge_base = PDFKnowledgeBase(
    path=os.getcwd() + "/backend/resources/data",
    vector_db=vector_db,
    reader=PDFReader(chunk=True),
)
knowledge_base.load()


basic_agent = Agent(
    name="Basic Agent",
    model=OpenAIChat(
        id="gpt-4o",
        base_url=os.getenv("METIS_OPENAI_BASE"),
    ),  # Ensure OPENAI_API_KEY is set
    storage=SqliteStorage(table_name="agent_sessions", db_file="./data.db"),
    add_history_to_messages=True,
    num_history_responses=3,
    add_datetime_to_instructions=True,
    markdown=True,
    knowledge=knowledge_base,
    show_tool_calls=True,
    debug_mode=True,
    tools=[
        trello_search,
        get_trello_list_names,
        get_git_merge_requests,
        get_git_merge_request_comments,
    ],
)

app = FastAPIApp(agent=basic_agent).get_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    serve_fastapi_app("agent_api:app", port=8001, reload=True)
