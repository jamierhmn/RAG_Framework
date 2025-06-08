import json
from embedding_util import generate_embeddings
from weaviate_client import get_weaviate_client

# Get the Weaviate client
client = get_weaviate_client()

# Define the query you want to search for
query = "Short Term Agricultural Credit institutions"
query_vector = generate_embeddings(query)

# Perform the search based on the query vector
result = client.query.get(
    "DocumentFinance", ["source_text"]
).with_near_vector(
    {
        "vector": query_vector,
        "certainty": 0.7  # Adjust the certainty threshold as needed
    }
).with_limit(3).with_additional(['certainty', 'distance']).do()

# Print out the results in a readable format
print(json.dumps(result, indent=4))

