from workflow.state import ResearchState
from utils.llm import LLMClient


async def write_report(state: ResearchState) -> dict:
    """Node 3: Generate full Markdown industry research report via LLM."""
    industry = state["industry"]
    analysis = state.get("financial_analysis", "")
    results = state.get("search_results", [])

    snippets = "\n\n".join(
        f"【{r.get('source', '来源')}】{r.get('title', '')}\n{r.get('snippet', '')}"
        for r in results[:5]
    )

    system_prompt = (
        "你是一位顶级券商研究所的首席分析师。请撰写一份专业的行业研究报告。\n\n"
        "报告要求：\n"
        "- 使用中文，Markdown格式\n"
        "- 结构完整，数据翔实\n"
        "- 语气专业、客观\n"
        "- 如有不确定数据，使用'约'、'预计'等措辞\n\n"
        "报告结构：\n"
        "## 执行摘要\n"
        "## 行业概况\n"
        "## 产业链分析\n"
        "## 市场规模与增长驱动\n"
        "## 竞争格局与关键企业\n"
        "## 技术趋势与创新\n"
        "## 风险因素\n"
        "## 投资建议与展望\n\n"
        "每个章节下使用 ### 细分子节。"
        "开头不要写'以下'、'这是'等元评论。直接开始报告正文。"
    )

    client = LLMClient()
    try:
        report = await client.chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": (
                f"请撰写关于「{industry}」的行业研究报告。\n\n"
                f"参考分析数据：\n{analysis}\n\n"
                f"搜索结果参考：\n{snippets}"
            )},
        ], temperature=0.5, max_tokens=8192)
    finally:
        await client.close()

    return {
        "markdown_report": report,
        "progress": 75,
        "status_message": "报告撰写完成",
        "error": None,
    }
