# 📄 PDFQuery - PDF Q&A Tool

A modern, production-grade Retrieval-Augmented Generation (RAG) tool built with **LangChain**, **ChromaDB**, and **Streamlit**. Upload any PDF document and ask contextual questions to receive answers grounded strictly in the document content, complete with source citations and page numbers.

---

## ✨ Features

- **Document Parsing & Chunking**: Extracts text from PDFs using `PyPDFLoader` and splits documents into optimal chunks using `RecursiveCharacterTextSplitter`.
- **Vector Search & Persistence**: Uses `Chroma` for vector storage and retrieval with persistent local storage.
- **Modern RAG Architecture**: Uses LangChain's retrieval pipelines (`create_stuff_documents_chain` & `create_retrieval_chain`).
- **Hallucination Guardrails**: Prompts ensure answers are derived strictly from the retrieved document context.
- **Interactive Streamlit UI**:
  - Drag-and-drop PDF upload with indexing status.
  - Multi-turn conversational chat interface.
  - Expandable source citation cards with page numbers and snippet previews.
- **Configurable Settings**: Managed via `pydantic-settings` and `.env`.

---

## 🏗️ Project Architecture

```
PDFQuery---PDF-Q-A-Tool/
├── app.py                          # Application entry point
├── pyproject.toml                  # Project packaging configuration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── data/
│   ├── uploads/                    # Uploaded PDF storage
│   └── vector_store/               # ChromaDB persistence directory
└── app/
    ├── __init__.py
    ├── config.py                   # Centralized Pydantic settings & directories
    ├── pdf_processor/
    │   ├── __init__.py
    │   └── loader.py               # PDF loading and validation
    ├── embedding_engine/
    │   ├── __init__.py
    │   └── embedder.py             # Document chunking & embedding logic
    ├── vector_store/
    │   ├── __init__.py
    │   └── store.py                # Chroma vector store management & retriever
    ├── qa_generator/
    │   ├── __init__.py
    │   └── rag_chain.py            # RAG question answering pipeline
    └── ui/
        ├── __init__.py
        └── app.py                  # Streamlit user interface
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.11 or 3.12
- An API key for an OpenAI-compatible endpoint (e.g. OpenAI or AICredits)

### 2. Clone Repository & Setup Virtual Environment

```bash
git clone <repository-url>
cd PDFQuery---PDF-Q-A-Tool
```

Create and activate a virtual environment:

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Using `pip`:
```bash
pip install -r requirements.txt
```

Or using `uv`:
```bash
uv pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# API Credentials (OpenAI or AICredits)
AICREDITS_API_KEY=your_api_key_here
AICREDITS_BASE_URL=https://aicredits.in/v1

# Models
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.1

# Chunking Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Retrieval
TOP_K_RESULTS=4
```

---

## 🖥️ Running the Application

Launch the Streamlit app:

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser:
1. Upload a `.pdf` file in the sidebar.
2. Click **Process Document**.
3. Ask questions in the chat box!

---

## 🧪 Testing

Run automated tests with pytest:

```bash
pytest
```

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **RAG & Orchestration**: [LangChain](https://www.langchain.com/) / `langchain-classic`
- **Embeddings & LLM**: OpenAI API / Compatible endpoints
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **PDF Processing**: [pypdf](https://pypdf.readthedocs.io/)
- **Configuration**: [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.