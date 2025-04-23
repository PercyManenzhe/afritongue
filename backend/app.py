from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import werkzeug

app = Flask(__name__)
CORS(app)

# Config
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'mp4'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return "AfriTongue Backend is Running"

# === WHISPER INTEGRATION ===
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = werkzeug.utils.secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Placeholder: Whisper API transcription
        transcription = "Transcription will be generated here by Whisper."

        return jsonify({
            'message': f'File {filename} uploaded successfully',
            'transcription': transcription
        })

    return jsonify({'error': 'File type not allowed'}), 400

# === TRANSLATOR DB ===
@app.route('/apply', methods=['POST'])
def apply_translator():
    data = request.get_json()
    print("Translator Application Received:", data)
    return jsonify({'message': 'Application received successfully'})

# === PAYSTACK ===
@app.route('/pay', methods=['POST'])
def pay():
    data = request.get_json()
    print("Initiate Payment:", data)
    return jsonify({'message': 'Payment initiated (mock)'})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
