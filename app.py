import os
import threading
import asyncio
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Load local .env if present (for development); on Streamlit Cloud, secrets take precedence
load_dotenv(Path(__file__).parent / ".env", override=False)

# Pre-load secrets into environment so downstream code (LLMClient, AnySearchClient) picks them up
def _bootstrap_secrets():
    """Copy Streamlit Cloud secrets into os.environ (secrets > .env > empty)."""
    mapping = {
        "OPENROUTER_API_KEY": "OPENROUTER_API_KEY",
        "ANYSEARCH_API_KEY": "ANYSEARCH_API_KEY",
        "LLM_MODEL": "LLM_MODEL",
    }
    for secret_key, env_key in mapping.items():
        if secret_key in st.secrets and st.secrets[secret_key]:
            os.environ[env_key] = str(st.secrets[secret_key])

try:
    _bootstrap_secrets()
except Exception:
    pass  # Local dev without secrets.toml — fine, falls back to .env or empty


# ---------------------------------------------------------------------------
# Background workflow runner
# ---------------------------------------------------------------------------
class WorkflowRunner:
    """Runs the LangGraph in a background thread, exposing progress for UI polling."""

    def __init__(self):
        self.progress = 0
        self.status_message = "准备就绪"
        self.html_report: str | None = None
        self.markdown_report: str | None = None
        self.error: str | None = None
        self._done = False

    @property
    def done(self) -> bool:
        return self._done

    def start(self, industry: str) -> None:
        t = threading.Thread(target=self._run, args=(industry,), daemon=True)
        t.start()

    def _run(self, industry: str) -> None:
        async def _async_run():
            from workflow.graph import create_research_graph

            graph = create_research_graph()
            initial = {
                "industry": industry,
                "search_results": [],
                "financial_analysis": "",
                "markdown_report": "",
                "html_report": "",
                "progress": 0,
                "status_message": "启动中...",
                "error": None,
            }
            async for event in graph.astream(initial):
                for output in event.values():
                    if not isinstance(output, dict):
                        continue
                    self.progress = output.get("progress", self.progress)
                    self.status_message = output.get(
                        "status_message", self.status_message
                    )
                    self.error = output.get("error") or self.error
                    if "html_report" in output:
                        self.html_report = output["html_report"]
                    if "markdown_report" in output:
                        self.markdown_report = output["markdown_report"]
            self._done = True

        try:
            asyncio.run(_async_run())
        except Exception as e:
            self.error = str(e)
            self._done = True


