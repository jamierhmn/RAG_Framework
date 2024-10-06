import chromadb

# Initialize the client
client = chromadb.Client()

# List all collections in the ChromaDB database
collections = client.list_collections()

# Output the collection names
if collections:
    print("Available Collections:")
    for collection in collections:
        print(collection.name)
else:
    print("No collections found.")