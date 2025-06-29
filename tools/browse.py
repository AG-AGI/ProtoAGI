from duckduckgo_search import DDGS
from collections import deque
import re
from pathlib import Path
from tools.llm import ask

def local_browse(query) -> str:
    print("Using local browsing simulation...")
    response = ask(f"pretend you are a search engine, in 1-4 lines output search results for: {query}")
    return response

def browse(query: str, max_results: int = 1) -> str:
    print(f"Searching for '{query}'...")
    
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=max_results)]
        
        if not results:
            return "No results found."

        formatted_results = []
        for result in results:
            title = result.get('title', 'No Title Found')
            url = result.get('href', 'No URL Found')
            summary = result.get('body', 'No Summary Available.')
            formatted_results.append(f"Title: {title}\nURL: {url}\nSummary: {summary}")
            
        return "\n\n---\n\n".join(formatted_results)

    except Exception as e:
        return local_browse(query)

if __name__ == "__main__":
    search_query = "france"
    search_results = browse(search_query)
    print("\n--- Search Results for 'france' ---")
    print(search_results)
    print("-----------------------------------")
    search_query_2 = "best python libraries for web scraping"
    search_results_2 = browse(search_query_2)
    print("\n--- Search Results for 'best python libraries for web scraping' ---")
    print(search_results_2)
    print("-------------------------------------------------------------------")