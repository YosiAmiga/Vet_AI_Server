from flask import Blueprint, request, jsonify
from DB import database
from DB.SQL_scripts.db_scripts import *

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = database.get_login(email)

    if user:
        if user[1] == password:
            return jsonify({'success': True, 'user_type': user[2]})
        else:
            return jsonify({'success': False, 'message': 'Incorrect password.'})
    else:
        return jsonify({'success': False, 'message': 'User not found.'})


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = database.get_user(email)

    if user:
        return jsonify({'success': False, 'message': 'User already exists.'})
    else:
        result = database.insert_user(email, password)

        return jsonify({'success': True})