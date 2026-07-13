import os
import httpx
from dotenv import load_dotenv

load_dotenv()
account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
api_key = os.getenv("CLOUDFLARE_API_KEY")

if not account_id or not api_key:
    print("❌ Couldn't find CLOUDFLARE_ACCOUNT_ID or CLOUDFLARE_API_KEY in your .env file!")
    exit()

print("Key loaded! Asking Cloudflare to say 'OK'...")

# Ask Cloudflare's Llama 3 model
response = httpx.post(
    f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3.1-8b-instruct",
    headers={"Authorization": f"Bearer {api_key}"},
    json={"messages": [{"role": "user", "content": "In one short sentence, why are open source models like Llama 3 important?"}]},
    timeout=30
)

if response.status_code == 200:
    print("✅ Cloudflare replied:", response.json()["result"]["response"].strip())
else:
    print("❌ API Error:", response.status_code)
    print(response.text)
