from app.tools.rag_tool import search_financial_knowledge

def test_retrieval():
    print("--- Testing RAG Retrieval ---")
    query = "כמה כסף כדאי לחסוך?"
    results = search_financial_knowledge(query)
    
    if not results:
        print("No results found. Check if DB is populated.")
        return

    for i, res in enumerate(results):
        print(f"Result {i+1}:")
        print(f" - Source: {res.source}")
        print(f" - Content: {res.content}")
        print("-" * 30)

if __name__ == "__main__":
    test_retrieval()