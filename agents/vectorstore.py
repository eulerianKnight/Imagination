import os
import uuid
from dotenv import load_dotenv
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import logging

load_dotenv()

# Create ChromaDB Client
chroma_client = chromadb.HttpClient(host=os.environ['CHROMA_DB_CLIENT'], port=os.environ['CHROMA_DB_PORT'])

# Function to Add documents to ChromaDB
def ingest_documents(collections: str, docs: list[str]):
    # Generate a list of 5 unique UUIDs
    unique_ids = [str(uuid.uuid4()) for _ in range(len(docs))]
    try:
        # Create Collection if not exists
        chroma_client.get_or_create_collection(name=collections)
        # Instantiate Vector Store
        vector_store = Chroma(
            client=chroma_client, 
            collection_name=collections, 
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
        )
        # Ingest Documents
        vector_store.add_documents(documents=docs, ids=unique_ids)
        return f"Documents Ingested Successful to Collections: {collections}"
    except Exception as e:
        return f"Error Ingesting Documents to ChromaDB in collections {collections}: {e}"
    
# Function to create retriever
def _retriever(collections: str):
    try:
        # Instantiate Vector Store
        vector_store = Chroma(
            client=chroma_client, 
            collection_name=collections, 
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
        )
        return vector_store.as_retriever()
    except Exception as e:
        logging.error(f"Error creating Retriever: {e}")
        return None