import PyPDF2
from PIL import Image
import pytesseract
import os

class FileProcessor:
    """Handle extraction of text from various file formats"""
    
    def process_file(self, filepath):
        """Process file based on its extension"""
        file_ext = os.path.splitext(filepath)[1].lower()
        
        if file_ext == '.pdf':
            return self.extract_from_pdf(filepath)
        elif file_ext in ['.png', '.jpg', '.jpeg']:
            return self.extract_from_image(filepath)
        elif file_ext == '.txt':
            return self.extract_from_text(filepath)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def extract_from_pdf(self, filepath):
        """Extract text from PDF files"""
        text = ""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error extracting from PDF: {str(e)}")
    
    def extract_from_image(self, filepath):
        """Extract text from images using OCR"""
        try:
            image = Image.open(filepath)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            raise Exception(f"Error extracting from image: {str(e)}")
    
    def extract_from_text(self, filepath):
        """Extract text from text files"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except Exception as e:
            raise Exception(f"Error extracting from text file: {str(e)}")