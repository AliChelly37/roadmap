import os
from dotenv import load_dotenv
import google.generativeai as genai
import instructor
from pydantic import BaseModel

# Charge les variables du fichier .env
load_dotenv()

class UserInfo(BaseModel):
    name: str
    age: int

# Récupère la clé depuis ton fichier .env (il faut qu'elle s'appelle GEMINI_API_KEY)
# ou change le nom de la variable si elle s'appelle autrement.
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Erreur: Clé GEMINI_API_KEY non trouvée dans le .env")
    exit(1)

genai.configure(api_key=api_key)

# On enveloppe le client Gemini avec instructor
client = instructor.from_gemini(
    client=genai.GenerativeModel(model_name="models/gemini-3.5-flash"),
    mode=instructor.Mode.GEMINI_JSON,
)

# Note: la méthode pour appeler Gemini via instructor est `.messages.create()`
user_info = client.messages.create(
    response_model=UserInfo,
    messages=[
        {"role": "user", "content": "je m'appelle Jean et j'ai 32 ans."}
    ]
)

print("Nom :", user_info.name)
print("Age :", user_info.age)
print("Type :", type(user_info))
