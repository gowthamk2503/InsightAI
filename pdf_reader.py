"""PDF Reader Module

This module extracts text from PDF files using PyPDF2.
"""

import PyPDF2


class PDFReader:
    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text from a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Extracted text as a string.
        """
        try:
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
