# AgriAgent

AI assistant for small farms. Built with Python, LangChain, IBM WatsonX, and Streamlit.

## What it does

Routes natural language requests to 4 workflows:
- **LOG** - Record farm activities (sales, purchases, harvests)
- **QUERY** - Ask questions about logged data
- **REPORT** - Generate summaries from logged data
- **GENERAL** - General farming advice

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

**Web UI:**
```bash
streamlit run app.py
```

**CLI:**
```bash
python main.py
```

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

Built for IBM WatsonX hackathon. Demonstrates intent-based routing architecture with enterprise LLM integration.
