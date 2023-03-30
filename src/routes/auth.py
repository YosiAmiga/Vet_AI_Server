from flask import Blueprint, request, jsonify
from DB import database
import os
from DB.SQL_scripts.db_scripts import SELECT_USER_BY_EMAIL, INSERT_USER

auth_bp = Blueprint('auth_bp', __name__)

UPLOAD_FOLDER = './src/uploaded_images'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@auth_bp.route('/login', methods=['POST'])
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

@auth_bp.route('/register', methods=['POST'])
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


@auth_bp.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return 'File uploaded and saved.', 200
        else:
            return 'No file found.', 400