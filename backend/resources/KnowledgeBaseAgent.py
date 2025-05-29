import os
from agno.agent import Agent
from agno.knowledge.pdf import PDFReader, PDFKnowledgeBase
from agno.vectordb.chroma import ChromaDb
from agno.models.openai.like import OpenAILike
from agno.storage.json import JsonStorage

from agno.embedder.openai import OpenAIEmbedder
from agno.embedder.sentence_transformer import SentenceTransformerEmbedder

import dotenv

dotenv.load_dotenv()

vector_db = ChromaDb(
    collection="documents",
    embedder=OpenAIEmbedder(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("METIS_OPENAI_BASE"),
    ),
    # embedder=SentenceTransformerEmbedder(),
)
knowledge_base = PDFKnowledgeBase(
    path="/home/larijanian/Documents/hackathon/manager_bot/backend/resources/data",
    vector_db=vector_db,
    reader=PDFReader(chunk=True),
)

KnowledgeBaseAgent = Agent(
    model=OpenAILike(
        id="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("METIS_OPENAI_BASE"),
    ),
    storage=JsonStorage(dir_path="tmp/agent_sessions_json"),
    knowledge=knowledge_base,
    show_tool_calls=True,
    debug_mode=True,
)

knowledge_base.load()
