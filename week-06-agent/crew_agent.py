import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Setup paths
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
dotenv_path = ROADMAP_ROOT / ".env"
load_dotenv(dotenv_path)

from langchain_community.tools import DuckDuckGoSearchRun
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import chromadb
from chromadb.utils import embedding_functions

# 1. Outils

@tool
def web_search(query: str) -> str:
    """Searches the web for information using DuckDuckGo. Use this tool to get up-to-date facts."""
    print(f"\n[OUTIL CREW] Recherche Web pour : '{query}'...")
    try:
        ddg = DuckDuckGoSearchRun()
        return ddg.invoke(query)
    except Exception as e:
        return f"Erreur de recherche : {e}"

@tool
def scrape_url(url: str) -> str:
    """Scrapes and extracts all text content from a web page URL. Use this to read details of specific pages."""
    print(f"\n[OUTIL CREW] Scraping URL : '{url}'...")
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for s in soup(["script", "style"]):
            s.decompose()
        text = soup.get_text(separator=' ')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text[:3500]
    except Exception as e:
        return f"Erreur de scraping : {e}"

@tool
def search_my_docs(query: str) -> str:
    """Searches our local database of technical documents. Use this first for topics related to Raft, multi-agents, or consensus."""
    print(f"\n[OUTIL CREW] Recherche RAG local pour : '{query}'...")
    try:
        db_path = str(ROADMAP_ROOT / "week-04-rag-chat-docs" / "chroma_db")
        client = chromadb.PersistentClient(path=db_path)
        sbert_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-base")
        collection = client.get_collection(name="rag_document_test", embedding_function=sbert_fn)
        results = collection.query(
            query_texts=[f"query: {query}"],
            n_results=3
        )
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        if not documents:
            return "Aucun document local pertinent trouvé."
        formatted_docs = []
        for idx, doc in enumerate(documents):
            meta = metadatas[idx] if idx < len(metadatas) else {}
            formatted_docs.append(f"Document {idx+1} [Page {meta.get('page', 'Inconnue')}]:\n{doc}")
        return "\n\n".join(formatted_docs)
    except Exception as e:
        return f"Erreur d'accès RAG local : {e}"

@tool
def save_markdown(content: str, filename: str) -> str:
    """Saves the final report as a markdown file on the local machine."""
    print(f"\n[OUTIL CREW] Sauvegarde du rapport dans '{filename}'...")
    try:
        output_dir = Path(__file__).parent
        filepath = output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Rapport sauvegardé avec succès dans '{filepath.resolve()}' !"
    except Exception as e:
        return f"Erreur de sauvegarde : {e}"

# 2. Initialisation du LLM local (Ollama)
llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434",
    temperature=0
)

# 3. Déclaration des Agents CrewAI
researcher = Agent(
    role="Expert Document and Web Researcher",
    goal="Find precise, accurate, and detailed facts about the topic: {topic}",
    backstory="You are an expert analytical researcher who knows how to find hidden facts, read technical papers, and query local databases or the web to build a solid factual basis.",
    tools=[search_my_docs, web_search, scrape_url],
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Senior Technical Writer",
    goal="Synthesize researched facts into a structured, clear, and comprehensive markdown report about {topic}",
    backstory="You are a professional technical writer who organizes complex technical jargon into structured, clear, and easy-to-read markdown sections with titles, comparison tables, and logical paragraphs.",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Critical Editor and Reviewer",
    goal="Review the draft report, identify gaps, vague claims, or missing sources, perform final corrections, and save it to the local filesystem.",
    backstory="You are a strict technical editor. You proofread drafts, demand source attribution for assertions, ensure all requirements are addressed in depth, and write the finalized markdown file.",
    tools=[save_markdown],
    llm=llm,
    verbose=True
)

# 4. Déclaration des Tâches CrewAI

research_task = Task(
    description="Conduct deep research on the topic: '{topic}' using both local documents (via search_my_docs) and web search (via web_search). Extract raw facts and citations.",
    expected_output="A structured log of findings, raw facts, and citations related to the topic.",
    agent=researcher
)

write_task = Task(
    description="Based on the researcher's findings, write a comprehensive, professional, and structured technical report in markdown about: '{topic}'. Do not invent facts, only use the research log.",
    expected_output="A complete draft of the report in markdown format.",
    agent=writer
)

review_task = Task(
    description="Review the markdown draft. Identify any gaps, vague sections, or missing sources. Correct these elements, refine the structure, and save the finalized report as a markdown file named '{filename}'.",
    expected_output="The finalized, edited markdown report saved on the local filesystem.",
    agent=reviewer
)

# 5. Compilation de la Crew
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, write_task, review_task],
    process=Process.sequential,
    verbose=True
)

def run_crew(topic: str, filename: str = "rapport_crew_final.md"):
    print(f"\n=== LANCEMENT DE LA CREWAI POUR LE SUJET : '{topic}' ===")
    inputs = {
        "topic": topic,
        "filename": filename
    }
    result = crew.kickoff(inputs=inputs)
    print("\n--- RÉSULTAT FINAL CREW ---")
    print(result)

if __name__ == "__main__":
    run_crew(
        topic="Analyse des avantages du protocole Raft par rapport à Paxos dans les systèmes multi-agents",
        filename="rapport_raft_multi_agents_crew.md"
    )
