from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from DB import database
from DB.SQL_scripts.db_scripts import *
from src.routes.auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
CORS(app)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
