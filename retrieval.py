import chromadb

def store_chunks_in_chroma(chunks_with_embeddings, collection_name="rag_documents"):
    client = chromadb.Client()
    collection = client.create_collection(collection_name)

    for idx, (embedding, metadata) in enumerate(chunks_with_embeddings):
        collection.add(
            embeddings=[embedding],
            documents=[f"chunk_{idx}"],
            metadatas=[metadata]
        )

    print(f"Stored {len(chunks_with_embeddings)} chunks in ChromaDB.")
    return collection


def retrieve_documents(query_embedding, collection, top_k=5):
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    documents = results['documents']
    metadata = results['metadatas']

    return documents, metadata
