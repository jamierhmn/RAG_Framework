from flask import Flask, request, jsonify
import chromadb
from ingestion import ingest_and_chunk_pdfs
from embeddings import generate_chunk_embeddings, EmbeddingGenerator
from retrieval import  retrieve_documents
from response_generation import QueryResponseGenerator
from query_optimization import generate_query_embedding,expand_query
import json
app = Flask(__name__)
import nltk
nltk.download('wordnet')

# Initialize embedding generator and response generator
embedder = EmbeddingGenerator()
api_key = ""
# Create the query-response generator
generator = QueryResponseGenerator(api_key)


# Load the ChromaDB collection
def load_chroma_collection(collection_name="rag_documents"):
    client = chromadb.Client()
    collection = client.get_collection(collection_name)
    return collection

# Load collection on server startup
collection = load_chroma_collection()

@app.route('/query', methods=['POST'])
def handle_query():
    # Step 1: Decode the byte string to a normal string
    json_string=request.get_data()
  #  print("jamie:",json_string)
  #  json_string = request.decode('utf-8')

    # Step 2: Parse the JSON string into a Python dictionary
    data = json.loads(json_string)
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query is missing"}), 400

        # Step 2: Optimize the query using query expansion
    expanded_query = expand_query(query)

    # Step 3: Generate query embedding
    query_embedding = generate_query_embedding(expanded_query, embedder)

    # Step 4: Retrieve relevant documents using the query embedding
    documents, metadata = retrieve_documents(query_embedding, collection)
    # Combine the query with the retrieved documents for context
    context = documents  # Combine retrieved documents into a single context string
    print("received context",str(context))
    # Step 5: Use GPT-3.5 to generate a response based on the query and context
    #gpt_response = generator.generate_response(query, context)

    # Process the query (you can replace this with your own logic)

    return jsonify(context)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
