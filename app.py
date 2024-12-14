from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os
from flask_cors import CORS  # Import and enable CORS

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/api/image-to-text', methods=['POST'])
def image_to_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    file_path = os.path.join('temp', file.filename)
    os.makedirs('temp', exist_ok=True)
    file.save(file_path)

    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        os.remove(file_path)
        return jsonify({'text': text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
