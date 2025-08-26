from langchain_core.tools import tool
from tavily import TavilyClient
import os

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def tavily_search(query: str) -> str:
    """Search the web for discussions and forums on Magic: The Gathering rules."""
    try:
        query = f"{query}"
        
        response = tavily_client.search(
            query=query,
            search_depth="basic",
            max_results=3,
            include_answer=True
        )
        
        if response.get('answer'):
            return response['answer']
        
        results = []
        for result in response.get('results', []):
            title = result.get('title', '')
            content = result.get('content', '')
            url = result.get('url', '')
            if content and len(content) > 50:
                results.append(f"**{title}**\n{content}\nSource: {url}")
        
        return "\n\n".join(results) if results else "No relevant search results found."
    
    except Exception as e:
        return f"Error searching web: {str(e)}"