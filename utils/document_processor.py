"""
Document Classifier - Document Processor
Copyright (c) 2024 Document Classifier
Licensed under the MIT License (see LICENSE file for details)

Utility functions for processing PDF documents.
"""

import os
import logging
from typing import List, Tuple
from pathlib import Path
from langchain.document_loaders import PyPDFLoader

logger = logging.getLogger("document_classifier")

def load_pdfs_from_folder(folder_path: str) -> List[Tuple[str, str]]:
    """Load PDF documents from a specified folder.
    
    Args:
        folder_path (str): Path to the folder containing PDF files
        
    Returns:
        List of tuples containing (file_name, text_content)
    """
    documents = []
    folder_path = Path(folder_path)
    
    logger.info(f"Starting to load PDFs from: {folder_path}")
    
    if not folder_path.exists():
        logger.error(f"Folder not found: {folder_path}")
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    pdf_files = list(folder_path.glob("*.pdf"))
    logger.info(f"Found {len(pdf_files)} PDF files")
    
    for pdf_file in pdf_files:
        try:
            logger.debug(f"Processing file: {pdf_file.name}")
            loader = PyPDFLoader(str(pdf_file))
            pages = loader.load()
            text = "\n".join([page.page_content for page in pages])
            documents.append((pdf_file.name, text))
            logger.debug(f"Successfully processed: {pdf_file.name}")
        except Exception as e:
            logger.error(f"Error processing {pdf_file.name}: {str(e)}", exc_info=True)
    
    logger.info(f"Successfully loaded {len(documents)} documents")
    return documents 