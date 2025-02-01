"""
Document Classifier - Document Processor
Copyright (c) 2024 Document Classifier
Licensed under the MIT License (see LICENSE file for details)

Utility functions for processing PDF documents.
"""

import os
import logging
from typing import List, Tuple, Dict
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from pypdf.errors import PdfReadError

logger = logging.getLogger("document_classifier")

class DocumentProcessingError(Exception):
    """Custom exception for document processing errors."""
    pass

def load_pdfs_from_folder(folder_path: str) -> List[Tuple[str, str]]:
    """Load PDF documents from a specified folder.
    
    Args:
        folder_path (str): Path to the folder containing PDF files
        
    Returns:
        List of tuples containing (file_name, text_content)
    
    Raises:
        FileNotFoundError: If the folder doesn't exist
        DocumentProcessingError: If there are issues processing documents
    """
    documents = []
    failed_documents = []
    folder_path = Path(folder_path)
    
    logger.info(f"Starting to load PDFs from: {folder_path}")
    
    if not folder_path.exists():
        error_msg = f"Folder not found: {folder_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    pdf_files = list(folder_path.glob("*.pdf"))
    logger.info(f"Found {len(pdf_files)} PDF files")
    
    if not pdf_files:
        logger.warning("No PDF files found in the specified folder")
        return documents
    
    for pdf_file in pdf_files:
        try:
            logger.debug(f"Processing file: {pdf_file.name}")
            
            # Check if file is readable
            if not os.access(pdf_file, os.R_OK):
                raise PermissionError(f"No read permission for {pdf_file.name}")
            
            # Check file size
            file_size = pdf_file.stat().st_size
            if file_size == 0:
                raise DocumentProcessingError(f"File is empty: {pdf_file.name}")
            
            # Try to load and process the PDF
            loader = PyPDFLoader(str(pdf_file))
            pages = loader.load()
            
            if not pages:
                raise DocumentProcessingError(f"No content found in {pdf_file.name}")
                
            text = "\n".join([page.page_content for page in pages])
            
            if not text.strip():
                raise DocumentProcessingError(f"No text content found in {pdf_file.name}")
                
            documents.append((pdf_file.name, text))
            logger.debug(f"Successfully processed: {pdf_file.name}")
            
        except PdfReadError as e:
            error_msg = f"PDF reading error in {pdf_file.name}: {str(e)}"
            logger.error(error_msg)
            failed_documents.append((pdf_file.name, "PDF_READ_ERROR"))
        except PermissionError as e:
            error_msg = f"Permission error for {pdf_file.name}: {str(e)}"
            logger.error(error_msg)
            failed_documents.append((pdf_file.name, "PERMISSION_ERROR"))
        except DocumentProcessingError as e:
            error_msg = f"Processing error for {pdf_file.name}: {str(e)}"
            logger.error(error_msg)
            failed_documents.append((pdf_file.name, "PROCESSING_ERROR"))
        except Exception as e:
            error_msg = f"Unexpected error processing {pdf_file.name}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            failed_documents.append((pdf_file.name, "UNEXPECTED_ERROR"))
    
    # Log summary
    success_count = len(documents)
    fail_count = len(failed_documents)
    total_count = success_count + fail_count
    
    logger.info(f"Successfully processed {success_count} out of {total_count} documents")
    
    if failed_documents:
        logger.warning("Failed to process the following documents:")
        for doc, error_type in failed_documents:
            logger.warning(f"  - {doc}: {error_type}")
    
    return documents 