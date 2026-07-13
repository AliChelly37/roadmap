import os
import httpx
from dotenv import load_dotenv
from google import genai
import ollama

load_dotenv()

def chat(prompt, provider="gemini"):
    """
    Sends a prompt to the specified provider and returns the text response.
    Providers supported: 'gemini', 'cloudflare', 'ollama'
    """
    
    if provider == "gemini":
        # 1. TODO: Use your gemini-3.5-flash code here
        # return the response text
        client = genai.Client()

        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
        )

        return response.text

    elif provider == "cloudflare":
        # 2. TODO: Use your Cloudflare httpx code here (Llama 3.1)
        # return the response text
        cf_account = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        cf_key = os.getenv("CLOUDFLARE_API_KEY")

        response = httpx.post(
            f"https://api.cloudflare.com/client/v4/accounts/{cf_account}/ai/run/@cf/meta/llama-3.1-8b-instruct",
            headers={"Authorization": f"Bearer {cf_key}"},
            json={"messages": [{"role": "user", "content": prompt}]},
            timeout=30.0
        )

        data = response.json()
        return data["result"]["response"]

    elif provider == "ollama":
        # 3. Here is a freebie for Ollama! The library is super simple:
        response = ollama.chat(model='llama3.1', messages=[
            {'role': 'user', 'content': prompt}
        ])
        return response['message']['content']

    else:
        return "Unknown provider!"

# === TEST YOUR FUNCTION ===
if __name__ == "__main__":
    test_prompt = "What is the capital of France? Answer in one word."
    
    print("🤖 GEMINI:")
    print(chat(test_prompt, provider="gemini"))
    print("-" * 30)
    
    print("☁️ CLOUDFLARE:")
    print(chat(test_prompt, provider="cloudflare"))
    print("-" * 30)

    print("🦙 OLLAMA:")
    print(chat(test_prompt, provider="ollama"))
