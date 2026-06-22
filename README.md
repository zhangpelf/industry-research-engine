# 📊 行业研究报告自动生成器

基于 **LangGraph** + **Streamlit** 的行业研究报告自动生成工具。输入行业名称，自动搜索、分析并输出专业HTML研报。

## 功能

- 输入行业名称（如"光模块 CPO"、"固态电池"、"人形机器人"）
- 自动搜索 DuckDuckGo 获取实时信息
- LLM 分析产业链结构、市场规模、竞争格局
- 生成结构化 Markdown 研报
- 输出精美 HTML，支持下载

## 工作流

```
用户输入行业名称
    ↓
[LangGraph] search_reports   — DuckDuckGo 搜索
    ↓
[LangGraph] analyze_financials — LLM 财务分析
    ↓
[LangGraph] write_report     — LLM 研报撰写
    ↓
[LangGraph] render_html      — HTML 渲染
    ↓
用户查看/下载报告
```

## 快速开始

### 1. 配置 API

```bash
cp .env.example .env
# 编辑 .env，填入你的 LLM API Key
# OPENROUTER_API_KEY=sk-xxx
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行

```bash
streamlit run app.py
```

浏览器打开 http://localhost:8501

### Docker

```bash
docker build -t industry-report .
docker run -p 8501:8501 --env-file .env industry-report
```

## 目录结构

```
industry-research-app/
├── app.py                    # Streamlit 入口
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── utils/
│   ├── llm.py                # LLM 客户端（OpenRouter）
│   └── search.py             # DuckDuckGo 搜索
├── workflow/
│   ├── state.py              # TypedDict 状态定义
│   ├── graph.py              # LangGraph 图组装
│   └── nodes/
│       ├── search_reports.py
│       ├── analyze_financials.py
│       ├── write_report.py
│       └── render_html.py
└── templates/
    ├── report_template.py    # HTML 模板渲染
    └── industry_report.html  # 模板文件
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 前端 | Streamlit |
| 工作流 | LangGraph (StateGraph) |
| 搜索 | DuckDuckGo (duckduckgo-search) |
| LLM | OpenRouter (兼容 OpenAI API) |
| 渲染 | markdown + 自定义 HTML 模板 |

## 免责声明

本工具生成的内容仅供参考，不构成任何投资建议。报告中的数据和观点来自公开信息搜索和 AI 分析，可能存在不准确之处。
