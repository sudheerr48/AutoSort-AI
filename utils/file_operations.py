"""
Document Classifier - File Operations
Copyright (c) 2024 Document Classifier
Licensed under the MIT License (see LICENSE file for details)

Utility functions for file operations and category management.
"""

import shutil
from pathlib import Path
import logging
from typing import Dict

logger = logging.getLogger("document_classifier")

def sanitize_path(path_str: str) -> str:
    """Sanitize the path string to be valid for all operating systems."""
    # Remove or replace invalid characters
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    result = path_str
    for char in invalid_chars:
        result = result.replace(char, '_')
    # Remove leading/trailing spaces and dots
    result = result.strip('. ')
    return result

def create_category_folders(base_output_dir: str) -> Path:
    """Create the base output directory structure.
    
    Args:
        base_output_dir (str): Base path for output directory
        
    Returns:
        Path: Path object of created base directory
    """
    output_path = Path(base_output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created/verified output directory at: {output_path}")
    return output_path

def move_document_to_category(
    file_path: Path,
    category: str,
    output_base_dir: Path
) -> bool:
    """Move a document to its classified category folder.
    
    Args:
        file_path (Path): Source file path
        category (str): Classified category/subcategory
        output_base_dir (Path): Base output directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Clean up category name and create proper path structure
        category = category.replace(" > ", "/").replace(">", "/")
        category_parts = [sanitize_path(part.strip()) for part in category.split("/")]
        
        # Create category path
        category_path = output_base_dir
        for part in category_parts:
            category_path = category_path / part
            category_path.mkdir(parents=True, exist_ok=True)
        
        # Create destination path
        dest_path = category_path / file_path.name
        
        # Handle duplicate filenames
        counter = 1
        original_stem = dest_path.stem
        while dest_path.exists():
            new_name = f"{original_stem}_{counter}{dest_path.suffix}"
            dest_path = category_path / new_name
            counter += 1
        
        # Copy the file
        shutil.copy2(file_path, dest_path)
        logger.info(f"Moved {file_path.name} to {dest_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error moving file {file_path}: {str(e)}", exc_info=True)
        return False 