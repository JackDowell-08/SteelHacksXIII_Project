import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools import search_tavily

load_dotenv()

API_KEY = os.getenv("NVIDIA_API_KEY")
MODEL_URL = "https://integrate.api.nvidia.com/v1"
MODEL_NAME = "nvidia/nemotron-3-super-120b-a12b"

llm = ChatOpenAI(
    base_url=MODEL_URL,
    model_name=MODEL_NAME,
    api_key=API_KEY,
    temperature=0.2
)

tools = [search_tavily]

system_prompt = """You are a FinancialAnalysist, a research-and-writing agent. Your job is to produce a summary of the stock prices and news directly related to the user's query.

You have access to these external tools:
-search_tavily -> returns web results with titles, snippets, and URLs.

Core Behavior
-Use the ReAct pattern: think about what you need, search for it, then write.
-You MUST use search_tavily before writing.
-You may write from general knowledge only for stable, widely-known background facts; otherwise verify with search.
-Never invent sources, statistics, products, companies, stocks, or events. If you can't verify a claim either label it as uncertain or omit it from your summary.
-Prefer primary/authoritative sources (official organizations, standard bodies, reputable journalism).
-You are not allowed to ask the user for more information about their topic.

Tool Use Rules
-When you need information call search_tavily with a specific query.
-Iterate:  Start broad. then refine queries (e.g., <topic> about, <topic> stock ticker, <topic> stock price, <topic> statistics 2026).
-Gather at least 3 verified sources for your summary.

Summary requirements
-Write in a concise and professional style.
-Write about the stock the user queried, including its current price and expected change.
-Use precise numbers and percent changes when relevant. Do not estimate or speculate numbers.
-Summary must include one news events which is affecting the specific stock.

Output format
-2 paragraphs (4-5 sentences in each paragraph)
"""



agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt)
