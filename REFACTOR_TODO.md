# Refactoring Roadmap

Work needed before this is portfolio-ready (2-3 days):

## 1. LangChain Version Compatibility
- Current: Using LangChain 0.3 (langchain-core, langchain-ibm)
- **Check**: Are we using any deprecated patterns?
- **Action**: Test if current code works with latest versions
- **Consider**: Modern tool calling patterns if needed

## 2. Data Storage
- Current: JSON files per user (`data/{user}_data.json`)
- **Issues**: 
  - No schema validation
  - No indexing or search beyond loading everything
  - Scalability concerns
- **Options**:
  - Keep JSON but add validation
  - Move to SQLite for better querying
  - Add vector DB for semantic search

## 3. API Connectivity
- Current: IBM WatsonX Granite-13B
- **Unknown**: 
  - Does it actually work with current credentials?
  - Error handling robust?
  - Rate limits?
- **Action**: Test live API calls, add proper error handling

## 4. Deployment
- Current: Local only (streamlit run / python main.py)
- **Needed**:
  - Dockerfile
  - Environment variable management
  - Production WSGI server (if needed)
  - Cloud deployment guide (Streamlit Cloud, Heroku, Railway, etc)
  - Or just good local setup instructions

## Testing Priority
1. Does it run at all? (verify venv, imports, .env)
2. Does IBM WatsonX API work?
3. Does data logging/querying work?
4. Does the web UI work?

Then refactor based on what's broken.
