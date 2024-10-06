import openai


class QueryResponseGenerator:
    def __init__(self, api_key, model_name="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model_name = model_name
        openai.api_key = self.api_key

    def generate_response(self, query, retrieved_documents):
        # Combine all retrieved documents into a single context
        context = " ".join(retrieved_documents)

        # Create the prompt with the context and the query
        prompt = f"Context: {context}\n\nQuery: {query}\n\nAnswer:"

        # Use OpenAI API to generate a response
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system",
                 "content": "You are an AI that provides accurate and concise answers based on the provided context."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extract and return the generated text
        return response['choices'][0]['message']['content']

