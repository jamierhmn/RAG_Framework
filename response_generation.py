from transformers import pipeline

class QueryResponseGenerator:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.generator = pipeline('text-generation', model=model_name)

    def generate_response(self, query, retrieved_documents):
        context = " ".join(retrieved_documents)
        prompt = f"Context: {context}\n\nQuery: {query}\n\nAnswer:"
        response = self.generator(prompt, max_length=200)
        return response[0]['generated_text']

