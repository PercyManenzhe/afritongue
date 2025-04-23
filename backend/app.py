from flask import Flask, request, jsonify
import os
# at top
import sqlite3

# Initialize the Flask application
app = Flask(__name__)

DB = 'translators.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS translators
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT, email TEXT, languages TEXT)""")
init_db()

@app.route('/apply', methods=['POST'])
def apply_translator():
    data = request.get_json()
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO translators(name,email,languages) VALUES (?,?,?)",
                     (data['name'], data['email'], data['languages']))
    return jsonify({'message': 'Application stored'}), 201

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Welcome to the AfriTongue API! Use the /upload endpoint to upload files."

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    Endpoint to handle file uploads.
    """
    if request.method == 'GET':
        # Display an HTML form for file upload
        return '''
        <h1>Upload a File</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="document">
            <input type="submit" value="Upload">
        </form>
        '''
    elif request.method == 'POST':
        # Handle file upload
        if 'document' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['document']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        return jsonify({'message': 'File uploaded', 'filename': file.filename}), 200

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, port=8080)