from ingestion import ingest_and_chunk_pdfs
from embeddings import generate_chunk_embeddings
#from retrieval import store_chunks_in_chroma
import chromadb
from chromadb import Client
from chromadb.config import Settings


client = chromadb.Client()

def store_chunks_in_chroma(chunks_with_embeddings, collection_name="rag_documents"):
   # client = chromadb.Client()
    collection = client.create_collection(collection_name)

    for idx, (embedding, metadata) in enumerate(chunks_with_embeddings):
        collection.add(
            ids=[f"chunk_{idx}"],  # Unique identifier for each chunk
            embeddings=[embedding],  # Add the embedding for this chunk
            documents=[metadata.get("content")],  # Store the actual chunk content
            metadatas=[metadata]  # Add metadata for this chunk
        )
    print(f"Stored {len(chunks_with_embeddings)} chunks in ChromaDB.")
    return collection

def initialize_database(pdf_folder):
    """
    Ingest PDF documents, generate chunk embeddings, and store them in ChromaDB.
    """
    chunks_with_metadata = ingest_and_chunk_pdfs(pdf_folder)
    chunk_embeddings = generate_chunk_embeddings(chunks_with_metadata)
    collection = store_chunks_in_chroma(chunk_embeddings)
    print(f"Data initialized and stored in ChromaDB from folder: {pdf_folder}")
    return collection

if __name__ == '__main__':
    # You can specify the PDF folder here
    pdf_folder = "C://finance"  # Ensure compatibility for the file path
    initialize_database(pdf_folder)
    # Keep Chroma running (or you can run it as a server using uvicorn below)
    print("Chroma DB is running...")
    #client.persist()
    collections = client.list_collections()
    print(collections)
    # Print collection names
    for collection in collections:
        print(f"Collection Name: {collection.name}")
