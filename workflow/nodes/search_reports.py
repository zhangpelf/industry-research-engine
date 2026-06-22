from workflow.state import ResearchState
from utils.search import search_industry


async def search_reports(state: ResearchState) -> dict:
    """Node 1: Search AnySearch for industry reports and data."""
    industry = state["industry"]
    results = await search_industry(industry, max_results=20)
    return {
        "search_results": results,
        "progress": 25,
        "status_message": f"搜索完成，找到 {len(results)} 条相关结果",
        "error": None,
    }
