"""
Document Classifier
Copyright (c) 2024 Document Classifier
Licensed under the MIT License (see LICENSE file for details)

A professional document classification system that automatically categorizes
PDF documents into predefined categories using LLMs.
"""

import os
import logging
from typing import List, Dict, Tuple
from pathlib import Path
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader

from config.categories import document_categories
from config.logging_config import setup_logging
from utils.document_processor import load_pdfs_from_folder
from utils.file_operations import create_category_folders, move_document_to_category

logger = logging.getLogger("document_classifier")

class DocumentClassifier:
    def __init__(self, model_name: str = "mistral"):
        """Initialize the document classifier with specified LLM model.
        
        Args:
            model_name (str): Name of the Ollama model to use. Defaults to "mistral".
        """
        logger.info(f"Initializing DocumentClassifier with model: {model_name}")
        try:
            self.llm = Ollama(model=model_name)
            self.chain = self._setup_chain()
            logger.info("Successfully initialized DocumentClassifier")
        except Exception as e:
            logger.error(f"Failed to initialize DocumentClassifier: {str(e)}", exc_info=True)
            raise

    def _setup_chain(self) -> LLMChain:
        """Set up the classification chain with prompt template."""
        logger.debug("Setting up classification chain")
        template = """
        You are an AI assistant trained to classify documents into specific categories.
        The available categories and subcategories are:

        {categories}

        Given the following document content, classify it into the most appropriate category.
        Use the exact category name from the list above.
        If it fits into both a main category and subcategory, use the format: "MainCategory > Subcategory"
        Provide just the category without any explanation.

        Document content:
        {document_text}
        """

        prompt = PromptTemplate(
            input_variables=["categories", "document_text"],
            template=template
        )
        return LLMChain(llm=self.llm, prompt=prompt)

    def classify_documents(self, documents: List[Tuple[str, str]]) -> List[Dict[str, str]]:
        """Classify a list of documents into predefined categories.
        
        Args:
            documents: List of tuples containing (file_name, text_content)
            
        Returns:
            List of dictionaries containing classification results
        """
        logger.info(f"Starting classification of {len(documents)} documents")
        results = []
        categories_formatted = "\n".join([
            f"{main_category}: {', '.join(subcategories)}"
            for main_category, subcategories in document_categories.items()
        ])

        for file_name, text in documents:
            try:
                logger.debug(f"Classifying document: {file_name}")
                # Limit text to 1000 chars to avoid token limits
                response = self.chain.run(
                    categories=categories_formatted, 
                    document_text=text[:1000]
                )
                results.append({
                    "file_name": file_name, 
                    "subcategory": response.strip()
                })
                logger.debug(f"Classified {file_name} as: {response.strip()}")
            except Exception as e:
                logger.error(f"Error classifying {file_name}: {str(e)}", exc_info=True)
                results.append({
                    "file_name": file_name,
                    "subcategory": "ERROR: Classification failed"
                })

        logger.info(f"Completed classification of {len(documents)} documents")
        return results

    def classify_and_organize_documents(
        self,
        documents: List[Tuple[str, str]],
        input_dir: Path,
        output_dir: Path,
        create_backups: bool = True
    ) -> List[Dict[str, str]]:
        """Classify documents and organize them into category folders.
        
        Args:
            documents: List of tuples containing (file_name, text_content)
            input_dir: Directory containing source documents
            output_dir: Base directory for organized output
            create_backups: Whether to create backups before moving files
            
        Returns:
            List of dictionaries containing classification results
        """
        if not documents:
            logger.warning("No documents provided for classification")
            return []

        # First classify all documents
        classified_docs = self.classify_documents(documents)
        
        # Create output directory
        try:
            output_base = create_category_folders(output_dir)
        except Exception as e:
            logger.error(f"Failed to create output directory structure: {str(e)}")
            return classified_docs
        
        # Move files to their respective categories
        for doc in classified_docs:
            file_name = doc['file_name']
            category = doc['subcategory']
            
            if category.startswith("ERROR:"):
                logger.warning(f"Skipping file organization for {file_name} due to classification error")
                doc['status'] = "CLASSIFICATION_FAILED"
                doc['error_message'] = category
                continue
                
            source_path = Path(input_dir) / file_name
            if not source_path.exists():
                logger.error(f"Source file not found: {source_path}")
                doc['status'] = "FILE_NOT_FOUND"
                continue
                
            if move_document_to_category(source_path, category, output_base, create_backups):
                doc['status'] = "SUCCESS"
                doc['new_location'] = str(output_base / category / file_name)
            else:
                doc['status'] = "MOVE_FAILED"
                doc['error_message'] = "Failed to move file to category folder"
        
        # Print summary
        self._print_classification_summary(classified_docs)
        
        return classified_docs

    def _print_classification_summary(self, results: List[Dict[str, str]]) -> None:
        """Print a summary of the classification results."""
        total = len(results)
        successful = sum(1 for doc in results if doc.get('status') == "SUCCESS")
        failed = total - successful
        
        logger.info("\nClassification Summary:")
        logger.info(f"Total documents processed: {total}")
        logger.info(f"Successfully classified and moved: {successful}")
        logger.info(f"Failed: {failed}")
        
        if failed > 0:
            logger.info("\nFailed Documents:")
            for doc in results:
                if doc.get('status') != "SUCCESS":
                    logger.info(f"  - {doc['file_name']}")
                    logger.info(f"    Status: {doc.get('status')}")
                    if 'error_message' in doc:
                        logger.info(f"    Error: {doc['error_message']}")

def main():
    # Set up logging
    logger = setup_logging()
    
    try:
        # Configure paths
        input_folder = Path(os.getenv('DOCUMENTS_PATH', './documents'))
        output_folder = Path(os.getenv('OUTPUT_PATH', './classified_documents'))
        
        logger.info(f"Using input path: {input_folder}")
        logger.info(f"Using output path: {output_folder}")
        
        # Initialize classifier
        classifier = DocumentClassifier()
        
        # Load and classify documents
        documents = load_pdfs_from_folder(input_folder)
        classified_docs = classifier.classify_and_organize_documents(
            documents,
            input_folder,
            output_folder
        )
        
        # Print results
        logger.info("Classification and Organization Results:")
        for doc in classified_docs:
            print(f"{doc['file_name']} -> {doc['subcategory']}")
            if 'new_location' in doc:
                print(f"  Moved to: {doc['new_location']}")
            print("---")
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main() 