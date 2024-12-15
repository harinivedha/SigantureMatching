from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from signature import match

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'error': 'No file part'})

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        return jsonify({'error': 'No selected file'})

    if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)

        file1.save(path1)
        file2.save(path2)

        similarity = match(path1, path2)

        if similarity > 90:
            confidence = "Likely a match"
        elif similarity > 70:
            confidence = "Possibly a match"
        else:
            confidence = "Unlikely a match"

        return jsonify({'similarity': similarity, 'confidence': confidence})

    return jsonify({'error': 'Invalid file type'})

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)
