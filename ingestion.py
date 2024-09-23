import os
import pdfplumber

def ingest_and_chunk_pdfs(pdf_folder, chunk_size=200, overlap=20):
    """
    Ingest PDF documents, split them into chunks with overlap, and return chunks with metadata.
    """
    chunks_with_metadata = []

    for file_name in os.listdir(pdf_folder):
        if file_name.endswith('.pdf'):
            try:
                with pdfplumber.open(os.path.join(pdf_folder, file_name)) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:  # Ensure text is not None or empty
                            chunks = split_into_chunks(text, chunk_size, overlap)
                            for i, chunk in enumerate(chunks):
                                metadata = {
                                    "document_id": file_name,
                                    "page_number": page.page_number,
                                    "chunk_index": i,
                                    "document_type": "PDF",
                                }
                                chunks_with_metadata.append((chunk, metadata))
            except Exception as e:
                print(f"Error reading {file_name}: {e}")

    return chunks_with_metadata

def split_into_chunks(text, chunk_size, overlap):
    """
    Split text into smaller chunks with overlap.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        # Create a chunk and apply the overlap for the next chunk
        end = min(start + chunk_size, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += (chunk_size - overlap)  # Move the start pointer by chunk_size minus overlap

    return chunks

pdf_folder = "C://finance"  # Ensure compatibility for file path
#data = ingest_and_chunk_pdfs(pdf_folder, chunk_size=200, overlap=20)
#print(data)

