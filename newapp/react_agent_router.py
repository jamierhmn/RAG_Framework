from typing import List, Dict, Optional
import openai
from enum import Enum
import logging

class Collection(str, Enum):
    GAMES = "DocumentGames"
    FINANCE = "DocumentFinance"

class ReActAgentRouter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        
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

Think through these steps:
1. Understand the query intent
2. Identify key information needed
3. Select the most appropriate collection
4. Explain your confidence level

Respond in JSON:
{
    "collection": "DocumentGames or DocumentFinance",
    "confidence": float between 0 and 1,
    "reasoning": "your explanation",
    "search_terms": ["relevant", "search", "terms"]
}"""

    async def classify_query(self, query: str) -> Dict:
        """Use GPT to classify the query"""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.classification_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.3
            )
            return response.choices[0].message['content']
        except Exception as e:
            logging.error(f"Classification error: {str(e)}")
            return self._fallback_classification(query)

    def _fallback_classification(self, query: str) -> Dict:
        """Simple fallback classification"""
        query_lower = query.lower()
        games_terms = {'league', 'legends', 'valorant', 'riot', 'api', 'game'}
        finance_terms = {'bank', 'investment', 'portfolio', 'financial'}
        
        games_matches = sum(1 for term in games_terms if term in query_lower)
        finance_matches = sum(1 for term in finance_terms if term in query_lower)
        
        if games_matches >= finance_matches:
            return {
                "collection": "DocumentGames",
                "confidence": 0.6,
                "reasoning": "Fallback: Gaming terms detected",
                "search_terms": list(games_terms & set(query_lower.split()))
            }
        return {
            "collection": "DocumentFinance",
            "confidence": 0.6,
            "reasoning": "Fallback: Finance terms detected",
            "search_terms": list(finance_terms & set(query_lower.split()))
        }

async def process_query(router: ReActAgentRouter, query: str, client, top_k: int = 5) -> Dict:
    """Process a query using the ReAct agent router"""
    try:
        # Get classification
        classification = await router.classify_query(query)
        
        # Search in appropriate collection
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant specializing in {classification['collection']} information."},
                {"role": "user", "content": query}
            ],
            temperature=0.7
        )
        
        return {
            "response": response.choices[0].message['content'],
            "classification": classification
        }
        
    except Exception as e:
        logging.error(f"Query processing error: {str(e)}")
        return {
            "response": "I apologize, but I encountered an error processing your query. Please try again.",
            "classification": None
        }
