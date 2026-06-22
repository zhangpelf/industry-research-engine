from langgraph.graph import StateGraph

from workflow.nodes import (
    analyze_financials,
    render_html_node,
    search_reports,
    write_report,
)
from workflow.state import ResearchState


def create_research_graph() -> StateGraph:
    """Assemble the 4-node sequential LangGraph."""
    builder = StateGraph(ResearchState)

    builder.add_node("search_reports", search_reports)
    builder.add_node("analyze_financials", analyze_financials)
    builder.add_node("write_report", write_report)
    builder.add_node("render_html_node", render_html_node)

    builder.set_entry_point("search_reports")
    builder.add_edge("search_reports", "analyze_financials")
    builder.add_edge("analyze_financials", "write_report")
    builder.add_edge("write_report", "render_html_node")
    builder.set_finish_point("render_html_node")

    return builder.compile()
