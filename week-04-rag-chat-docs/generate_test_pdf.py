import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_sample_pdf(filename="document_test.pdf"):
    print(f"Creation du PDF d'exemple '{filename}'...")
    
    # Configuration du document PDF
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6366f1'),
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#a855f7'),
        spaceBefore=15,
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=12
    )

    story = []

    # PAGE 1 : Introduction aux Systèmes Multi-Agents
    story.append(Paragraph("Systèmes Multi-Agents (SMA)", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Page 1 — Introduction et Concepts Clés", heading_style))
    story.append(Paragraph(
        "Un système multi-agents (SMA) est un système composé de plusieurs agents autonomes "
        "qui interagissent entre eux pour résoudre des problèmes complexes qu'un seul agent "
        "ne pourrait pas résoudre facilement. Ces agents peuvent être des logiciels informatiques, "
        "des robots ou même des humains.",
        body_style
    ))
    story.append(Paragraph(
        "Les propriétés principales d'un agent autonome incluent l'autonomie (capacité de prendre des décisions), "
        "la réactivité (réagir aux changements de son environnement), la proactivité (prendre l'initiative) "
        "et la sociabilité (communiquer et coopérer avec les autres agents). Les interactions au sein d'un SMA "
        "peuvent être coopératives (les agents travaillent ensemble vers un but commun) ou compétitives "
        "(les agents ont des intérêts conflictuels, comme dans les enchères).",
        body_style
    ))
    story.append(PageBreak())  # Force le passage à la page suivante

    # PAGE 2 : Protocoles de Consensus
    story.append(Paragraph("Protocoles de Consensus", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Page 2 — Paxos, Raft et Accord Distribué", heading_style))
    story.append(Paragraph(
        "Dans les systèmes distribués et multi-agents, le consensus est une exigence critique. "
        "Les agents doivent s'accorder sur un état commun ou une valeur partagée en présence de pannes.",
        body_style
    ))
    story.append(Paragraph(
        "Le protocole Raft est une alternative moderne à Paxos, conçue pour être plus facile à comprendre. "
        "Raft décompose le consensus en trois sous-problèmes principaux : l'élection du leader, la réplication des logs "
        "et la sécurité. À tout moment, chaque agent (nœud) se trouve dans l'un de ces trois états : leader, suiveur (follower) "
        "ou candidat. Le leader gère toutes les demandes des clients et coordonne la duplication des journaux système.",
        body_style
    ))
    story.append(PageBreak())

    # PAGE 3 : Latence et Performances
    story.append(Paragraph("Performances et Latence Réseau", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Page 3 — Évaluation et Limites Physiques", heading_style))
    story.append(Paragraph(
        "L'efficacité globale d'un système multi-agents dépend fortement de l'infrastructure de communication. "
        "La latence réseau, qui est le retard accumulé lors de la transmission des données, joue un rôle déterminant.",
        body_style
    ))
    story.append(Paragraph(
        "Pour évaluer les performances d'un SMA, nous mesurons plusieurs métriques clés :\n"
        "1. Le temps de convergence (le temps nécessaire pour que tous les agents s'accordent sur une décision).\n"
        "2. La bande passante utilisée (le volume total de messages échangés).\n"
        "3. La robustesse aux pannes d'agents (la capacité du système à continuer de fonctionner si 30% des agents s'arrêtent brutalement).",
        body_style
    ))
    story.append(Paragraph(
        "Une latence élevée ou des pertes de paquets sur le réseau peuvent paralyser la prise de décision et entraîner "
        "des divergences d'état entre les agents.",
        body_style
    ))

    # Génération du fichier
    doc.build(story)
    print(f"PDF cree avec succes a l'emplacement : {os.path.abspath(filename)}")

if __name__ == "__main__":
    create_sample_pdf()
