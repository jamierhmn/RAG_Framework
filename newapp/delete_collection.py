import weaviate

def delete_class_in_weaviate(weaviate_url="http://localhost:8080", class_name="DocumentFinane"):
    """
    Delete the class and all associated data from Weaviate.
    """
    # Connect to Weaviate
    client = weaviate.Client(weaviate_url)

    # Check if the class exists before attempting to delete it
    existing_classes = client.schema.get()
    if class_name in [cls['class'] for cls in existing_classes['classes']]:
        # Delete the class
        client.schema.delete_class(class_name)
        print(f"Class '{class_name}' and all its data have been deleted.")
    else:
        print(f"Class '{class_name}' does not exist.")

# Call the function to delete the class
delete_class_in_weaviate()

