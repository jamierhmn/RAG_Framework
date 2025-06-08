import openai
from enum import Enum

class Collection(str, Enum):
    GAMES = "DocumentGames"
    FINANCE = "DocumentFinance"

class ReActAgentRouter:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        openai.api_key = api_key  # Set OpenAI API Key
        self.model = model  # Choose GPT model

        self.classification_prompt = """You are a ReAct (Reasoning + Acting) agent that routes queries to the appropriate document collection.

Available collections:
1. DocumentGames - For queries about:
   - League of Legends API
   - Valorant API
   - Riot Games terms

2. DocumentFinance - For queries about:
   - Banking
   - Alternative investments
   - Portfolio management

### Steps to follow:
1️⃣ Understand the query intent.  
2️⃣ Identify key information needed.  
3️⃣ Select the most appropriate collection (DocumentGames or DocumentFinance).  
4️⃣ Explain your confidence level in classification.  

### Response Format (JSON only):
{{ "collection": "<selected_collection>", "confidence": "<confidence_score>", "reasoning": "<brief_explanation>" }}
"""

    def classify_query(self, query: str) -> dict:
        """
        Classifies the given query into either the GAMES or FINANCE collection using GPT-4.
        """
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.classification_prompt},
                {"role": "user", "content": f"Query: {query}"}
            ],
            temperature=0.2,
            max_tokens=100,
        )

        # Extracting response
        gpt_response = response["choices"][0]["message"]["content"]
        
        try:
            classification = eval(gpt_response)  # Convert JSON string to dict
        except Exception as e:
            classification = {"collection": None, "confidence": "Low", "reasoning": f"Error parsing response: {str(e)}"}
        
        return classification

# ✅ Example Usage
if __name__ == "__main__":
    api_key = 'sk-nRihvOmpF72sK7WZmNQxiqTwMWpx8YuWIElBpSqBAST3BlbkFJeWPOonQdlVP8Nu_EH3NGxohV-Fs5TfilVY1ILJP2gA'  # Replace with your actual API key
    router = ReActAgentRouter(api_key)

    queries = [
        "How to integrate Riot Games API with my game?",
        "Best strategies for portfolio diversification?",
        "What is the Valorant API rate limit?",
        "How do hedge funds manage alternative investments?"
    ]

    for query in queries:
        result = router.classify_query(query)
        print(f"Query: {query}\nClassification: {result}\n")

