from flask import Blueprint, request, jsonify
from DB import database
from DB.SQL_scripts.db_scripts import *

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/login', methods=['POST'])
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


@user_bp.route('/register', methods=['POST'])
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