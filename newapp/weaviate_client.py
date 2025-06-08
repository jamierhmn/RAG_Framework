import weaviate

def get_weaviate_client():
    # Create Weaviate client
    client = weaviate.Client(
        url="http://localhost:8080",  # Replace with your endpoint
    )

    # Check if the client is ready
    if client.is_ready():
        print("Weaviate client is ready.")
    else:
        raise ConnectionError("Weaviate client is not ready.")

    return client


def setup_class_schema(client):
    # Define the class schema for document search
    class_obj = {
        "class": "DocumentGames",
        "vectorizer": "none",
    }

    # Add the class to the schema if it doesn't exist
    client.schema.create_class(class_obj)
    print("Schema set up successfully!")

