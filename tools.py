import os
import asyncio
import logging
from dotenv import load_dotenv

from typing import Literal
from langchain_core.tools import tool
from tavily import TavilyClient

load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=tavily_api_key)

chunks_per_source = 3
max_results = 5
time_range = 15
#include_images = False

def deduplicate_and_format(search_results):

    #convert our search_results into a list or dictionary for deduplication/formatting
    if isinstance(search_results, dict):
        sources_list = search_results["results"]
    elif isinstance(search_results, list):
        sources_list = []
        for response in search_results:
            if isinstance(response, dict) and "results" in response:
                sources_list.extend(response["results"])
            else:
                sources_list.extend(response)
    else:
        raise ValueError(
            "Input must be either a dict with 'results' or a list of search results"
        )

    #remove duplicatew sources
    unique_sources = {}
    for source in sources_list:
        if source['url'] not in unique_sources:
            unique_sources[source['url']] = source

    #format for Agent Freddy
    formatted_text = "Sources:\n\n"
    for i, source in enumerate(unique_sources.values()):
        formatted_text += ("Source: " + source['title'] + ":\n")
        formatted_text += ("URL: " + source['url'] + "\n")
        formatted_text += ("Relevant content from source: " + source['content'] + "\n")

    formatted_text = str(formatted_text)
    return formatted_text.strip()
    


@tool(parse_docstring=True)
def search_tavily(
    queries: list[str],
    topic: Literal["news", "finance", "general"] = "finance",
    include_images: bool = False,
) -> str:
    """Search the web using the Tavily API.

    Args:
        queries: List of queries to search.
        topic: The topic of the provided queries.
          general - General search.
          news - News search.
          finance - Finance search.

    Returns:
        A string of the search results.
    """
 
    #loop through queries from agent
    search_results = []
    for query in queries:
        search_results.append(
            #asyncio.create_task)
            tavily_client.search(
                query,
                chunks_per_source=chunks_per_source,
                max_results=max_results,
                topic=topic,
                days=time_range,
                include_images=include_images
            )
            #)
        )

    #search_results = await asyncio.gather(*search_results)

    formatted_results = deduplicate_and_format(search_results)

    return formatted_results