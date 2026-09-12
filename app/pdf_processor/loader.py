from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

class PDFLoader:
    def __init__(self , file_path:Path|str):
        self.file_path  = Path(file_path) 
        if not self.file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {self.file_path}")
        if self.file_path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a pdf file , got : {file_path}")

        

    def load(self)->list[Document]:
        loader  = PyPDFLoader(file_path= str(self.file_path))
        documents = loader.load()
        cleaned_docs = [doc for doc in documents if doc.page_content and doc.page_content.strip()]
        if not cleaned_docs:
            raise ValueError(f"No extractable text found in PDF: {self.file_path.name}")
        return cleaned_docs 
