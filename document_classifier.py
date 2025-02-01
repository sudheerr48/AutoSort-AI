import os
from typing import List, Dict, Tuple
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader

from config.categories import document_categories
from utils.document_processor import load_pdfs_from_folder

class DocumentClassifier:
    def __init__(self, model_name: str = "mistral"):
        """Initialize the document classifier with specified LLM model.
        
        Args:
            model_name (str): Name of the Ollama model to use. Defaults to "mistral".
        """
        self.llm = Ollama(model=model_name)
        self.chain = self._setup_chain()

    def _setup_chain(self) -> LLMChain:
        """Set up the classification chain with prompt template."""
        template = """
        You are an AI assistant trained to classify documents into specific categories.
        The available categories and subcategories are:

        {categories}

        Given the following document content, classify it into the most appropriate subcategory only.
        Provide just the subcategory name without any explanation:

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
        results = []
        categories_formatted = "\n".join([
            f"{main_category}: {', '.join(subcategories)}"
            for main_category, subcategories in document_categories.items()
        ])

        for file_name, text in documents:
            # Limit text to 1000 chars to avoid token limits
            response = self.chain.run(
                categories=categories_formatted, 
                document_text=text[:1000]
            )
            results.append({
                "file_name": file_name, 
                "subcategory": response.strip()
            })
        return results

def main():
    # Configure folder path
    folder_path = os.getenv('DOCUMENTS_PATH', './documents')
    
    # Initialize classifier
    classifier = DocumentClassifier()
    
    # Load and classify documents
    documents = load_pdfs_from_folder(folder_path)
    classified_docs = classifier.classify_documents(documents)
    
    # Print results
    for doc in classified_docs:
        print(f"{doc['file_name']} -> {doc['subcategory']}")

if __name__ == "__main__":
    main() 