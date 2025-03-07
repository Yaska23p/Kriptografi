from flask import Flask, render_template, request, send_file
import os
from encryption import encrypt_text, decrypt_text, encrypt_file, decrypt_file
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_type = request.form['input_type']
    operation = request.form['operation']
    algorithm = request.form['algorithm']
    key = request.form['key'].encode()
    
    if input_type == 'text':
        text = request.form['text_input']
        if operation == 'encrypt':
            cipher_text = encrypt_text(text.encode(), key, algorithm)
            cipher_base64 = base64.b64encode(cipher_text).decode('utf-8')  # base64 encoding
            return render_template('index.html', cipher_text=cipher_base64)
        elif operation == 'decrypt':
            decrypted_text = decrypt_text(base64.b64decode(text), key, algorithm)
            return render_template('index.html', cipher_text=decrypted_text.decode('utf-8'))

    elif input_type == 'file':
        if 'file' not in request.files:
            return "No file uploaded", 400

        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        if operation == 'encrypt':
            processed_path = encrypt_file(filepath, key, algorithm)
        elif operation == 'decrypt':
            processed_path = decrypt_file(filepath, key, algorithm)
        
        return send_file(processed_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
