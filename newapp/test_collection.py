import weaviate

# Connect to your Weaviate instance
client = weaviate.Client("http://localhost:8080")  # Replace with your Weaviate instance's URL

# Get the schema which includes all classes
schema = client.schema.get()

# Retrieve up to 3 collections (classes)
collections = schema['classes'][:3]  # Limit to 3 classes

# Print the names of the collections and their properties
for idx, class_info in enumerate(collections, 1):
    print(f"Collection {idx}: {class_info['class']}")
    print("Properties:")
    for property_info in class_info['properties']:
        print(f"  - {property_info['name']} (data type: {property_info['dataType']})")
    print("\n")

