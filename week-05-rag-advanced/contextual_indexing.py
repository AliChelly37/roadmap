import os
import sys
import fitz  # PyMuPDF
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from pathlib import Path
from dotenv import load_dotenv

# Setup paths
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
dotenv_path = ROADMAP_ROOT / ".env"
load_dotenv(dotenv_path)

# Configuration
WEEK4_PATH = ROADMAP_ROOT / "week-04-rag-chat-docs"
PDF_FILE = str(WEEK4_PATH / "document_test.pdf")
DB_PATH = str(WEEK4_PATH / "chroma_db")
COLLECTION_NAME = "rag_contextual_test"
MODEL_NAME = "intfloat/multilingual-e5-base"

def main():
    print(f"Connexion au document '{PDF_FILE}'...")
    if not os.path.exists(PDF_FILE):
        print(f"Erreur : Le fichier PDF '{PDF_FILE}' n'existe pas.")
        sys.exit(1)
        
    doc = fitz.open(PDF_FILE)
    
    # 1. Extraire l'intégralité du texte du document pour le contexte global
    entire_document_text = ""
    for page_idx in range(len(doc)):
        entire_document_text += f"\n--- Page {page_idx+1} ---\n"
        entire_document_text += doc.load_page(page_idx).get_text()
        
    print(f"Texte intégral extrait ({len(entire_document_text)} caractères).")

    # 2. Initialisation d'Ollama pour générer les headers
    print("Initialisation du modèle Ollama llama3.1 pour générer les headers...")
    llm = ChatOpenAI(
        model="llama3.1",
        api_key="ollama",
        base_url="http://localhost:11434/v1",
        temperature=0
    )

    # 3. Découpage en morceaux
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )
    
    all_chunks = []
    all_metadatas = []
    all_ids = []
    
    print("\nGénération des headers contextuels (Anthropic style) page par page...")
    
    for page_idx in range(len(doc)):
        page = doc.load_page(page_idx)
        page_text = page.get_text()
        page_num = page_idx + 1
        
        chunks = text_splitter.split_text(page_text)
        print(f"\nPage {page_num} : découpée en {len(chunks)} morceaux.")
        
        for local_idx, chunk in enumerate(chunks):
            clean_chunk = chunk.replace("\t", "    ").strip()
            if len(clean_chunk) < 15:
                continue
                
            # Prompt Anthropic pour générer le contexte
            prompt = f"""Tu es un assistant sémantique spécialisé dans l'indexation.
Voici le document complet :
<document>
{entire_document_text}
</document>

Voici un court morceau extrait du document :
<chunk>
{clean_chunk}
</chunk>

Génère une explication de contexte extrêmement courte (1 phrase, maximum 35 mots) pour situer ce morceau dans le document. Cette explication doit indiquer de quel document et de quel sujet précis parle ce morceau.
Donne uniquement l'explication générée, sans introduction, sans commentaire.
Exemple : "Ce morceau fait partie de document_test.pdf, dans la section élection du leader de Raft, décrivant comment les nœuds initient le vote."
"""
            
            try:
                print(f"  [Morceau {local_idx+1}/{len(chunks)}] Génération du header...")
                response = llm.invoke(prompt)
                header = response.content.strip().replace("\n", " ")
                print(f"    Header : {header}")
            except Exception as e:
                print(f"    Erreur lors de la génération du header : {e}")
                header = f"Ce morceau provient de document_test.pdf à la page {page_num}."

            # Fusionner le header et le morceau
            contextualized_text = f"Contexte : {header}\n\nMorceau de texte : {clean_chunk}"
            
            # Préfixe E5
            formatted_chunk = f"passage: {contextualized_text}"
            
            all_chunks.append(formatted_chunk)
            all_metadatas.append({
                "source": "document_test.pdf",
                "page": page_num,
                "local_chunk_idx": local_idx,
                "context_header": header
            })
            all_ids.append(f"ctx_chunk_p{page_num}_{local_idx}")

    # 4. Ingestion dans ChromaDB
    print(f"\nConnexion à Chroma DB dans '{DB_PATH}'...")
    client = chromadb.PersistentClient(path=DB_PATH)
    sbert_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
    
    # Supprimer la collection si elle existe déjà
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(name=COLLECTION_NAME)
        
    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=sbert_fn
    )
    
    print(f"Indexation des {len(all_chunks)} morceaux contextualisés dans '{COLLECTION_NAME}'...")
    collection.add(
        ids=all_ids,
        documents=all_chunks,
        metadatas=all_metadatas
    )
    print(f"Indexation complétée ! La collection '{COLLECTION_NAME}' contient {collection.count()} chunks.")

if __name__ == "__main__":
    main()
