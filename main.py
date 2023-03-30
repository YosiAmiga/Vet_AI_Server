from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from DB import database
from DB.SQL_scripts.db_scripts import *

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploaded_images'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = database.get_db()
    c = conn.cursor()
    c.execute(SELECT_USER_BY_EMAIL, (email,))
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

    conn = database.get_db()
    c = conn.cursor()
    c.execute(SELECT_USER_BY_EMAIL, (email,))
    user = c.fetchone()

    if user:
        conn.close()
        return jsonify({'success': False, 'message': 'User already exists.'})
    else:
        c.execute(INSERT_USER, (email, password))
        conn.commit()
        conn.close()
        return jsonify({'success': True})


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
