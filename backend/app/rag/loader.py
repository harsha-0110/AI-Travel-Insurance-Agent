from langchain_community.document_loaders import TextLoader
import os

def load_policy_documents():

    docs = []
    base_path = "app/policies"

    for file in os.listdir(base_path):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(base_path, file))
            docs.extend(loader.load())

    return docs
