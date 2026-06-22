"""AnySearch wrapper for industry research — replaces DuckDuckGo."""

import logging
import os
import re

import httpx

logger = logging.getLogger(__name__)

ANYSEARCH_ENDPOINT = "https://api.anysearch.com/mcp"


class AnySearchClient:
    """Async client for AnySearch JSON-RPC API (general search only)."""

    def __init__(self, api_key: str = ""):
        self.api_key = (api_key or os.getenv("ANYSEARCH_API_KEY", "")).strip()

    async def search(self, query: str, max_results: int = 20) -> list[dict]:
        """Single general search query via AnySearch."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "search",
                "arguments": {"query": query, "max_results": max_results},
            },
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    ANYSEARCH_ENDPOINT, json=payload, headers=headers
                )
                resp.raise_for_status()
                data = resp.json()
                if "error" in data:
                    logger.warning("AnySearch API error: %s", data["error"])
                    return []
                content = data.get("result", {}).get("content", [])
                markdown_text = ""
                for item in content:
                    if item.get("type") == "text":
                        markdown_text = item.get("text", "")
                        break
                return self._parse_results(markdown_text)
        except Exception as e:
            logger.warning("AnySearch request failed: %s", e)
            return []

    async def batch_search(self, queries: list[str], max_results: int = 10) -> list[dict]:
        """Execute multiple search queries in parallel via batch_search."""
        query_objects = [{"query": q, "max_results": max_results} for q in queries]
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "batch_search",
                "arguments": {"queries": query_objects},
            },
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(
                    ANYSEARCH_ENDPOINT, json=payload, headers=headers
                )
                resp.raise_for_status()
                data = resp.json()
                if "error" in data:
                    logger.warning("AnySearch batch API error: %s", data["error"])
                    return []
                content = data.get("result", {}).get("content", [])
                markdown_text = ""
                for item in content:
                    if item.get("type") == "text":
                        markdown_text = item.get("text", "")
                        break
                return self._parse_results(markdown_text)
        except Exception as e:
            logger.warning("AnySearch batch request failed: %s", e)
            return []

    def _parse_results(self, markdown: str) -> list[dict]:
        """Parse AnySearch Markdown output into structured result dicts."""
        results = []
        # Pattern: ### N. Title\n- **URL**: url\n...snippet...
        blocks = re.split(r"### \d+\.\s+", markdown)
        for block in blocks[1:]:
            lines = block.strip().split("\n")
            if not lines:
                continue
            title = lines[0].strip()
            url = ""
            snippet_parts = []

            for line in lines[1:]:
                line = line.strip()
                if line.startswith("- **URL**"):
                    url = line.split("**:", 1)[-1].strip().lstrip(":")
                elif line.startswith("- **URL**:") and not url:
                    url = line.split("**:", 1)[-1].strip()
                elif line and not line.startswith("- **"):
                    snippet_parts.append(line)

            results.append({
                "title": title,
                "url": url,
                "snippet": " ".join(snippet_parts) if snippet_parts else "",
                "source": _extract_source(url),
            })

        return results


async def search_industry(industry: str, max_results: int = 20) -> list[dict]:
    """Search for industry research reports via AnySearch.

    Uses batch_search to query multiple angles in parallel for comprehensive results.
    Returns a list of dicts with keys: title, url, snippet, source.
    """
    queries = [
        f"{industry} 行业研究报告 券商研报 市场规模 竞争格局 2026",
        f"{industry} 产业链 上市公司 龙头企业 分析",
        f"{industry} 市场规模 增长率 发展趋势 预测",
    ]

    client = AnySearchClient()

    # Try batch search first (3 queries in parallel)
    results = await client.batch_search(queries, max_results=10)
    logger.info("AnySearch batch returned %d results for '%s'", len(results), industry)

    # If batch returned too few, fall back to a single larger search
    if len(results) < 5:
        logger.info("Batch results insufficient, falling back to single search")
        results = await client.search(
            f"{industry} 行业深度研究报告 2026", max_results=max_results
        )
        logger.info(
            "AnySearch fallback returned %d results for '%s'",
            len(results),
            industry,
        )

    seen_urls = set()
    deduped = []
    for r in results:
        if r["url"] and r["url"] not in seen_urls:
            seen_urls.add(r["url"])
            deduped.append(r)

    results = deduped[:max_results]

    # Last-resort mock so the pipeline never stalls
    if not results:
        logger.warning("AnySearch returned no results, providing mock fallback.")
        results = [
            {
                "title": f"{industry} 行业深度研究报告",
                "url": "https://example.com/report",
                "snippet": f"关于{industry}行业的最新市场规模、竞争格局、技术趋势和投资建议分析...",
                "source": "Mock数据",
            }
        ]

    return results


def _extract_source(url: str) -> str:
    """Extract a human-readable source label from a URL."""
    from urllib.parse import urlparse

    netloc = urlparse(url).netloc
    if "zhihu" in netloc:
        return "知乎"
    if "36kr" in netloc:
        return "36氪"
    if "eastmoney" in netloc or "10jqka" in netloc:
        return "东方财富"
    if "sina" in netloc:
        return "新浪财经"
    if "163" in netloc:
        return "网易财经"
    if "pdf" in url.lower():
        return "PDF研报"
    return netloc.replace("www.", "") if netloc else "网页"
