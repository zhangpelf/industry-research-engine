import sys
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")
os.environ["LLM_MODEL"] = "meta-llama/llama-3.1-8b-instruct:free"

print("Running Evals for Industry Research App...")
print("==========================================")

passed = 0
total = 0

def assert_step(name, condition, error_msg=""):
    global passed, total
    total += 1
    if condition:
        print(f"✅ PASS: {name}")
        passed += 1
    else:
        print(f"❌ FAIL: {name} - {error_msg}")

# Regression 1: app.py syntax check
try:
    import py_compile
    py_compile.compile("app.py", doraise=True)
    assert_step("界面加载 (app.py 无语法错误)", True)
except Exception as e:
    assert_step("界面加载 (app.py 无语法错误)", False, str(e))

# Regression 2: module imports
try:
    from workflow.graph import create_research_graph
    assert_step("依赖健康 (图模块可导入)", True)
except Exception as e:
    assert_step("依赖健康 (图模块可导入)", False, str(e))

# Capability 1: Graph initialization
try:
    from workflow.graph import create_research_graph
    graph = create_research_graph()
    assert_step("工作流初始化 (创建 LangGraph 成功)", graph is not None)
except Exception as e:
    assert_step("工作流初始化 (创建 LangGraph 成功)", False, str(e))

from unittest.mock import patch

# Capability 2 & 3: Run pipeline for a lightweight keyword
async def test_pipeline():
    try:
        from workflow.graph import create_research_graph
        from utils.llm import LLMClient
        
        async def mock_chat(*args, **kwargs):
            return "Test Markdown Output\n" * 20
            
        with patch.object(LLMClient, 'chat', side_effect=mock_chat):
            graph = create_research_graph()
            initial = {
                "industry": "EDD Test Query",
                "search_results": [{"title": "Test", "snippet": "Test"}],
                "financial_analysis": "Test Financials",
                "markdown_report": "",
                "html_report": "",
                "progress": 0,
                "status_message": "Init",
                "error": None
            }
            
            final_state = None
            async for event in graph.astream(initial):
                for v in event.values():
                    if isinstance(v, dict):
                        if not final_state:
                            final_state = {}
                        final_state.update(v)
                        
            md_ok = final_state and len(final_state.get("markdown_report", "")) > 100
            html_ok = final_state and len(final_state.get("html_report", "")) > 100
            
            assert_step("基础研报生成 (Markdown 长度达标)", md_ok, "Markdown report too short or missing")
            assert_step("HTML转换能力 (HTML 长度达标)", html_ok, "HTML report too short or missing")
            
    except Exception as e:
        assert_step("基础研报生成 (Markdown 长度达标)", False, str(e))
        assert_step("HTML转换能力 (HTML 长度达标)", False, "Pipeline failed before HTML generation")

asyncio.run(test_pipeline())

print("==========================================")
print(f"Total: {total}, Passed: {passed}")
if passed == total:
    print("STATUS: ALL PASS")
    sys.exit(0)
else:
    print("STATUS: HAS FAILURES")
    sys.exit(1)
