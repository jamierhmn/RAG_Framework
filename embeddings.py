from transformers import AutoTokenizer, AutoModel
import torch

class EmbeddingGenerator:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def generate_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state[:, 0, :].numpy()
        return embeddings.squeeze()

def generate_chunk_embeddings(chunks_with_metadata):
    embedder = EmbeddingGenerator()
    chunk_embeddings = []

    for chunk, metadata in chunks_with_metadata:
        embedding = embedder.generate_embeddings(chunk)
        chunk_embeddings.append((embedding, metadata))

    return chunk_embeddings

