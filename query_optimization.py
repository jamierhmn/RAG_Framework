from nltk.corpus import wordnet

def expand_query(query):
    synonyms = []
    for word in query.split():
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
    return query + " " + " ".join(set(synonyms))

def generate_query_embedding(query, embedder):
    expanded_query = expand_query(query)
    query_embedding = embedder.generate_embeddings(expanded_query)
    return query_embedding
