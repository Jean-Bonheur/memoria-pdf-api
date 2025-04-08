from flask import Flask, request, send_file, jsonify
import os
import tempfile
import uuid
from pdf_generator import generate_pdf

app = Flask(__name__)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf_api():
    try:
        data = request.get_json()

        # Extraction des champs
        main_title = data.get('main_title', 'Toi & Moi')
        sub_title = data.get('sub_title', "Notre histoire d'amour")
        cover_image_path = data.get('cover_image_path')
        footer_image_path = data.get('footer_image_path')
        messages = data.get('messages', [])

        # Répertoire temporaire
        output_dir = os.path.join("static", "temp")
        os.makedirs(output_dir, exist_ok=True)

        # Nom de fichier unique
        filename = f"{uuid.uuid4()}.pdf"
        file_path = os.path.join(output_dir, filename)

        # Génération du PDF (le script doit retourner file_path)
        generate_pdf(main_title, sub_title, cover_image_path, footer_image_path, output_dir, messages)

        # Envoi du fichier en réponse
        return send_file(file_path, as_attachment=True, download_name=f"{main_title}_${sub_title}.pdf", mimetype='application/pdf')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
