"""
Main launcher script for PDFQuery application.
To run:
    streamlit run app.py
"""
from app.ui.app import PDFQueryApp

if __name__ == "__main__":
    app = PDFQueryApp()
    app.run()
