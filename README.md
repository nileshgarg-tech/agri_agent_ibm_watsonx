# AgriAgent

An interactive database for small farms. Log operations, query your data, and generate reports - all through natural language.

> Built during IBM WatsonX Hackathon (June 2025) • Refactored & improved (January 2026)  
> **Version 0.1** - Simple, practical tool for daily farm operations

## What it does

An AI-powered operations assistant that routes natural language requests to 4 workflows:
- **LOG** - Record farm activities (sales, purchases, harvests, expenses)
- **QUERY** - Ask questions about your logged data
- **REPORT** - Generate weekly/monthly summaries and aggregations
- **GENERAL** - General farming advice and conversations

**Think of it as:** An interactive database where each farmer can log their operations and query them naturally, without SQL or spreadsheets.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with IBM WatsonX credentials (see `ENV_SETUP.txt`):
```env
WATSONX_URL=https://us-south.ml.cloud.ibm.com
PROJECT_ID=your_project_id
WATSONX_APIKEY=your_api_key
```

3. Create data folder:
```bash
mkdir data
```

4. Test setup:
```bash
python test_setup.py
```

See `EXAMPLES.md` for usage examples.

## Run

**Web UI (Local):**
```bash
streamlit run app.py
```

**Web UI (Deployed):**
Visit: https://agri-agent-ibm-watsonx.streamlit.app

**CLI:**
```bash
python main.py
```

See `DEPLOYMENT.md` for deployment instructions.

## Project Structure

```
agri-agent/
├── app.py                  # Streamlit web interface
├── main.py                 # CLI interface
├── langchain_config.py     # IBM WatsonX LLM setup
├── routing_prompt.txt      # Intent classifier prompt
├── json_storage.py         # User data persistence
└── workflows/              # 4 modular workflows
    ├── log_flow.py
    ├── query_flow.py
    ├── report_flow.py
    └── general_flow.py
```

## Tech Stack

- Python 3.11+
- LangChain 0.3
- IBM WatsonX Granite-13B
- Streamlit
- JSON storage

## How it works

1. User input → Intent classifier (LLM-based)
2. Routes to appropriate workflow
3. Workflow processes with specialized prompt
4. Returns response

**What makes it unique:** Intent-based routing with IBM WatsonX Granite models. Each farmer gets their own isolated data store (JSON files). Simple, practical, and built to work within IBM Cloud constraints.

**Not fancy, but functional** - A working v0.1 that solves real problems for small farmers.
