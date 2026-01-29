# Deployment Guide

## Streamlit Cloud Deployment

AgriAgent is ready to deploy on Streamlit Cloud at **agri-agent-ibm-watsonx.streamlit.app**

### Steps:

1. **Push to GitHub** (already done)
   ```bash
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"

3. **Configure App**
   - Repository: `nileshgarg-tech/AGRI-AGENT`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: `agri-agent-ibm-watsonx`

4. **Add Secrets**
   Click "Advanced settings" → "Secrets" and paste:
   ```toml
   WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
   PROJECT_ID = "your_actual_project_id"
   WATSONX_APIKEY = "your_actual_api_key"
   ```
   
   (Get these from your IBM WatsonX account)

5. **Deploy**
   - Click "Deploy!"
   - Wait 2-3 minutes for build
   - App will be live at: https://agri-agent-ibm-watsonx.streamlit.app

### Important Notes:

- **Data Persistence**: User data is stored in JSON files but will reset on each redeploy (Streamlit Cloud has ephemeral storage). For production, consider using:
  - Streamlit's `st.session_state` for session data
  - External database (Supabase, Firebase, etc.)
  - Cloud storage (S3, Google Cloud Storage)

- **Secrets**: Never commit `.env` or secrets.toml to GitHub. Always use Streamlit Cloud's Secrets management.

- **Python Version**: Streamlit Cloud uses Python 3.11 by default. Our requirements.txt is compatible.

### Troubleshooting:

**App won't start:**
- Check "App logs" in Streamlit Cloud dashboard
- Verify all secrets are configured correctly
- Ensure IBM WatsonX credentials are valid

**Import errors:**
- Check requirements.txt has all dependencies
- Streamlit Cloud rebuilds on each push

**Data not persisting:**
- Expected behavior - see "Data Persistence" note above
- Data persists during a session but resets on redeploy

### Local Testing:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials
# (see ENV_SETUP.txt)

# Run locally
streamlit run app.py
```

## Alternative Deployments:

### Docker (for self-hosting):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t agri-agent .
docker run -p 8501:8501 --env-file .env agri-agent
```

### Railway / Render:

Similar process to Streamlit Cloud - connect GitHub repo, set environment variables, deploy.

---

**Deploy URL:** https://agri-agent-ibm-watsonx.streamlit.app  
**Status:** Ready to deploy
