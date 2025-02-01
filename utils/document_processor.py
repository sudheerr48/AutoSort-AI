import os
from typing import List, Tuple
from langchain.document_loaders import PyPDFLoader

def load_pdfs_from_folder(folder_path: str) -> List[Tuple[str, str]]:
    """Load PDF documents from a specified folder.
    
    Args:
        folder_path (str): Path to the folder containing PDF files
        
    Returns:
        List of tuples containing (file_name, text_content)
    """
    documents = []
    
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")
        
    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            try:
                file_path = os.path.join(folder_path, file)
                loader = PyPDFLoader(file_path)
                pages = loader.load()
                text = "\n".join([page.page_content for page in pages])
                documents.append((file, text))
            except Exception as e:
                print(f"Error loading {file}: {str(e)}")
                
    return documents 