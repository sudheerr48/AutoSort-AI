"""
Document Classifier - Processing Configuration
Copyright (c) 2024 Document Classifier
Licensed under the MIT License (see LICENSE file for details)

Configuration settings for document processing parameters.
"""

# Document processing settings
document_processing = {
    # Maximum number of pages to read for classification
    "max_pages_to_read": 10,
    
    # Maximum characters per page to process
    "max_chars_per_page": 1000,
    
    # File size limits (in bytes)
    "max_file_size": 50 * 1024 * 1024,  # 50MB
    "min_file_size": 100,  # 100 bytes
    
    # Supported file types
    "supported_extensions": [".pdf"],
    
    # Processing timeout (in seconds)
    "processing_timeout": 30,
    
    # Whether to process password-protected PDFs
    "process_encrypted": False,
    
    # Text extraction settings
    "extract_images": False,
    "extract_tables": False,
    
    # Performance settings
    "batch_size": 10,  # Number of documents to process in parallel
    "use_threading": True
} 