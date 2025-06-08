# backend.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from weaviate_client import get_weaviate_client
from embedding_util import generate_embeddings
from route_classifier_agent import Collection,ReActAgentRouter
import openai
import json
from collections import deque
import os
import logging
from query_classifier import QueryClassifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# OpenAI API key setup
#openai.api_key = 'sk-nRihvOmpF72sK7WZmNQxiqTwMWpx8YuWIElBpSqBAST3BlbkFJeWPOonQdlVP8Nu_EH3NGxohV-Fs5TfilVY1ILJP2gA'
class QueryRequest(BaseModel):
    query: str

class ResultHistory:
    def __init__(self, storage_file: str = "search_history.json"):
        self.storage_file = storage_file
        self.results = self.load_history()

    def load_history(self) -> deque:
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    return deque(data, maxlen=10)  # Keep only last 10 items
            except json.JSONDecodeError:
                return deque(maxlen=10)
        return deque(maxlen=10)

    def save_history(self):
        with open(self.storage_file, 'w') as f:
            json.dump(list(self.results), f)

    def add_result(self, result: dict):
        self.results.append(result)
        self.save_history()

    def get_history(self) -> List[dict]:
        return list(self.results)

result_history = ResultHistory()

@app.post("/query")
async def handle_query(request: QueryRequest):
    try:
        logger.info(f"Received query: {request.query}")
        query = request.query
        router = ReActAgentRouter(openai.api_key)
        result = router.classify_query(query) 
        Classification = result["collection"]
        print("classification=",Classification)
        # Generate embeddings and search Weaviate
        query_vector = generate_embeddings(query)
        client = get_weaviate_client()
        
        search_result = client.query.get(
            Classification, ["source_text"]
        ).with_near_vector(
            {
                "vector": query_vector,
                "certainty": 0.7
            }
        ).with_limit(5).with_additional(['certainty']).do()

        chunks = search_result.get('data', {}).get('Get', {}).get('DocumentGames', [])
        print(chunks)
        # Classify query and construct prompt
        classifier = QueryClassifier()
        classification = classifier.classify_query(query)
        is_long_answer = classification['requires_long_answer']
        if Classification =="DocumentFinance":
            Assistant ="You are a financial assistant"
        else:
            Assistant ="You are a Gaming assistant"
        #prompt = f"You are a financial assistant.User Query: {query}\n\nBased on the following information, please provide a {'detailed' if is_long_answer else 'short and precise'} response **only using the provided text**:\n\n"
        #prompt = f"You are a financial assistant. Please respond **using only the information from the below text . User Query: {query}\n\nBased on the following information, please provide a {'detailed' if is_long_answer else 'short and precise'} response:\n\n"
        prompt = f"{Assistant}. Please respond **using only the information from the below text . User Query: {query}\n\nBased on the following information, please provide a {'detailed' if is_long_answer else 'short and precise'} response:\n\n"
        for idx, chunk in enumerate(chunks):
            prompt += f"Chunk {idx + 1}: {chunk['source_text']}\n\n"
        print(prompt)
        
      # Get OpenAI response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            top_p=0.9,
            max_tokens=300
        )
        gpt_response = response.choices[0].message['content']

        # Create and save result
        result = {
            "query": query,
            "response": gpt_response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        result_history.add_result(result)

        return {
            "response": gpt_response,
            "history": result_history.get_history()
        }

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/query_history")
async def get_query_history():
    return result_history.get_history()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
