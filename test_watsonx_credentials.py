"""
TEMPORARY TEST FILE - DELETE AFTER VERIFYING CREDENTIALS
Tests if IBM WatsonX credentials are valid and working.
"""
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get credentials
watsonx_url = os.getenv("WATSONX_URL")
project_id = os.getenv("PROJECT_ID")
apikey = os.getenv("WATSONX_APIKEY")

print("=" * 50)
print("IBM WatsonX Credentials Test")
print("=" * 50)

# Check if credentials exist
print("\n1. Checking if credentials are set...")
if not watsonx_url:
    print("[ERROR] WATSONX_URL not found")
elif not project_id:
    print("[ERROR] PROJECT_ID not found")
elif not apikey:
    print("[ERROR] WATSONX_APIKEY not found")
else:
    print("[OK] All credentials found in .env")
    print(f"   URL: {watsonx_url}")
    print(f"   Project ID: {project_id[:10]}..." if len(project_id) > 10 else f"   Project ID: {project_id}")
    #print(f"   API Key: {apikey[:10]}..." if len(apikey) > 10 else f"   API Key: {apikey}")

# Try to import and initialize LLM
print("\n2. Testing LLM initialization...")
try:
    from langchain_ibm import WatsonxLLM
    
    # Using granite-4-h-small (recommended replacement)
    llm = WatsonxLLM(
        model_id="ibm/granite-4-h-small",
        url=watsonx_url,
        project_id=project_id,
        apikey=apikey,
        params={
            "max_new_tokens": 150,
            "temperature": 0.0
        }
    )
    print("[OK] LLM initialized successfully")
except Exception as e:
    print(f"[ERROR] Failed to initialize LLM: {e}")
    exit(1)

# Try a simple test call
print("\n3. Testing API call...")
try:
    test_prompt = "Best LLM model in 2025"
    print(f"   Prompt: '{test_prompt}'")
    response = llm.invoke(test_prompt)
    print(f"[OK] API call successful!")
    print(f"   Response: {response}")
    print("\n" + "=" * 50)
    print("[SUCCESS] ALL TESTS PASSED - Credentials are valid!")
    print("=" * 50)
except Exception as e:
    print(f"[ERROR] API call failed: {e}")
    print("\n" + "=" * 50)
    print("[FAILED] CREDENTIALS TEST FAILED")
    print("=" * 50)
    print("\nPossible issues:")
    print("- Credentials expired or invalid")
    print("- Wrong project ID")
    print("- API key doesn't have access")
    print("- Network/connection issue")
    exit(1)
