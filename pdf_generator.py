import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def build_cover_page(main_title, sub_title, cover_image_path, footer_image_path):
    """
    Construit la page de couverture avec le titre, le sous-titre, l'image de couverture et l'image de pied de page.
    """
    story = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("coverTitle", parent=styles["Title"], alignment=1, fontSize=40, leading=42)
    subtitle_style = ParagraphStyle("coverSubTitle", parent=styles["Title"], alignment=1, fontSize=24, leading=26)

    # Titre et sous-titre centrés avec espacement
    story.append(Spacer(1, 60))
    story.append(Paragraph(main_title, title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(sub_title, subtitle_style))
    story.append(Spacer(1, 40))

    # Image de couverture
    if cover_image_path and os.path.exists(cover_image_path):
        img = Image(cover_image_path, width=400, height=400)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 20))
    else:
        story.append(Spacer(1, 20))

    # Image de pied de page (footer)
    if footer_image_path and os.path.exists(footer_image_path):
        footer_img = Image(footer_image_path, width=70, height=70)
        footer_img.hAlign = 'RIGHT'
        story.append(Spacer(1, 40))
        story.append(footer_img)

    # Saut de page pour séparer la couverture du reste du contenu
    story.append(PageBreak())
    return story

def build_message_widgets(processed_messages):
    """
    Construit les "widgets" pour chaque message afin de simuler des bulles de discussion.
    Chaque message est présenté dans un Paragraph contenu dans une Table pour appliquer un fond et du padding.
    On suppose que processed_messages est une liste de dictionnaires avec les clés 'sender', 'content' et 'datetime'.
    """
    styles = getSampleStyleSheet()
    message_style = ParagraphStyle("messageStyle", parent=styles["BodyText"], fontSize=10, leading=12)
    widgets = []
    for msg in processed_messages:
        # Formatage du message – ajustez au besoin pour reproduire la logique originale
        content_text = f"<b>{msg.get('sender','')}</b>: {msg.get('content','')}  <font size='8' color='grey'>[{msg.get('datetime','')}]</font>"
        p = Paragraph(content_text, message_style)
        # Utilisation d'une Table pour simuler une bulle de message
        table = Table([[p]], colWidths=[400])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        widgets.append(table)
        widgets.append(Spacer(1, 6))
    return widgets

def generate_pdf(main_title, sub_title, cover_image_path, footer_image_path, output_directory, processed_messages):
    """
    Génère un PDF complet en ajoutant une page de couverture suivie des messages.
    Le PDF est créé avec des marges similaires à celles du code original et est sauvegardé dans le répertoire output_directory.
    """
    # Construction du chemin de sortie
    file_path = os.path.join(output_directory, f"{main_title}_{sub_title}.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=A4,
                            rightMargin=20, leftMargin=20, topMargin=40, bottomMargin=60)

    story = []
    # Construction de la page de couverture
    cover_page = build_cover_page(main_title, sub_title, cover_image_path, footer_image_path)
    story.extend(cover_page)

    # Construction des messages "widgets"
    message_widgets = build_message_widgets(processed_messages)
    story.extend(message_widgets)

    # Création du document final en un seul flux
    doc.build(story)
    print(f"PDF généré avec succès : {file_path}")
    return file_path