from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = 'app_data.db'
UPLOAD_FOLDER = 'uploaded_images'

UPLOAD_FOLDER = 'uploaded_images'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
################################
# Initialize the database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()

    if user:
        if user[1] == password:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Incorrect password.'})
    else:
        return jsonify({'success': False, 'message': 'User not found.'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()

    if user:
        conn.close()
        return jsonify({'success': False, 'message': 'User already exists.'})
    else:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()
        return jsonify({'success': True})@app.route('/register', methods=['POST'])


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return 'File uploaded and saved.', 200
        else:
            return 'No file found.', 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
