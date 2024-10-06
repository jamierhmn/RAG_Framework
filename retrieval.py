
def retrieve_documents(query_embedding, collection, top_k=2):
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    # Retrieve documents and metadata from the results
    documents = results['documents']  # These should contain the actual content
    metadata = results['metadatas']

    return documents, metadata