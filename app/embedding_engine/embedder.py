from typing import List
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings


class Embedder:
    """
    Handles document chunking and OpenAI-compatible embeddings.
    """

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.AICREDITS_API_KEY,
            base_url=settings.AICREDITS_BASE_URL
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Splits documents into chunks."""
        return self.splitter.split_documents(documents)

    def get_embedding_function(self) -> OpenAIEmbeddings:
        """Returns the embedding instance for vector store operations."""
        return self.embeddings
