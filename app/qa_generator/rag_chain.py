from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever


from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

from app.config import settings


class RAGPipeline:
    """
    Modern LangChain RAG pipeline using pre-built chains:
    - create_stuff_documents_chain: Handles document stuffing into prompt internally (no format_docs needed).
    - create_retrieval_chain: Coordinates retrieval and question answering, returning both
      the synthesized 'answer' and retrieved 'context' documents.
    """

    def __init__(self, retriever: VectorStoreRetriever):
        self.retriever = retriever

        # 1. LLM Client
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            api_key=settings.AICREDITS_API_KEY,
            base_url=settings.AICREDITS_BASE_URL
        )

        # 2. QA Prompt Template
        # Note: create_stuff_documents_chain expects {context} and {input}
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an expert Q&A assistant analyzing a PDF document.\n"
                "Answer the user's question accurately, concisely, and factually using ONLY the provided context.\n"
                "When possible, reference the page number or source.\n"
                "If the context does not contain enough information, reply: "
                "'I cannot find the answer in the provided document.' Do not hallucinate.\n\n"
                "Context:\n{context}"
            ),
            (
                "human",
                "{input}"
            )
        ])

        # 3. Pre-built Chains (no format_docs required)
        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, self.question_answer_chain)

    def query(self, question: str) -> Dict[str, Any]:
        """
        Executes query.
        Returns:
            {
                "answer": "Synthesized text...",
                "sources": [Document, Document, ...]
            }
        """
        response = self.rag_chain.invoke({"input": question})
        return {
            "answer": response["answer"],
            "sources": response["context"]
        }
