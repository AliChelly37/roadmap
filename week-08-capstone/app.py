import os
import re
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Charger les variables d'environnement (en local ; sur HF Spaces ce sont des Secrets)
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROADMAP_ROOT / ".env")

# Importer les modules locaux
from core.rag import index_roadmap_files
from core.observability import get_langfuse_handler, guardrail_check
from core.agent import graph, SYSTEM_PROMPT

# En Docker l'index est déjà construit au build : cet appel ne fait que le vérifier.
index_roadmap_files()
LANGFUSE_HANDLER = get_langfuse_handler()


# ---------------------------------------------------------------------------
# Le corpus est un parcours : 8 semaines, 4 phases. C'est la seule chose
# vraiment singulière de ce produit, donc c'est la seule chose qu'on colore.
# Le reste de l'interface reste monochrome.
# ---------------------------------------------------------------------------
PHASES = [
    ("Fondations",     (1, 2), "#4C6EF5"),
    ("Données & RAG",  (3, 5), "#0CA678"),
    ("Agents",         (6, 6), "#F08C00"),
    ("Production",     (7, 8), "#E03131"),
]
TRANSVERSE_COLOR = "#868E96"

WEEK_COLOR = {
    week: color
    for _, (start, end), color in PHASES
    for week in range(start, end + 1)
}


def _rail_html() -> str:
    """La carte du corpus : 8 semaines groupées en 4 phases.

    Ce n'est pas une décoration — c'est la structure réelle des documents
    interrogés, et les pastilles de source sous chaque réponse reprennent
    exactement ces couleurs.
    """
    groups = []
    for label, (start, end), color in PHASES:
        ticks = "".join(
            f'<span class="rail-week" style="--c:{color}">{w}</span>'
            for w in range(start, end + 1)
        )
        groups.append(
            f'<span class="rail-group"><span class="rail-weeks">{ticks}</span>'
            f'<span class="rail-label">{label}</span></span>'
        )
    return f'<div class="rail">{"".join(groups)}</div>'


def _source_chips(weeks, used_transverse: bool) -> str:
    """Provenance réelle de la réponse, une pastille par semaine consultée.

    Styles en ligne volontairement : le markdown du chatbot est rendu hors de
    la portée de notre feuille CSS, donc on ne dépend pas d'elle.
    """
    if not weeks and not used_transverse:
        return ""

    # Les mémos transverses (Git, garde-fous, system design) n'ont pas de position
    # sur le rail. Affichés à chaque fois ils ne porteraient aucune information :
    # on ne les montre que s'ils ont répondu seuls.
    if weeks:
        used_transverse = False

    base = ("display:inline-block;font-family:'IBM Plex Mono',ui-monospace,monospace;"
            "font-size:11px;font-weight:500;letter-spacing:.02em;padding:2px 8px;"
            "border-radius:999px;margin:0 4px 0 0;border:1px solid;")
    chips = "".join(
        f'<span style="{base}color:{WEEK_COLOR.get(w, TRANSVERSE_COLOR)};'
        f'border-color:{WEEK_COLOR.get(w, TRANSVERSE_COLOR)}33;'
        f'background:{WEEK_COLOR.get(w, TRANSVERSE_COLOR)}0f">S{w}</span>'
        for w in weeks
    )
    if used_transverse:
        chips += (f'<span style="{base}color:{TRANSVERSE_COLOR};'
                  f'border-color:{TRANSVERSE_COLOR}33;'
                  f'background:{TRANSVERSE_COLOR}0f">Transverse</span>')

    return (
        '\n\n<div style="margin-top:14px;padding-top:10px;'
        'border-top:1px solid rgba(128,134,150,.18)">'
        '<span style="font-family:\'IBM Plex Mono\',ui-monospace,monospace;font-size:10px;'
        'letter-spacing:.08em;text-transform:uppercase;color:#868E96;'
        'margin-right:8px">Sources</span>'
        f'{chips}</div>'
    )


def _history_to_messages(history):
    """Convertit l'historique Gradio (format 'messages') en messages LangChain."""
    messages = []
    for item in history or []:
        role, content = item.get("role"), item.get("content")
        if not content:
            continue
        # On retire les pastilles de source d'un tour précédent : c'est de
        # l'habillage, le modèle n'a pas à le relire.
        content = re.split(r"\n\n<div style=\"margin-top:14px", content)[0]
        messages.append(HumanMessage(content=content) if role == "user"
                        else AIMessage(content=content))
    return messages


