import weaviate

# Connect to your Weaviate instance
client = weaviate.Client("http://localhost:8080")  # or replace with your instance's URL

# Get the schema which includes all classes and their properties
schema = client.schema.get()

# Print out all classes and their properties (keys)
for class_info in schema['classes']:
    print(f"Class: {class_info['class']}")
    print("Properties:")
    for property_info in class_info['properties']:
        print(f"  - {property_info['name']} (data type: {property_info['dataType']})")
    print("\n")

