from langchain_core.documents import Document
from app.embedding_engine.embedder import Embedder
from app.config import settings
from typing import Optional ,List
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever




class VecotrStoreService:
    """
    Manages persistent Chroma vector store creation, updates, and retriever creation.
    Uses Chroma.from_documents() for optimal batching and simplicity.
    """

    COLLECTION_NAME = "pdf_query_collection"

    def __init__(self,embedder:Optional[Embedder]=None):
        self.embedder = embedder or Embedder()
        self.persist_directory = str(settings.VECTOR_STORE_DIR)


    def build_from_documents(self,documents:List[Document])-> Chroma:
        vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=self.embedder.get_embedding_function(),
        persist_directory=self.persist_directory,
        collection_name=self.COLLECTION_NAME

    )
        return vectorstore



    def load_vector_store(self)->Chroma:

        return Chroma(
            embedding_function=self.embedder.get_embedding_function(),
            persist_directory=self.persist_directory,
            collection_name=self.COLLECTION_NAME
        )

    def get_retriever(self,top_k:int = settings.TOP_K_RESULTS)-> VectorStoreRetriever:
        """
        Returns a LangChain retriever ready to plug into any RAG chain.
        Supports search_type='similarity' or 'mmr' (Maximal Marginal Relevance).
        """

        vectorstore = self.load_vector_store()
        return vectorstore.as_retriever(
                search_type="similarity", # or "mmr", "similarity_score_threshold"
                search_kwargs={"k": top_k}

        )


    def reset(self)->None:
        """Deletes current collection to prepare for a new document upload."""
        try:
            vectorstore = self.load_vector_store()
            vectorstore.delete_collection()
        except Exception:
            raise RuntimeError(f"Unable to delete at this movment")

