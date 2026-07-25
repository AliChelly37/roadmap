from string import Template
from typing import List, Dict, Optional

class PromptTemplate:
    """
    Une classe pour gérer les templates de prompts avec System Prompt, Few-Shot examples
    et injection de variables dynamiques, tout en retournant le format OpenAI standard.
    """
    def __init__(self, system_prompt: str, examples: Optional[List[Dict[str, str]]] = None):
        """
        :param system_prompt: Le prompt système de base (peut contenir des variables comme $langue)
        :param examples: Liste optionnelle de dictionnaires pour le few-shot.
                         Ex: [{"user": "input 1", "assistant": "output 1"}]
        """
        self.system_prompt = system_prompt
        self.examples = examples or []

    def format_messages(self, **kwargs) -> List[Dict[str, str]]:
        """
        Construit la liste de messages finale pour l'API (OpenAI, Ollama, Groq, etc.)
        :param kwargs: Les variables à injecter dans le template (ex: user_input="Texte", langue="français")
        """
        messages = []
        
        # 1. Traitement du System Prompt (injection sécurisée des variables)
        sys_template = Template(self.system_prompt)
        # safe_substitute ignore les variables non fournies sans faire crasher l'app
        formatted_sys = sys_template.safe_substitute(**kwargs)
        messages.append({"role": "system", "content": formatted_sys})
        
        # 2. Ajout des exemples Few-Shot (s'il y en a)
        for ex in self.examples:
            if "user" in ex:
                messages.append({"role": "user", "content": ex["user"]})
            if "assistant" in ex:
                messages.append({"role": "assistant", "content": ex["assistant"]})
                
        # 3. Ajout du message utilisateur final
        # Si un "user_input" est fourni, on l'encadre avec des balises XML
        if "user_input" in kwargs:
            user_content = f"<user_input>\n{kwargs['user_input']}\n</user_input>"
            messages.append({"role": "user", "content": user_content})
            
        return messages
