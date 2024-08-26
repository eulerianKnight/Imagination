from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from vectorstore import _retriever


web_search_tool = TavilySearchResults(max_results=2)

@tool
def chromadb_search_tool(collections: str, query: str):
    """Retrieve relevant content from ChromaDB VectorStore based on query 
    for the specific Username provided as the collections name for chromadb.
    """
    retriever = _retriever(collections=collections)
    docs = retriever.query(query, k=2)
    return "\n\n".join([doc["page_content"] for doc in docs])


tool_mapping = {"WEB_SEARCH_TOOL": web_search_tool, "CHROMA_DB_SEARCH_TOOL": chromadb_search_tool}