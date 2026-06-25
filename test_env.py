import os
from dotenv import load_dotenv

load_dotenv()  # This magically loads the variables from the .env file

api_key = os.getenv("MY_API_KEY")
model = os.getenv("MY_MODEL")

assert api_key is not None, "❌ MY_API_KEY non chargée"
assert api_key.startswith("sk-"), "❌ Format inattendu"
assert model == "gemini-2.5-flash"

print(f"✅ Key loaded: {api_key[:8]}... (hidden for safety)")
print(f"✅ Model loaded: {model}")