def chat_function(message, history, request: gr.Request):
    # Garde-fou d'entrée (OWASP LLM01)
    if not guardrail_check(message):
        yield ("Cette requête cherche à modifier mes instructions, je ne peux pas la traiter. "
               "Pose ta question sur le contenu de la formation.")
        return

    # Un thread par session. C'était auparavant la constante "gradio_thread" :
    # sur un Space public, tous les visiteurs partageaient le même checkpointer
    # LangGraph, donc la mémoire de conversation de tout le monde.
    thread_id = getattr(request, "session_hash", None) or "anonymous"

    config = {"configurable": {"thread_id": thread_id}}
    if LANGFUSE_HANDLER is not None:
        config["callbacks"] = [LANGFUSE_HANDLER]

    initial_state = {
        "messages": [SystemMessage(content=SYSTEM_PROMPT)]
        + _history_to_messages(history)
        + [HumanMessage(content=message)]
    }

    full_response = ""
    weeks, used_transverse = set(), False

    try:
        for event in graph.stream(initial_state, config=config, stream_mode="updates"):
            for node_name, update in event.items():
                if node_name == "tools":
                    # Le contenu de l'outil dit quelles semaines ont réellement
                    # servi : c'est ce qui alimente les pastilles de source.
                    tool_text = str(update["messages"][-1].content)
                    weeks |= {int(w) for w in re.findall(r"\[S(\d)\]", tool_text)}
                    used_transverse = used_transverse or "[transverse]" in tool_text
                    yield "Consultation de la roadmap…"

                elif node_name == "agent":
                    agent_msg = update["messages"][-1]
                    if agent_msg.content:
                        full_response = agent_msg.content
                        yield full_response

        if not full_response:
            yield ("Je n'ai pas trouvé de quoi répondre. Reformule en visant une notion "
                   "précise de la formation — « reranking », « LangGraph », « chunking ».")
        else:
            yield full_response + _source_chips(sorted(weeks), used_transverse)

    except Exception as exc:
        # On n'expose pas la stack trace à l'utilisateur, mais on la log côté serveur.
        print(f"[ERREUR] {type(exc).__name__}: {exc}")
        yield ("Le service LLM ne répond pas. Réessaie dans un instant.")


# ---------------------------------------------------------------------------
# Thème
# ---------------------------------------------------------------------------
# Registre typographique volontairement « ingénierie » plutôt que « startup » :
# Space Grotesk pour les titres et les chiffres du rail, IBM Plex Sans pour la
# prose française (bon rendu des accents), IBM Plex Mono pour les métadonnées.
THEME = gr.themes.Base(
    primary_hue=gr.themes.Color(
        c50="#EEF1FE", c100="#DDE3FD", c200="#BCC7FB", c300="#9AABF9",
        c400="#798FF7", c500="#4C6EF5", c600="#3B57C4", c700="#2C4193",
        c800="#1E2C62", c900="#0F1631", c950="#080B18",
    ),
    neutral_hue=gr.themes.Color(
        c50="#FCFCFD", c100="#F4F5F8", c200="#E4E7EE", c300="#CBD0DB",
        c400="#9AA1B2", c500="#5B6274", c600="#454B5C", c700="#333849",
        c800="#222634", c900="#12141C", c950="#0B0D13",
    ),
    font=[gr.themes.GoogleFont("IBM Plex Sans"), "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("IBM Plex Mono"), "ui-monospace", "monospace"],
    radius_size=gr.themes.sizes.radius_md,
    text_size=gr.themes.sizes.text_md,
).set(
    body_background_fill="#FCFCFD",
    body_background_fill_dark="#0E1016",
    block_background_fill="transparent",
    block_background_fill_dark="transparent",
    block_border_width="0px",
    block_shadow="none",
    panel_background_fill="transparent",
    panel_background_fill_dark="transparent",
    input_background_fill="#FFFFFF",
    input_background_fill_dark="#171A22",
    input_border_color="#E4E7EE",
    input_border_color_dark="#262A35",
    input_shadow="none",
    button_primary_background_fill="#12141C",
    button_primary_background_fill_dark="#E8EAF0",
    button_primary_text_color="#FFFFFF",
    button_primary_text_color_dark="#12141C",
)

# Space Grotesk n'est pas dans le thème (Gradio ne gère que body + mono) : on le
# charge via <head>, avec repli sur la pile système si le réseau est coupé.
HEAD = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2'
    '?family=Space+Grotesk:wght@500;600;700&display=swap">'
)

