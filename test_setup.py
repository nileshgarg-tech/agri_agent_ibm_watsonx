"""
Quick test script to verify setup is correct.
Run: python test_setup.py
"""
import sys

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import langchain
        print("✓ langchain")
        import langchain_ibm
        print("✓ langchain_ibm")
        import streamlit
        print("✓ streamlit")
        import dotenv
        print("✓ python-dotenv")
        print("\n✅ All packages installed correctly!")
        return True
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def test_env():
    """Test if .env file exists and has required variables"""
    print("\nTesting environment variables...")
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        required_vars = ["WATSONX_URL", "PROJECT_ID", "WATSONX_APIKEY"]
        missing = []
        
        for var in required_vars:
            value = os.getenv(var)
            if not value or value.startswith("your_"):
                missing.append(var)
                print(f"✗ {var} - not set")
            else:
                print(f"✓ {var} - set")
        
        if missing:
            print(f"\n⚠️  Missing or placeholder values: {', '.join(missing)}")
            print("See ENV_SETUP.txt for instructions")
            return False
        
        print("\n✅ All environment variables configured!")
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_data_dir():
    """Test if data directory exists"""
    print("\nTesting data directory...")
    import os
    if os.path.exists("data"):
        print("✓ data/ directory exists")
        return True
    else:
        print("✗ data/ directory missing")
        print("Run: mkdir data")
        return False

if __name__ == "__main__":
    print("=== AgriAgent Setup Test ===\n")
    
    results = []
    results.append(test_imports())
    results.append(test_env())
    results.append(test_data_dir())
    
    print("\n" + "="*30)
    if all(results):
        print("🎉 Setup complete! Ready to run.")
        print("\nNext steps:")
        print("  - Web UI: streamlit run app.py")
        print("  - CLI: python main.py")
    else:
        print("⚠️  Some issues need fixing. See above.")
        sys.exit(1)
