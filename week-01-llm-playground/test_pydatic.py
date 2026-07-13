from pydantic import BaseModel, ValidationError
#syntax de base 
class Article(BaseModel):
    # Champ obligatoire (pas de valeur par défaut)
    title: str 
    word_count: int 
    
    # Champ optionnel (on utilise "Type | None" et on donne None par défaut)
    author: str | None = None 
    
    # Liste (obligatoire, mais peut être une liste vide)
    tags: list[str]

# Création d'un article
doc = Article(title="Tutoriel Pydantic", word_count=500, tags=["python", "ai"])
print(doc.title) # Affiche: Tutoriel Pydantic

# Pydantic est intelligent : il voit que "1200" est une string, 
# mais comme le modèle attend un entier, il va le convertir automatiquement !
doc2 = Article(title="News", word_count="1200", tags=[])
print(type(doc2.word_count)) # <class 'int'>

# Par contre, si la donnée est impossible à convertir...
# doc3 = Article(title="News", word_count="mille", tags=[])
# ❌ Ça va lever une "ValidationError: Input should be a valid integer..."

#nested models : on peut mettre un modèle Pydantic à l'intérieur d'un autre
class Company(BaseModel):
    name: str
    location: str

class JobPosting(BaseModel):
    title: str
    salary: int | None = None
    # Le champ "company" doit être un objet qui respecte le modèle Company
    company: Company  

# Instanciation
my_job = JobPosting(
    title="AI Engineer", 
    company=Company(name="TechCorp", location="Paris")
)

print(my_job.company.name)

#export de données
# 1. Obtenir un dictionnaire Python classique :
mon_dict = my_job.model_dump() 
# {'title': 'AI Engineer', 'salary': None, 'company': {'name': 'TechCorp', 'location': 'Paris'}}

# 2. Obtenir une chaîne de caractères JSON directement :
mon_json = my_job.model_dump_json()
# '{"title":"AI Engineer","salary":null,"company":{"name":"TechCorp","location":"Paris"}}'
print(mon_json,mon_dict)
print(type(mon_json),type(mon_dict))

class User(BaseModel):
    id: int
    name: str
    age: int | None = None
# On passe des mauvaises données volontairement
donnees_invalides = {
    "id": "pas-un-entier", # Mauvais type
    # "name" est manquant !
    "age": "vingt" # Ne peut pas être converti en int
}
try:
    # On unpack le dictionnaire avec **
    user = User(**donnees_invalides) 
    
except ValidationError as e:
    # 1. Tu peux printer l'erreur formatée directement (très lisible)
    print("--- L'erreur complète ---")
    print(e)
    
    # 2. Tu peux extraire les attributs structurés avec .errors()
    # Ça te renvoie une liste de dictionnaires, un par champ en erreur !
    print("\n--- Les détails des erreurs ---")
    erreurs = e.errors()
    
    for erreur in erreurs:
        print(f"Champ posant problème : {erreur['loc']}")
        print(f"Type d'erreur       : {erreur['type']}")
        print(f"Message pour l'user : {erreur['msg']}\n")