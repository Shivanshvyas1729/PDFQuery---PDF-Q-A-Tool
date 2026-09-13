from app.config import settings
from app.pdf_processor.loader import PDFLoader
from app.embedding_engine.embedder import Embedder 
from app.vector_store.store import VectorStoreService
from app.qa_generator.rag_chain import RAGPipeline
import streamlit as st
class PDFQueryApp:

    """"Streamlit frontend for the pdfQuery RAG tool"""

    def __init__(self):
        self.embedder = Embedder()
        self.vector_service = VectorStoreService()


    def process_pdf(self,uploaded_file)->None:
        """Handles pdf ingestion: Load-> split-> embed & persist into chroma"""
        temp_file_path = settings.UPLOADS_DIR / uploaded_file.name
        with st.spinner("Step 1/3: Saving uploaded PDF..."):
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        try:
            with st.spinner("Step 2/3: Extracting text from PDF pages..."):
                loader = PDFLoader(temp_file_path)
                documents = loader.load()

            with st.spinner("Step 3/3: Chunking text and creating vector embeddings..."):
                    chunks = self.embedder.split_documents(documents)

                    self.vector_service.reset()
                    self.vector_service.build_from_documents(chunks)

            # Update session state
            st.session_state["pdf_loaded"] = True
            st.session_state["pdf_name"] = uploaded_file.name
            st.session_state["total_pages"] = len(documents)
            st.session_state["total_chunks"] = len(chunks)
            st.session_state["chat_history"] = []

            st.sidebar.success(
                f"✅ Ready! Indexed {len(chunks)} chunks from {len(documents)} pages."
            )

        except Exception as e:
            st.sidebar.error(f"Failed to process PDF: {str(e)}")


    def run(self) -> None:
        """Renders the Streamlit application layout and chat loop."""
        st.set_page_config(
            page_title="PDFQuery - RAG Q&A",
            page_icon="📄",
            layout="wide"
        )

        st.title("📄 PDFQuery - PDF Q&A Tool")
        st.caption("Ask questions directly from your PDF using modern LangChain RAG & Chroma")

        # Session state initialization
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        if "pdf_loaded" not in st.session_state:
            st.session_state["pdf_loaded"] = False

        # Sidebar: File Upload & Status
        with st.sidebar:
            st.header("Upload Document")
            uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

            if uploaded_file and st.button("Process Document", type="primary"):
                self.process_pdf(uploaded_file)

            if st.session_state["pdf_loaded"]:
                st.divider()
                st.subheader("Document Stats")
                st.write(f"📁 **File:** `{st.session_state.get('pdf_name')}`")
                st.write(f"📃 **Pages:** {st.session_state.get('total_pages')}")
                st.write(f"🧩 **Chunks:** {st.session_state.get('total_chunks')}")

        # Main Chat Area
        if not st.session_state["pdf_loaded"]:
            st.info("👈 Upload and process a PDF from the sidebar to start asking questions.")
            return

        # Display conversation history
        for message in st.session_state["chat_history"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message.get("sources"):
                    with st.expander("📚 View Cited Sources"):
                        for idx, doc in enumerate(message["sources"], start=1):
                            page_num = doc.get("page", "Unknown")
                            st.markdown(f"**Source {idx} (Page {page_num}):**")
                            st.caption(doc.get("text", ""))

        # Chat Input
        if user_query := st.chat_input("Ask a question about your PDF..."):
            # Display user question immediately
            st.session_state["chat_history"].append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            # Generate RAG response
            with st.chat_message("assistant"):
                with st.spinner("Searching document & synthesizing answer..."):
                    try:
                        retriever = self.vector_service.get_retriever()
                        pipeline = RAGPipeline(retriever=retriever)
                        result = pipeline.query(user_query)

                        answer = result["answer"]
                        sources = result["sources"]

                        st.markdown(answer)

                        # Render source cards with exact page numbers
                        serialized_sources = []
                        if sources:
                            with st.expander("📚 View Cited Sources"):
                                for idx, doc in enumerate(sources, start=1):
                                    page = doc.metadata.get("page", 0) + 1
                                    text_preview = doc.page_content
                                    st.markdown(f"**Source {idx} (Page {page}):**")
                                    st.caption(text_preview)
                                    serialized_sources.append({
                                        "page": page,
                                        "text": text_preview
                                    })

                        # Save assistant response to history
                        st.session_state["chat_history"].append({
                            "role": "assistant",
                            "content": answer,
                            "sources": serialized_sources
                        })

                    except Exception as e:
                        st.error(f"Error answering question: {str(e)}")
