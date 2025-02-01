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
        # Split category into main and sub if present
        category_parts = [part.strip() for part in category.split('>')]
        if len(category_parts) == 2:
            main_category, subcategory = category_parts
        else:
            main_category = subcategory = category_parts[0]
            
        # Create category directories
        category_dir = output_base_dir / main_category / subcategory
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Create destination path
        dest_path = category_dir / file_path.name
        
        # Handle duplicate filenames
        counter = 1
        while dest_path.exists():
            new_name = f"{file_path.stem}_{counter}{file_path.suffix}"
            dest_path = category_dir / new_name
            counter += 1
        
        # Move the file
        shutil.copy2(file_path, dest_path)
        logger.info(f"Moved {file_path.name} to {dest_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error moving file {file_path}: {str(e)}", exc_info=True)
        return False 