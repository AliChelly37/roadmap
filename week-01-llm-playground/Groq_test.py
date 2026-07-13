import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load your .env variables
load_dotenv()

# 2. Initialize the Groq client (it will automatically look for GROQ_API_KEY)
client = Groq()

# 3. Create a chat completion using Llama 3
# Note: Groq uses the exact same API structure as OpenAI!
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "In one short sentence, why are Groq LPUs so fast?",
        }
    ],
    # TODO: Fill in the model name! 
    # Hint: Check the Groq console for available models. A good one to use is "llama3-8b-8192"
    model="llama3-8b-8192", 
)

# 4. TODO: Print the response!
print(chat_completion.choices[0].message.content)
# Hint: In the OpenAI/Groq SDK, the text response is deeply nested inside the object.
# You will need to access: chat_completion.choices[0].message.content

