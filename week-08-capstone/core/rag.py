import os
import re
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi

# Le corpus est vendu dans l'image (knowledge/) : il doit vivre à l'intérieur du
# contexte de build Docker. Auparavant ce chemin remontait de 4 niveaux vers le
# vault Obsidian, qui n'existe pas dans le conteneur -> 0 document indexé.
KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
DB_PATH = Path(__file__).resolve().parent.parent / "chroma_db"

# Le corpus est en FRANÇAIS. all-MiniLM-L6-v2 (90 Mo) est un modèle anglophone :
# il avait été choisi pour tenir dans les 512 Mo du free tier Render. Sur HF Spaces
# (CPU basic = 16 Go de RAM) cette contrainte disparaît, donc on repasse sur un
# modèle multilingue (~470 Mo) qui comprend réellement les requêtes en français.
EMBED_MODEL = os.environ.get("EMBED_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")

# Taille de chunk visée (caractères). Les paragraphes sont regroupés jusqu'à ce seuil.
CHUNK_TARGET_CHARS = int(os.environ.get("CHUNK_TARGET_CHARS", "500"))

# Nombre max de chunks provenant d'un même fichier dans un résultat (diversité).
MAX_CHUNKS_PER_SOURCE = 2

# Nombre de chunks renvoyés à l'agent. Source unique de vérité : l'outil ET l'éval
# lisent cette constante, pour qu'on ne mesure jamais une configuration qui ne part
# pas en production.
DEFAULT_N_RESULTS = 5

# Garde « je ne sais pas » (brique de la Semaine 4, S4-J5-T1) : en dessous de ce
# seuil de proximité, aucun passage n'est jugé pertinent et on refuse de répondre.
#
# Le seuil n'est pas choisi au jugé. Distances mesurées sur ce corpus :
#   dans le corpus  : 0.32 -> 0.41
#   hors du corpus  : 0.57 -> 0.80
# 0.50 tombe dans l'écart, avec de la marge des deux côtés.
RELEVANCE_THRESHOLD = float(os.environ.get("RELEVANCE_THRESHOLD", "0.50"))

# Renvoyé à l'agent quand rien n'est pertinent. Le texte est explicite parce que
# c'est un modèle 8B qui le lit : il doit être impossible à interpréter autrement.
NO_RELEVANT_CONTENT = (
    "AUCUN_PASSAGE_PERTINENT — la question ne correspond à aucun mémo de la "
    "formation. Tu dois répondre que le sujet n'est pas couvert par les notes, "
    "et NE PAS répondre depuis tes connaissances générales."
)


def get_collection():
    """Initialise et retourne la collection ChromaDB pour le RAG."""
    client = chromadb.PersistentClient(path=str(DB_PATH))

    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)

    # get_or_create_collection pour ne pas crasher si elle existe déjà
    collection = client.get_or_create_collection(
        name="roadmap_knowledge",
        embedding_function=ef
    )
    return collection


def week_from_filename(name: str):
    """Numéro de semaine d'un mémo, ou None s'il est transverse.

    Le corpus est constitué des mémos rédigés pendant la formation :
    `S5-J2-Memo-Reranking.md` -> 5, `semaine-8.md` -> 8, et
    `Memo-Guardrails.md` -> None (notion transverse, hors semaine).
    """
    match = re.match(r"^S(\d)\b", name) or re.match(r"^semaine-(\d)", name)
    return int(match.group(1)) if match else None


