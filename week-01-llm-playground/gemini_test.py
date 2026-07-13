import os
from dotenv import load_dotenv
from google import genai
from google.genai import types # <-- Add this new import!

load_dotenv()
client = genai.Client()

response = client.models.generate_content(
    model='gemini-3.5-flash',
    contents='Tell me a story about a token that got lost in a neural network.',
    config=types.GenerateContentConfig(
        system_instruction="You are an angry, impatient AI who hates explaining things. Respond entirely in uppercase.",
        temperature=0.7,
        max_output_tokens=150
    )
)

print(response.text)
