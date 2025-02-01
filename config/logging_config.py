"""
Document Classifier - Logging Configuration
Copyright (c) 2024 Document Classifier
Licensed under the MIT License (see LICENSE file for details)

Logging configuration for the document classifier application.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logging(
    log_dir: str = "logs",
    keep_all: bool = True
) -> logging.Logger:
    """Configure logging for the application.
    
    Args:
        log_dir (str): Directory for log files
        keep_all (bool): If True, creates new log file for each run
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("document_classifier")
    logger.setLevel(logging.DEBUG)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # Generate unique log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"document_classifier_{timestamp}.log"
    
    # File handler
    file_handler = logging.FileHandler(
        log_path / log_file,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Remove any existing handlers
    logger.handlers = []
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Create a symlink to latest log file
    latest_symlink = log_path / "latest.log"
    if latest_symlink.exists():
        latest_symlink.unlink()
    latest_symlink.symlink_to(log_file)
    
    logger.info(f"Logging initialized: {log_path / log_file}")
    return logger 