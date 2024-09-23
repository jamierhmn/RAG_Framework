from flask import Flask, request, jsonify
from ingestion import ingest_and_chunk_pdfs
from embeddings import generate_chunk_embeddings, EmbeddingGenerator
from retrieval import store_chunks_in_chroma, retrieve_documents
from response_generation import QueryResponseGenerator
from query_optimization import generate_query_embedding

app = Flask(__name__)

# Initialize embedding generator and response generator
embedder = EmbeddingGenerator()
response_generator = QueryResponseGenerator()

# Store pre-processed chunks in ChromaDB
def initialize_database(pdf_folder):
    chunks_with_metadata = ingest_and_chunk_pdfs(pdf_folder)
    chunk_embeddings = generate_chunk_embeddings(chunks_with_metadata)
    collection = store_chunks_in_chroma(chunk_embeddings)
    return collection

# Load collection on server startup
pdf_folder = "C://finance"  # Ensure compatibility for file path
collection = initialize_database(pdf_folder)

@app.route('/query', methods=['POST'])
def handle_query():
    query = request.json['query']
    query_embedding = generate_query_embedding(query, embedder)
    retrieved_docs, _ = retrieve_documents(query_embedding, collection)
    response = response_generator.generate_response(query, retrieved_docs)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
