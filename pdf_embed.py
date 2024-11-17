import chromadb 
from langchain_community.embeddings import HuggingFaceEmbeddings
from pdf_loader import Pdf_Reader
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize ChromaDB client with the new configuration
#client = chromadb.Client(
#    chromadb.config.Settings(
#        persist_directory="persistent_doc"
#    )
#)

client = chromadb.PersistentClient(path=r'persistent_doc')

# Create or retrieve the collection
collection = client.get_or_create_collection(name="files")

# Load SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Read PDF and preprocess the documents
documents = Pdf_Reader(r"Grammar Rules _ Speak Good English Movement.pdf")
documents = [str(doc) if not isinstance(doc, str) else doc for doc in documents]

# Generate embeddings
embeddings = model.encode(documents, convert_to_numpy=True)

# Generate unique document IDs
ids = [f'doc_{i}' for i in range(len(documents))]

# Add documents and their embeddings to the collection
collection.add(
    documents=documents,
    ids=ids,
    embeddings=embeddings
)

