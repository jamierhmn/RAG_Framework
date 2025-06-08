from transformers import pipeline
import re
import numpy as np
from typing import Dict, List, Tuple

class QueryClassifier:
    def __init__(self):
        # Initialize zero-shot classification pipeline
        self.classifier = pipeline("zero-shot-classification")
        
        # Keywords that typically indicate need for short answers
        self.short_answer_indicators = [
            'when', 'where', 'who', 'which', 'what time', 'how many', 'how much',
            'yes or no', 'true or false', 'date', 'location', 'name', 'number',
            'price', 'cost', 'year'
        ]
        
        # Keywords that typically indicate need for longer answers
        self.long_answer_indicators = [
            'explain', 'describe', 'elaborate', 'how to', 'why', 'what are the reasons',
            'compare', 'contrast', 'analyze', 'discuss', 'evaluate', 'what is the process',
            'tell me about', 'give me details'
        ]

    def _check_keyword_indicators(self, query: str) -> float:
        """
        Check for presence of keyword indicators and return a score
        negative score suggests short answer, positive score suggests long answer
        """
        query = query.lower()
        
        short_matches = sum(1 for word in self.short_answer_indicators if word in query)
        long_matches = sum(1 for word in self.long_answer_indicators if word in query)
        
        return long_matches - short_matches

    def _analyze_query_structure(self, query: str) -> float:
        """
        Analyze query structure and length to contribute to classification
        """
        # Longer queries often require longer answers
        length_score = (len(query.split()) - 5) / 10  # normalize around typical lengths
        
        # Check for complex sentence structures
        complex_indicators = len(re.findall(r'and|or|because|therefore|however', query.lower()))
        
        return length_score + complex_indicators * 0.5

    def _get_semantic_classification(self, query: str) -> float:
        """
        Use zero-shot classification to determine if query needs detailed explanation
        """
        candidate_labels = ["factual quick answer", "detailed explanation"]
        result = self.classifier(query, candidate_labels)
        
        # Convert classification confidence to score
        score = result['scores'][1] - result['scores'][0]
        return score

    def classify_query(self, query: str) -> Dict:
        """
        Classify a query as requiring either a short or long answer
        Returns classification with confidence score and reasoning
        """
        # Gather evidence from different methods
        keyword_score = self._check_keyword_indicators(query)
        structure_score = self._analyze_query_structure(query)
        semantic_score = self._get_semantic_classification(query)
        
        # Combine scores (can be weighted differently based on importance)
        final_score = (
            keyword_score * 0.4 +
            structure_score * 0.2 +
            semantic_score * 0.4
        )
        
        # Determine classification and confidence
        is_long_answer = final_score > 0
        confidence = abs(min(final_score, 1.0))
        
        reasoning = []
        if keyword_score != 0:
            reasoning.append(f"{'Long' if keyword_score > 0 else 'Short'} answer keywords detected")
        if structure_score > 0.5:
            reasoning.append("Complex query structure suggests detailed response needed")
        if semantic_score > 0.3:
            reasoning.append("Semantic analysis indicates explanation required")
        
        return {
            "query": query,
            "requires_long_answer": is_long_answer,
            "confidence": confidence,
            "reasoning": reasoning
        }

def integrate_with_rag(query: str, classifier: QueryClassifier, retriever, generator) -> str:
    """
    Example of how to integrate the classifier with a RAG pipeline
    """
    classification = classifier.classify_query(query)
    
    if classification["requires_long_answer"]:
        # For long answers, retrieve more context and generate detailed response
        documents = retriever.get_relevant_docs(query, k=5)
        response = generator.generate(query, documents, max_length=500)
    else:
        # For short answers, retrieve fewer documents and generate concise response
        documents = retriever.get_relevant_docs(query, k=2)
        response = generator.generate(query, documents, max_length=100)
    
    return response

# Example usage
if __name__ == "__main__":
    classifier = QueryClassifier()
    
    # Example queries
    test_queries = [
        "What is the capital of France?",
        "Can you explain how photosynthesis works in detail?",
        "What time does the store open?",
        "What are the main factors contributing to climate change and their long-term impacts?",
    ]
    
    for query in test_queries:
        result = classifier.classify_query(query)
        print(f"\nQuery: {query}")
        print(f"Requires long answer: {result['requires_long_answer']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Reasoning: {', '.join(result['reasoning'])}")
