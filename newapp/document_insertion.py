import os
from embedding_util import generate_embeddings
from weaviate_client import get_weaviate_client, setup_class_schema
from ingestion import ingest_and_chunk_pdfs

# Folder containing PDF files
pdf_folder = "games"

# Get the Weaviate client and set up the schema
client = get_weaviate_client()
setup_class_schema(client)

# Ingest and chunk PDF files from the 'finance' folder
chunks_with_metadata = ingest_and_chunk_pdfs(pdf_folder)
print(chunks_with_metadata)
# Configure the batch size for insertion
client.batch.configure(batch_size=len(chunks_with_metadata))

# Insert chunks with metadata into Weaviate
with client.batch as batch:
    for i, (chunk, metadata) in enumerate(chunks_with_metadata):
        print(f"Inserting chunk {i + 1}/{len(chunks_with_metadata)} from {metadata['document_id']}")

        properties = {
            "source_text": metadata["content"],  # The chunk content
            "document_id": metadata["document_id"],
            "page_number": metadata["page_number"],
            "chunk_index": metadata["chunk_index"],
            "document_type": metadata["document_type"]
        }

        # Generate embedding for the chunk
        vector = generate_embeddings(chunk)

        # Add the chunk and its metadata to Weaviate
        #batch.add_data_object(properties, "DocumentFinance", vector=vector)
        batch.add_data_object(properties, "DocumentGames", vector=vector)
print("Document insertion completed!")

