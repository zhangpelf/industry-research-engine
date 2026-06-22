## 评估定义: 研报生成核心工作流 (Report Generation Workflow)

### 能力评估 (Capability Evals)
1. 工作流初始化: 能够成功构建 LangGraph 并返回可执行图 (Runnable)
2. 基础研报生成: 输入有效行业词汇后，能够最终输出内容丰富的 Markdown 报告
3. HTML转换能力: 能够将 Markdown 成功转译为带有自定义 CSS 的 HTML 报告

### 回归评估 (Regression Evals)
1. 界面加载: Streamlit 主程序 `app.py` 无语法/导入错误
2. 依赖健康: 所有 `workflow/nodes` 能够成功被导入

### 成功指标
- 能力评估: pass@1 = 100%
- 回归评估: pass^1 = 100%
