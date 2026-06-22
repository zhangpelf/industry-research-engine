# Project: industry-research-app

## Current State (2026-06-21)

### What Changed

| File | Change |
|---|---|
| `utils/search.py` | Full rewrite — removed `duckduckgo-search`, replaced with `httpx` → AnySearch JSON-RPC API (`search` + `batch_search` methods) |
| `workflow/nodes/search_reports.py` | `max_results=10` → `max_results=20`; docstring updated |
| `app.py` | Sidebar badge: AnySearch; added 5 example industry quick-select chips |
| `requirements.txt` | Removed `duckduckgo-search>=8.0.0` |

### AnySearch Integration Details

- **Protocol**: JSON-RPC over HTTP (`https://api.anysearch.com/mcp`)
- **Search methods**: `search` (single query) + `batch_search` (parallel queries)
- **Strategy**: 3-angle batch (研报/产业链/市场规模) → fallback to single large search if <5 results → URL dedup → mock fallback if empty
- **Parser**: Markdown output → `### N. Title` pattern → structured dicts with `title`, `url`, `snippet`, `source`
- **Source labeler**: Extracts domain → Chinese labels (知乎/36氪/东方财富/PDF研报...)

### Files Not Changed (working state expected)

- `workflow/state.py`, `workflow/graph.py`, `workflow/nodes/*` (others), `workflow/templates/`, `utils/llm.py`, `utils/format.py`

### Remaining Work / Known Issues

1. **Endpoint config**: `ANYSEARCH_ENDPOINT` is hardcoded as `https://api.anysearch.com/mcp` — should read from env var
2. **API key**: Passed but unused on current endpoint; may need auth later
3. **Parser fragility**: `_parse_results` depends on Markdown format `### N. Title\n- **URL**: url` — if API changes output format, parser breaks silently
4. **No tests**: No unit tests for search client or parser
5. **AnySearch CLI vs API**: Decision was direct HTTP (not CLI subprocess) — relies on JSON-RPC endpoint being stable
6. **app.py example chips**: `st.rerun()` updates `industry` variable but Streamlit button callback may not propagate correctly — needs runtime testing
