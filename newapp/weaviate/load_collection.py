import weaviate

# Connect to Weaviate instance
client = weaviate.Client("http://localhost:8080")  # Change URL if needed

# Query the DocumentGames collection
response = client.query.get(
    "DocumentGames",
    ["document_id", "page_number", "chunk_index", "source_text"]
).do()

# Print the retrieved chunks
for item in response["data"]["Get"]["DocumentGames"]:
    print(item)

