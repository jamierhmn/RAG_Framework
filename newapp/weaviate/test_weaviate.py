import weaviate

# Connect to Weaviate instance
client = weaviate.Client("http://localhost:8080")  # or your Weaviate instance URL

# Check available classes (collections)
schema = client.schema.get()
print("Available classes:")
for class_obj in schema['classes']:
    print("name:",class_obj['class'])

response = (
         client.query
        .get("DocumentGames",
             ["content", "document_id", "page_number", "chunk_index", "document_type"])  # Retrieve relevant fields
        .with_near_vector({"vector": query_embedding})
        .with_limit(top_k)  # Limit the number of results to top_k
        .do()
    )
print("response=",response)