# ---------------------------------------------------------------------------
# Page Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Aegis · 产业投研引擎",
    page_icon="⚡",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Full-page Dark Futuristic CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ── Global Reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ── Dark Background with Grid ── */
    .stApp {
        background: #0a0a0f;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(59, 130, 246, 0.12), transparent),
            linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
        background-size: 100% 100%, 60px 60px, 60px 60px;
    }

    /* ── Hide default chrome ── */
    #MainMenu, footer, header,
    [data-testid="stSidebarNav"],
    .stDeployButton {
        display: none !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 18, 0.95);
        backdrop-filter: blur(24px);
        border-right: 1px solid rgba(59, 130, 246, 0.15);
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #94a3b8 !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(30, 30, 50, 0.8);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 10px;
        color: #e2e8f0;
    }
    [data-testid="stSidebar"] input {
        background: rgba(30, 30, 50, 0.8) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }

    /* ── Hero Section ── */
    .hero-container {
        text-align: center;
        padding: 4rem 1rem 2.5rem 1rem;
        position: relative;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 16px;
        border-radius: 999px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        background: rgba(59, 130, 246, 0.08);
        color: #60a5fa;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-bottom: 1.5rem;
        text-transform: uppercase;
    }
    .hero-badge::before {
        content: '';
        width: 6px; height: 6px;
        border-radius: 50%;
        background: #3b82f6;
        box-shadow: 0 0 8px #3b82f6;
        animation: pulse-dot 2s ease-in-out infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.4); }
    }
    .hero-title {
        font-size: clamp(2.2rem, 5vw, 3.8rem);
        font-weight: 900;
        letter-spacing: -0.04em;
        line-height: 1.1;
        background: linear-gradient(135deg, #f8fafc 0%, #60a5fa 50%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #64748b;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.7;
    }
    .hero-subtitle strong {
        color: #94a3b8;
        font-weight: 600;
    }

    /* ── Text Input ── */
    .stTextInput > div > div > input {
        background: rgba(15, 15, 25, 0.9) !important;
        border: 1px solid rgba(59, 130, 246, 0.25) !important;
        border-radius: 14px !important;
        padding: 1rem 1.25rem !important;
        font-size: 1.05rem !important;
        color: #e2e8f0 !important;
        box-shadow: 0 0 0 0 transparent, inset 0 2px 4px rgba(0,0,0,0.3);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.15), 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #475569 !important;
    }
    .stTextInput label {
        color: #94a3b8 !important;
        font-weight: 500 !important;
    }

    /* ── Quick-select Chip Buttons ── */
    .stButton > button:not([kind="primary"]) {
        background: rgba(30, 30, 50, 0.6) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 10px !important;
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 0.55rem 0.8rem !important;
        transition: all 0.25s ease !important;
        backdrop-filter: blur(8px);
    }
    .stButton > button:not([kind="primary"]):hover {
        border-color: #3b82f6 !important;
        color: #60a5fa !important;
        background: rgba(59, 130, 246, 0.08) !important;
        box-shadow: 0 0 16px rgba(59, 130, 246, 0.12) !important;
        transform: translateY(-1px);
    }

    /* ── Primary CTA Button ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #6366f1 50%, #8b5cf6 100%) !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.9rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        color: white !important;
        letter-spacing: 0.02em;
        box-shadow: 0 8px 30px -6px rgba(59, 130, 246, 0.45);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 14px 40px -8px rgba(99, 102, 241, 0.55) !important;
    }
    .stButton > button[kind="primary"]:active {
        transform: translateY(0) !important;
    }

    /* ── Progress Bar ── */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #3b82f6) !important;
        background-size: 200% 100%;
        animation: shimmer 2s linear infinite;
        border-radius: 999px;
    }
    .stProgress > div > div {
        background: rgba(30, 30, 50, 0.8) !important;
        border-radius: 999px;
        height: 6px !important;
    }
    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    /* ── Status / Info boxes ── */
    .stAlert {
        background: rgba(15, 15, 25, 0.85) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 12px !important;
        color: #cbd5e1 !important;
        backdrop-filter: blur(12px);
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: rgba(15, 15, 25, 0.8);
        border-radius: 14px;
        padding: 4px;
        border: 1px solid rgba(59, 130, 246, 0.15);
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        color: #64748b;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(59, 130, 246, 0.12) !important;
        color: #60a5fa !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background: rgba(59, 130, 246, 0.12) !important;
        border-radius: 10px;
    }

    /* ── Download buttons in results ── */
    .stDownloadButton > button {
        background: rgba(30, 30, 50, 0.7) !important;
        border: 1px solid rgba(59, 130, 246, 0.25) !important;
        border-radius: 10px !important;
        color: #60a5fa !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
    }
    .stDownloadButton > button:hover {
        background: rgba(59, 130, 246, 0.12) !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.15) !important;
    }

    /* ── Pipeline Steps ── */
    .pipeline-bar {
        display: flex;
        gap: 2px;
        margin: 2rem 0;
        padding: 0 1rem;
    }
    .pipeline-step {
        flex: 1;
        text-align: center;
        padding: 1rem 0.5rem;
        border-radius: 10px;
        background: rgba(20, 20, 35, 0.8);
        border: 1px solid rgba(59, 130, 246, 0.1);
        transition: all 0.4s ease;
        position: relative;
    }
    .pipeline-step.active {
        border-color: #3b82f6;
        background: rgba(59, 130, 246, 0.08);
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.1);
    }
    .pipeline-step.done {
        border-color: rgba(34, 197, 94, 0.4);
        background: rgba(34, 197, 94, 0.06);
    }
    .pipeline-step .step-icon {
        font-size: 1.4rem;
        margin-bottom: 0.4rem;
    }
    .pipeline-step .step-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .pipeline-step.active .step-title {
        color: #60a5fa;
    }
    .pipeline-step.done .step-title {
        color: #4ade80;
    }
    .pipeline-step .step-connector {
        position: absolute;
        right: -8px;
        top: 50%;
        transform: translateY(-50%);
        color: #1e293b;
        font-size: 0.7rem;
        z-index: 1;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(59, 130, 246, 0.1) !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a0a0f; }
    ::-webkit-scrollbar-thumb { background: rgba(59, 130, 246, 0.3); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(59, 130, 246, 0.5); }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar — Config Only
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 1rem 0;">
        <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">⚡</div>
        <div style="font-size: 1.2rem; font-weight: 800; color: #e2e8f0; letter-spacing: -0.02em;">Aegis Engine</div>
        <div style="font-size: 0.75rem; color: #475569; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase;">产业投研引擎 v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔧 引擎配置")

    current_key = os.environ.get("OPENROUTER_API_KEY", "")
    api_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        value=current_key,
        placeholder="sk-or-v1-…",
        help="已从云端预配置，无需手动输入",
    )
    if api_key:
        os.environ["OPENROUTER_API_KEY"] = api_key.strip()

    model = st.selectbox(
        "推理引擎",
        [
            "openai/gpt-oss-120b:free",
            "meta-llama/llama-3.3-70b-instruct:free",
            "google/gemini-2.0-flash-exp:free",
            "qwen/qwen-2.5-72b-instruct:free",
            "deepseek/deepseek-chat:free",
        ],
        index=0,
    )
    os.environ["LLM_MODEL"] = model

    st.markdown("---")
    st.markdown("""
    <div style="padding: 0.8rem; border-radius: 10px; border: 1px solid rgba(59,130,246,0.15); background: rgba(59,130,246,0.04);">
        <div style="display:flex; align-items:center; gap:6px; margin-bottom:6px;">
            <span style="width:6px;height:6px;border-radius:50%;background:#22c55e;box-shadow:0 0 6px #22c55e;"></span>
            <span style="color:#94a3b8; font-size:0.78rem; font-weight:600;">PIPELINE ONLINE</span>
        </div>
        <div style="color:#475569; font-size:0.75rem; line-height:1.6;">
            LangGraph 多节点流转<br/>
            AnySearch 实时聚合<br/>
            多模型推理融合
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">Live · Research Engine</div>
    <div class="hero-title">产业投研自动驾驶舱</div>
    <div class="hero-subtitle">
        基于 <strong>LangGraph</strong> 多智能体编排，实时聚合全网公开研报数据，
        驱动深度推理大模型生成机构级产业研究报告
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
if "industry_input" not in st.session_state:
    st.session_state.industry_input = ""

industry = st.text_input(
    "研究课题",
    placeholder="输入行业关键词，如：光模块 CPO、固态电池、人形机器人…",
    key="industry_input",
)

def _set_example(value: str):
    st.session_state.industry_input = value

examples = ["光模块 CPO", "固态电池", "人形机器人", "低空经济", "AI 算力芯片"]
cols = st.columns(len(examples))
for i, ex in enumerate(examples):
    with cols[i]:
        st.button(ex, key=f"ex_{i}", use_container_width=True, on_click=_set_example, args=(ex,))

st.write("")

RUN_KEY = "workflow_runner"
if RUN_KEY not in st.session_state:
    st.session_state[RUN_KEY] = None

col_btn, _ = st.columns([1, 3])
with col_btn:
    start_clicked = st.button(
        "⚡ 启动深度研报生成", type="primary", disabled=not industry.strip()
    )

if start_clicked and industry.strip():
    runner = WorkflowRunner()
    runner.start(industry.strip())
    st.session_state[RUN_KEY] = runner


# ---------------------------------------------------------------------------
# Pipeline visualization helper
# ---------------------------------------------------------------------------
STEPS = [
    ("🔌", "初始化"),
    ("🔍", "聚合搜索"),
    ("📊", "财报剖析"),
    ("✍️", "报告撰写"),
    ("🎨", "渲染导出"),
]

def render_pipeline(active_idx: int, all_done: bool = False):
    """Render the futuristic pipeline bar."""
    parts = []
    for i, (icon, title) in enumerate(STEPS):
        if all_done:
            cls = "done"
        elif i < active_idx:
            cls = "done"
        elif i == active_idx:
            cls = "active"
        else:
            cls = ""
        connector = '<span class="step-connector">›</span>' if i < len(STEPS) - 1 else ""
        parts.append(f"""
        <div class="pipeline-step {cls}">
            <div class="step-icon">{icon}</div>
            <div class="step-title">{title}</div>
            {connector}
        </div>""")
    st.markdown(f'<div class="pipeline-bar">{"".join(parts)}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Progress & Results
# ---------------------------------------------------------------------------
runner: WorkflowRunner | None = st.session_state[RUN_KEY]

if runner is not None and not runner.done:
    import time

    pipeline_ph = st.empty()
    status_ph = st.empty()
    progress_bar = st.progress(0)

    while not runner.done:
        pct = runner.progress
        idx = 0
        if pct >= 10: idx = 1
        if pct >= 40: idx = 2
        if pct >= 65: idx = 3
        if pct >= 90: idx = 4

        with pipeline_ph.container():
            render_pipeline(idx)

        progress_bar.progress(pct / 100.0)

        with status_ph.container():
            if runner.error:
                st.error(f"⛔ 异常阻断：{runner.error}")
            else:
                st.info(f"⏳ {runner.status_message}  ·  {pct}%")

        if runner.error:
            break
        time.sleep(0.3)

    progress_bar.progress(1.0)
    if runner.error:
        st.session_state[RUN_KEY] = None
    else:
        status_ph.empty()
        pipeline_ph.empty()
        st.rerun()

if runner is not None and runner.done and not runner.error:
    render_pipeline(4, all_done=True)
    st.markdown("---")

    tab_html, tab_md = st.tabs(["🌐 交互式 Web 视图", "📝 Markdown 源码"])

    with tab_html:
        if runner.html_report:
            st.download_button(
                "📥 导出 HTML 报告",
                data=runner.html_report,
                file_name=f"{industry}_产业研报.html",
                mime="text/html",
            )
            import streamlit.components.v1 as components
            st.markdown(
                '<div style="border-radius:12px; overflow:hidden; border:1px solid rgba(59,130,246,0.15); margin-top:1rem;">',
                unsafe_allow_html=True,
            )
            components.html(runner.html_report, height=800, scrolling=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("无 HTML 输出")

    with tab_md:
        if runner.markdown_report:
            st.download_button(
                "📥 导出 Markdown",
                data=runner.markdown_report,
                file_name=f"{industry}_产业研报.md",
                mime="text/markdown",
            )
            st.markdown(runner.markdown_report)
        else:
            st.warning("Markdown 报告为空")

    st.write("")
    if st.button("🔄 重置工作区"):
        st.session_state[RUN_KEY] = None
        st.rerun()