def _chunk_markdown(content: str, source: str):
    """Découpe un markdown en chunks porteurs de leur contexte.

    Reprend le principe des « contextual chunk headers » vu en Semaine 5 : chaque
    chunk est préfixé par son fichier et son titre de section. Sans ça, un chunk
    isolé (une ligne de tableau, une citation) est indistinguable du même
    boilerplate présent dans les autres fichiers.
    """
    chunks = []
    heading = ""
    buffer = []
    buffer_len = 0

    def flush():
        nonlocal buffer, buffer_len
        if not buffer:
            return
        body = "\n".join(buffer).strip()
        if len(body) > 50:
            prefix = f"[{source} > {heading}]" if heading else f"[{source}]"
            chunks.append((f"{prefix}\n{body}", heading))
        buffer = []
        buffer_len = 0

    # Découpage ligne à ligne, et non bloc à bloc : dans ces fichiers un titre et
    # sa liste ne sont séparés que d'un seul \n, donc un split("\n\n") mettait le
    # titre ET tout son contenu dans le même bloc — contenu qui était alors jeté
    # avec le titre. C'est ce qui rendait « reranking » introuvable.
    for line in content.split("\n"):
        stripped = line.strip()

        if stripped.startswith("#"):
            flush()
            heading = stripped.lstrip("#").strip()
            continue

        # Ligne vide = frontière de paragraphe : on coupe si le chunk est assez gros.
        if not stripped:
            if buffer_len >= CHUNK_TARGET_CHARS:
                flush()
            continue

        buffer.append(stripped)
        buffer_len += len(stripped)
        # Garde-fou : une longue table sans ligne vide ne doit pas tout avaler.
        if buffer_len >= CHUNK_TARGET_CHARS * 2:
            flush()

    flush()
    return chunks

