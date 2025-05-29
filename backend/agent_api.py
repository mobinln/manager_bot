import os
from agno.agent import Agent
from agno.app.fastapi.app import FastAPIApp
from agno.app.fastapi.serve import serve_fastapi_app
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.knowledge.document import DocumentKnowledgeBase
from agno.vectordb.chroma import ChromaDb
from agno.embedder.sentence_transformer import SentenceTransformerEmbedder

import dotenv

dotenv.load_dotenv()

knowledge_base = DocumentKnowledgeBase(
    documents=[],
    vector_db=ChromaDb(
        collection="documents",
        path="./chromadb",
        persistent_client=True,
        embedder=SentenceTransformerEmbedder(),
    ),
)
knowledge_base.load()

basic_agent = Agent(
    name="Basic Agent",
    model=OpenAIChat(
        id="gpt-4o-mini", base_url=os.getenv("OPENAI_API_BASE")
    ),  # Ensure OPENAI_API_KEY is set
    storage=SqliteStorage(table_name="agent_sessions", db_file="./data.db"),
    add_history_to_messages=True,
    num_history_responses=3,
    add_datetime_to_instructions=True,
    markdown=True,
    knowledge=knowledge_base,
    show_tool_calls=True,
    debug_mode=True,
)

app = FastAPIApp(agent=basic_agent).get_app()

if __name__ == "__main__":
    print(basic_agent.get_session_data())
    serve_fastapi_app("main:app", port=8001, reload=True)
