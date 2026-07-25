from prompt_template import PromptTemplate

# 1. création de notre template

template = PromptTemplate(
    system_prompt="Tu es traducteur expert. Traduis le texte fourni en $langue.",
    examples= [
        {"user": "<user_input>Hello</user_input>","assistant":"bonjour"}
    ]
)

#2. on génère les messages finaux pour l'utilisation actuel

messages = template.format_messages(
    langue="espagnol",
    user_input="How are you?"
)
print(messages)
