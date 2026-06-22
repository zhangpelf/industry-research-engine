"""TypedDict state definition for the LangGraph research workflow."""

from typing import TypedDict, Optional


class ResearchState(TypedDict):
    """State passed between LangGraph nodes during report generation."""

    industry: str
    search_results: list[dict]
    financial_analysis: str
    markdown_report: str
    html_report: str
    progress: int            # 0 → 100
    status_message: str
    error: Optional[str]