def index_roadmap_files():
    """Indexe tous les fichiers markdown de la roadmap dans ChromaDB."""
    collection = get_collection()
    
    # On évite de réindexer si c'est déjà fait
    if collection.count() > 0:
        print(f"[RAG] Base déjà indexée avec {collection.count()} documents.")
        return

    print("[RAG] Début de l'indexation de la roadmap...")
    docs = []
    metadatas = []
    ids = []
    
    doc_id = 0
    if not KNOWLEDGE_DIR.is_dir():
        raise FileNotFoundError(
            f"Corpus introuvable : {KNOWLEDGE_DIR}. "
            "Le dossier knowledge/ doit être présent (il est copié dans l'image Docker)."
        )

    # Parcourir les fichiers de la roadmap
    for md_file in sorted(KNOWLEDGE_DIR.glob("*.md")):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            for p_id, (chunk, heading) in enumerate(_chunk_markdown(content, md_file.stem)):
                docs.append(chunk)
                metadatas.append({
                    "source": md_file.name,
                    "heading": heading,
                    "chunk_id": p_id,
                    # 0 = transverse : Chroma n'accepte pas None en métadonnée.
                    "week": week_from_filename(md_file.name) or 0,
                })
                ids.append(f"doc_{doc_id}")
                doc_id += 1

        except Exception as e:
            print(f"Erreur de lecture {md_file.name}: {e}")

    if not docs:
        raise RuntimeError(
            f"0 chunk extrait de {KNOWLEDGE_DIR}. L'assistant répondrait sans "
            "connaissances : on échoue au build plutôt qu'en production."
        )

    # Ajout par lots pour éviter les limites
    batch_size = 100
    for i in range(0, len(docs), batch_size):
        collection.add(
            documents=docs[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
            ids=ids[i:i+batch_size]
        )
    print(f"[RAG] Indexation terminée : {doc_id} chunks indexés.")

# --- Recherche hybride (brique reprise de la Semaine 5, query_hybrid.py) ---------
# Le dense seul rate les termes techniques rares ("LangGraph", "reranking") : un
# modèle de paraphrase encode mal les noms propres. BM25 les retrouve exactement.
# Formule RRF de la S5 (k=60), mais rééquilibrée à 0.5/0.5 : les poids d'origine
# étaient réglés sur un corpus PDF, pas sur ce curriculum (voir README).
_BM25_CACHE = {}


def _tokenize(text: str):
    """Tokenisation simple compatible français (accents conservés)."""
    return re.findall(r"\w+", text.lower(), flags=re.UNICODE)


def _get_bm25():
    """Construit (une seule fois) l'index BM25 à partir des documents Chroma."""
    if "index" in _BM25_CACHE:
        return _BM25_CACHE["index"], _BM25_CACHE["docs"], _BM25_CACHE["metas"]

    data = get_collection().get()
    docs = data.get("documents") or []
    metas = data.get("metadatas") or []
    index = BM25Okapi([_tokenize(d) for d in docs]) if docs else None

    _BM25_CACHE.update({"index": index, "docs": docs, "metas": metas})
    return index, docs, metas


DENSE_WEIGHT = float(os.environ.get("DENSE_WEIGHT", "0.5"))
SPARSE_WEIGHT = float(os.environ.get("SPARSE_WEIGHT", "0.5"))


def _reciprocal_rank_fusion(dense, sparse, k=60,
                            dense_weight=None, sparse_weight=None):
    """Fusionne deux classements par Reciprocal Rank Fusion.

    `dense` et `sparse` sont des listes de (texte, metadata) déjà triées.
    """
    dense_weight = DENSE_WEIGHT if dense_weight is None else dense_weight
    sparse_weight = SPARSE_WEIGHT if sparse_weight is None else sparse_weight

    scores, payload = {}, {}
    for weight, ranking in ((dense_weight, dense), (sparse_weight, sparse)):
        for rank, (text, meta) in enumerate(ranking, start=1):
            key = text.strip()
            payload.setdefault(key, (text, meta))
            scores[key] = scores.get(key, 0.0) + weight * (1.0 / (k + rank))

    ordered = sorted(scores, key=scores.get, reverse=True)
    return [payload[key] for key in ordered]


def search_roadmap(query: str, n_results: int = DEFAULT_N_RESULTS) -> str:
    """Recherche hybride (dense + BM25, fusion RRF) dans la roadmap."""
    collection = get_collection()
    
    # On récupère large de chaque côté (top-10), puis RRF resserre sur n_results.
    candidates = max(n_results * 3, 10)

    # A. Dense. Pas de préfixe "query:" : convention E5, pas MiniLM. Les documents
    #    sont indexés bruts, la requête doit l'être aussi.
    results = collection.query(query_texts=[query], n_results=candidates)
    dense = list(zip(
        results.get("documents", [[]])[0],
        results.get("metadatas", [[]])[0],
    ))

    # Garde de pertinence AVANT toute fusion : si le meilleur passage dense est
    # trop loin, le corpus ne parle pas du sujet. Sans ça le modèle recevait des
    # extraits hors sujet et répondait quand même depuis ses connaissances
    # générales — il a répondu « Sydney » à la capitale de l'Australie, ce qui
    # est en prime faux.
    distances = (results.get("distances") or [[]])[0]
    if not distances or min(distances) > RELEVANCE_THRESHOLD:
        return NO_RELEVANT_CONTENT

    # B. Sparse (BM25) — rattrape les correspondances lexicales exactes.
    sparse = []
    index, all_docs, all_metas = _get_bm25()
    if index is not None:
        scored = sorted(
            enumerate(index.get_scores(_tokenize(query))),
            key=lambda pair: pair[1],
            reverse=True,
        )
        sparse = [
            (all_docs[i], all_metas[i] if i < len(all_metas) else {})
            for i, score in scored[:candidates] if score > 0
        ]

    # C. Fusion, puis diversification par source. roadmap_0.md est la table des
    #    matières : elle ressemble à *toutes* les questions sur la roadmap et
    #    saturait le top-k, évinçant le fichier de la semaine réellement visée.
    #    On plafonne donc à 2 chunks par fichier.
    fused = []
    per_source = {}
    for doc, meta in _reciprocal_rank_fusion(dense, sparse):
        source = (meta or {}).get("source", "?")
        if per_source.get(source, 0) >= MAX_CHUNKS_PER_SOURCE:
            continue
        per_source[source] = per_source.get(source, 0) + 1
        fused.append((doc, meta))
        if len(fused) == n_results:
            break

    if not fused:
        return "Aucune information trouvée dans la roadmap."

    formatted_docs = []
    for doc, meta in fused:
        meta = meta or {}
        source = meta.get("source", "Inconnue")
        heading = meta.get("heading", "")
        # Le tag de semaine est lu par l'UI pour ses pastilles de provenance.
        week = meta.get("week") or 0
        tag = f"[S{week}] " if week else "[transverse] "
        label = f"{tag}{source} > {heading}" if heading else f"{tag}{source}"
        formatted_docs.append(f"Source: {label}\nContenu:\n{doc}")

    return "\n\n---\n\n".join(formatted_docs)

if __name__ == "__main__":
    # Test unitaire rapide
    index_roadmap_files()
    print("Test de recherche :", search_roadmap("Qu'est-ce que LiteLLM ?"))
