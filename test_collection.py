import chromadb

# Initialize Chroma client
client = chromadb.Client()

# List all collections
collections = client.list_collections()
print(collections)
# Print collection names
for collection in collections:
    print(f"Collection Name: {collection.name}")
