import base64
import os
import glob
from flask import Blueprint, request, jsonify
from DB import database
from DB.SQL_scripts.db_scripts import *
from PIL import Image

vet_bp = Blueprint('vet_bp', __name__)
UPLOAD_FOLDER = './src/uploaded_images'


@vet_bp.route('/vet-upload', methods=['POST'])
def vet_upload():
    image = request.files['image']
    filename = image.filename
    tag = request.form['tag']

    base_path = UPLOAD_FOLDER+'/Vet_Tagging'
    pain_path = os.path.join(base_path, 'Pain')
    no_pain_path = os.path.join(base_path, 'No_Pain')

    # Create the necessary directories if they do not exist
    os.makedirs(pain_path, exist_ok=True)
    os.makedirs(no_pain_path, exist_ok=True)
    # Save the image in the appropriate
    if tag == 'Pain':
        image.save(os.path.join(pain_path, filename))
        return jsonify({'success': True})
    if tag == 'No Pain':
        image.save(os.path.join(no_pain_path, filename))
        return jsonify({'success': True})
    else:
        return jsonify({'fail': False})
