import os
import sys
import json
import fitz  # PyMuPDF
from pathlib import Path
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma as LangchainChroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb

# Setup paths
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
dotenv_path = ROADMAP_ROOT / ".env"
load_dotenv(dotenv_path)

# Configuration
WEEK4_PATH = ROADMAP_ROOT / "week-04-rag-chat-docs"
PDF_FILE = str(WEEK4_PATH / "document_test.pdf")
DB_PATH = str(WEEK4_PATH / "chroma_db")
COLLECTION_NAME = "rag_document_test"
MODEL_NAME = "intfloat/multilingual-e5-base"
GRAPH_FILE = str(Path(__file__).parent / "knowledge_graph.json")

class KnowledgeGraph:
    def __init__(self):
        self.triplets = []
        
    def add_triplet(self, subject: str, relation: str, obj: str):
        self.triplets.append({
            "subject": subject.strip(),
            "relation": relation.strip(),
            "object": obj.strip()
        })
        
    def save(self, file_path: str):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.triplets, f, indent=2, ensure_ascii=False)
            
    def load(self, file_path: str):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.triplets = json.load(f)
                
    def query_entity(self, entity_name: str) -> list[str]:
        """
        Trouve tous les triplets liés à l'entité recherchée (insensible à la casse, match par mot clé).
        """
        results = []
        entity_lower = entity_name.lower().strip()
        # Séparer en mots significatifs (longueur > 3)
        words = [w.strip() for w in entity_lower.split() if len(w.strip()) > 3]
        if not words:
            words = [entity_lower]
            
        for t in self.triplets:
            match = False
            for w in words:
                if w in t["subject"].lower() or w in t["object"].lower():
                    match = True
                    break
            if match:
                rel_str = f"- {t['subject']} ➔ [{t['relation']}] ➔ {t['object']}"
                results.append(rel_str)
        return results

def extract_json_array(text: str) -> list:
    text = text.strip()
    start = text.find('[')
    end = text.rfind(']')
    if start != -1 and end != -1:
        json_str = text[start:end+1]
        try:
            return json.loads(json_str)
        except Exception:
            pass
    return []

def build_knowledge_graph():
    print(f"Extraction des triplets pour construire le Graphe de Connaissances...")
    doc = fitz.open(PDF_FILE)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    
    all_text = ""
    for page in doc:
        all_text += page.get_text()
        
    chunks = text_splitter.split_text(all_text)
    print(f"Découpage en {len(chunks)} morceaux pour analyse du graphe.")
    
    llm = ChatOpenAI(
        model="llama3.1",
        api_key="ollama",
        base_url="http://localhost:11434/v1",
        temperature=0
    )
    
    graph = KnowledgeGraph()
    
    for idx, chunk in enumerate(chunks):
        print(f"  [Chunk {idx+1}/{len(chunks)}] Extraction des entités & relations...")
        prompt = f"""Tu es un extracteur d'entités et de relations sémantiques.
Analyse le paragraphe ci-dessous et extrais-en les entités clés (noms propres, concepts, protocoles) et les relations directes qui les lient sous forme de liste de triplets JSON.

Format de sortie strict attendu (uniquement le JSON, sans commentaire, sans markdown):
[
  {{"subject": "nom de l'entité 1", "relation": "verbe ou type de lien", "object": "nom de l'entité 2"}}
]

Paragraphe à analyser :
<paragraph>
{chunk}
</paragraph>
"""
        try:
            response = llm.invoke(prompt)
            content = response.content.strip()
            triplets = extract_json_array(content)
            for t in triplets:
                if "subject" in t and "relation" in t and "object" in t:
                    graph.add_triplet(t["subject"], t["relation"], t["object"])
                    
        except Exception as e:
            print(f"    Erreur lors de l'extraction sur le chunk {idx+1} : {e}")
            
    print(f"Extraction terminée : {len(graph.triplets)} triplets extraits.")
    graph.save(GRAPH_FILE)
    print(f"Graphe de connaissances enregistré dans {GRAPH_FILE}")
    return graph

class GraphAugmentedRAG:
    def __init__(self):
        # Initialisation du Graphe de Connaissances
        self.graph = KnowledgeGraph()
        if not os.path.exists(GRAPH_FILE):
            self.graph = build_knowledge_graph()
        else:
            print(f"Chargement du Graphe de Connaissances existant depuis {GRAPH_FILE}...")
            self.graph.load(GRAPH_FILE)
            
        # Initialisation du retriever vectoriel Chroma
        print("Initialisation du retriever vectoriel...")
        self.embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
        self.chroma_client = chromadb.PersistentClient(path=DB_PATH)
        self.vectorstore = LangchainChroma(
            client=self.chroma_client,
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings
        )
        self.llm = ChatOpenAI(
            model="llama3.1",
            api_key="ollama",
            base_url="http://localhost:11434/v1",
            temperature=0
        )

    def query(self, question: str) -> str:
        print(f"\nRequête GraphRAG : '{question}'")
        
        # 1. Extraction des entités clés de la question à l'aide d'Ollama
        entity_prompt = f"""Identifie le sujet ou l'entité centrale de la question suivante.
Réponds uniquement avec le nom sémantique de l'entité, sans aucun autre mot.

Question : {question}
Sujet :"""
        try:
            entity_response = self.llm.invoke(entity_prompt)
            entity = entity_response.content.strip().replace('"', '')
            print(f"Entité clé identifiée : '{entity}'")
        except Exception as e:
            entity = "Raft"
            print(f"Erreur détection d'entité, valeur par défaut : '{entity}'")

        # 2. Requête dans le Graphe de Connaissances
        graph_contexts = self.graph.query_entity(entity)
        print(f"Relations trouvées dans le graphe pour '{entity}' : {len(graph_contexts)}")
        graph_context_str = "\n".join(graph_contexts)

        # 3. Requête dans la base Vectorielle
        prefixed_query = f"query: {question}"
        vector_docs = self.vectorstore.similarity_search(prefixed_query, k=3)
        vector_texts = []
        for idx, doc in enumerate(vector_docs):
            text = doc.page_content
            if text.startswith("passage: "):
                text = text[len("passage: "):]
            vector_texts.append(f"Document {idx+1} [Source: {doc.metadata.get('source', 'document')}, Page: {doc.metadata.get('page', 0)}]:\n{text}")
        vector_context_str = "\n\n".join(vector_texts)

        # 4. Combiner Graphe + Vecteur dans le prompt
        prompt = f"""Tu es un assistant de lecture IA factuel et extrêmement précis.
Réponds à la question de l'utilisateur en te basant sur le Graphe de Connaissances (relations conceptuelles) et le Contexte Vectoriel (extraits de texte) fournis ci-dessous.

<graphe_connaissances>
{graph_context_str}
</graphe_connaissances>

<contexte_vectoriel>
{vector_context_str}
</contexte_vectoriel>

Consignes de Grounding strictes :
1. N'invente aucun fait hors de ces deux contextes.
2. Pour chaque affirmation, cite la source (ex: [nom_du_fichier.pdf, Page X] ou [Graphe de connaissances]).

Question : {question}
Réponse :"""

        print("\nGénération de la réponse finale...")
        response = self.llm.invoke(prompt)
        return response.content

if __name__ == "__main__":
    rag = GraphAugmentedRAG()
    # Test avec une question sémantique complexe
    answer = rag.query("Qu'est-ce que le protocole Raft et en quoi se distingue-t-il de Paxos ?")
    print("\n--- REPONSE ANCREE GraphRAG ---")
    print(answer)
    print("-------------------------------\n")
