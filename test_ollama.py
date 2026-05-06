"""
Test script to verify Ollama connection
"""
import requests

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    try:
        # Use port 11435
        response = requests.get("http://127.0.0.1:11435/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running!")
            models = response.json().get("models", [])
            if models:
                print("📦 Available models:")
                for model in models:
                    print(f"   - {model.get('name')}")
            else:
                print("⚠️ No models found. Run: ollama pull llama2")
            return True
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Make sure it's running.")
        print("   Start Ollama with: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_model_generation():
    """Test if model can generate responses"""
    try:
        payload = {
            "model": "llama2",
            "prompt": "Hello",
            "stream": False
        }
        response = requests.post("http://127.0.0.1:11435/api/generate", json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Model generation successful!")
            print(f"Response: {result.get('response', '')[:100]}...")
            return True
        else:
            print(f"❌ Generation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Ollama Setup...\n")
    
    if test_ollama_connection():
        print("\n📝 Testing model generation...")
        test_model_generation()
    else:
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure Ollama is installed")
        print("2. Start Ollama: ollama serve")
        print("3. Pull a model: ollama pull llama2")