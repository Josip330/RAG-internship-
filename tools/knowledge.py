from langchain_core.tools import tool
from config.settings import get_embeddings, get_qdrant_client
import os

embeddings = get_embeddings()
qdrant_client = get_qdrant_client()

@tool
def retrieve_knowledge(query: str) -> str:
    """Search knowledge base for information about Magic: The Gathering rules."""
    try:
        query_vector = embeddings.embed_query(query)
        
        search_result = qdrant_client.query_points(
            collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
            query=query_vector,
            limit=3
        )
        
        results = []
        for hit in search_result.points:
            if hasattr(hit, 'payload') and 'text' in hit.payload:
                results.append(hit.payload['text'])
        
        return "\n".join(results) if results else "No relevant knowledge found."
    
    except Exception as e:
        return f"Error retrieving knowledge: {str(e)}"