CSS = """
:root {
  --ink: #12141C; --ink-2: #5B6274; --line: #E4E7EE;
  --surface: #FFFFFF; --paper: #FCFCFD;
  --display: 'Space Grotesk', 'IBM Plex Sans', system-ui, sans-serif;
  --mono: 'IBM Plex Mono', ui-monospace, monospace;
}
.dark {
  --ink: #E8EAF0; --ink-2: #9AA1B2; --line: #262A35;
  --surface: #171A22; --paper: #0E1016;
}

/* Colonne de lecture unique — la longueur de ligne prime sur le remplissage. */
.gradio-container { max-width: 100% !important; }
#app-shell { max-width: 47rem; margin: 0 auto; padding: 0 1.25rem; }

/* --- En-tête : le rail est la carte du corpus ------------------------------ */
#masthead { padding: 26px 0 18px; border-bottom: 1px solid var(--line); margin-bottom: 8px; }
#masthead h1 {
  font-family: var(--display); font-weight: 600; font-size: 1.0625rem;
  letter-spacing: -0.01em; color: var(--ink); margin: 0 0 2px;
}
#masthead p {
  font-size: 0.8125rem; color: var(--ink-2); margin: 0 0 16px; line-height: 1.5;
}
.rail { display: flex; gap: 22px; flex-wrap: wrap; align-items: flex-start; }
.rail-group { display: flex; flex-direction: column; gap: 5px; }
.rail-weeks { display: flex; gap: 3px; }
.rail-week {
  font-family: var(--mono); font-size: 10px; font-weight: 500; line-height: 1;
  color: var(--c); background: color-mix(in srgb, var(--c) 10%, transparent);
  border: 1px solid color-mix(in srgb, var(--c) 28%, transparent);
  border-radius: 4px; padding: 4px 6px; min-width: 18px; text-align: center;
}
.rail-label {
  font-family: var(--mono); font-size: 9px; letter-spacing: 0.07em;
  text-transform: uppercase; color: var(--ink-2);
}

/* --- Messages : prose à plat côté assistant, bulle discrète côté humain ---- */
#chat-area .message-row { padding: 0 !important; }
#chat-area .message.bot, #chat-area .bot {
  background: transparent !important; border: none !important;
  box-shadow: none !important; padding: 2px 0 !important;
}
#chat-area .message.user, #chat-area .user {
  background: var(--surface) !important; border: 1px solid var(--line) !important;
  border-radius: 14px !important; padding: 10px 14px !important;
}
#chat-area .message p { line-height: 1.68; }
#chat-area .message h1, #chat-area .message h2, #chat-area .message h3 {
  font-family: var(--display); letter-spacing: -0.01em;
}

/* --- Composer -------------------------------------------------------------- */
#chat-area textarea {
  font-size: 0.9375rem !important; line-height: 1.6 !important; padding: 12px 14px !important;
}
#chat-area textarea::placeholder { color: var(--ink-2); opacity: .75; }

footer, .built-with, .show-api { display: none !important; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
@media (max-width: 640px) { .rail { gap: 14px; } #app-shell { padding: 0 .875rem; } }
"""

EXAMPLES = [
    "Comment fonctionne le reranking avec un cross-encoder ?",
    "Quelle différence entre LangGraph et CrewAI ?",
    "Quelles stratégies de chunking pour un pipeline RAG ?",
    "Comment tracer un LLM en production ?",
]

# Gradio 6 : theme / css / head se passent à launch(), plus au constructeur.
with gr.Blocks(title="AI Roadmap Assistant",
               fill_height=True, analytics_enabled=False) as demo:
    with gr.Column(elem_id="app-shell"):
        gr.HTML(
            '<div id="masthead">'
            "<h1>AI Roadmap Assistant</h1>"
            "<p>Pose une question sur la formation AI Engineering. Les réponses sont "
            "tirées du corpus des 8 semaines, jamais des connaissances générales du modèle.</p>"
            f"{_rail_html()}"
            "</div>"
        )

        gr.ChatInterface(
            fn=chat_function,
            chatbot=gr.Chatbot(
                elem_id="chat-area",
                show_label=False,
                height=520,
                render_markdown=True,
                placeholder=(
                    "<div style='text-align:center;color:#5B6274;"
                    "font-family:IBM Plex Sans,system-ui,sans-serif'>"
                    "<div style='font-family:Space Grotesk,system-ui;font-size:15px;"
                    "font-weight:600;color:#12141C;margin-bottom:6px'>"
                    "Tes mémos, indexés.</div>"
                    "<div style='font-size:13px;line-height:1.6'>Demande une notion précise —&nbsp;"
                    "la réponse indiquera de quelle semaine elle vient.</div></div>"
                ),
            ),
            textbox=gr.Textbox(
                placeholder="Pose une question sur la formation…",
                submit_btn=True,
                show_label=False,
                lines=1,
                max_lines=6,
            ),
            examples=EXAMPLES,
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        theme=THEME,
        css=CSS,
        head=HEAD,
    )
