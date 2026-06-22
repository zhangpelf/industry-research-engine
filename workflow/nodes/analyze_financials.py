from workflow.state import ResearchState
from utils.llm import LLMClient


async def analyze_financials(state: ResearchState) -> dict:
    """Node 2: Analyze search results via LLM to extract financial insights."""
    industry = state["industry"]
    results = state.get("search_results", [])

    snippets = "\n\n".join(
        f"【{r.get('source', '来源')}】{r.get('title', '')}\n{r.get('snippet', '')}"
        for r in results[:8]
    )

    system_prompt = (
        "你是一位资深行业研究员。根据以下搜索材料，分析该行业的：\n"
        "1. 核心产业链结构（上游/中游/下游）\n"
        "2. 主要上市公司及财务概况（如已知）\n"
        "3. 市场规模与增长趋势\n"
        "4. 竞争格局与集中度\n"
        "5. 技术路线与创新方向\n"
        "输出结构化分析，每个维度用 ### 标题分段。"
        "用中文。如果某些信息不足，诚实说明。"
    )

    client = LLMClient()
    try:
        analysis = await client.chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"行业：{industry}\n\n搜索材料：\n{snippets}"},
        ], temperature=0.3)
    finally:
        await client.close()

    return {
        "financial_analysis": analysis,
        "progress": 50,
        "status_message": "财务数据分析完成",
        "error": None,
    }
