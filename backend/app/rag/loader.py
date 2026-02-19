import os
from langchain_community.document_loaders import PyPDFDirectoryLoader

def load_policy_documents():
    base_path = "app/policies"
    
    # Check if the directory exists to avoid errors
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    # PyPDFDirectoryLoader dynamically loads all PDFs in the folder
    loader = PyPDFDirectoryLoader(base_path)
    docs = loader.load()
    
    return docs