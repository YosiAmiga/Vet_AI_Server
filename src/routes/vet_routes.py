# import os
# from Computer_vision.core_classes.face_detection_service.Object_Detector import ObjectDetector
# from flask import Blueprint, request, jsonify
#
#
# vet_bp = Blueprint('vet_bp', __name__)
# UPLOAD_FOLDER = './src/uploaded_images'
# object_detector = ObjectDetector()
#
# @vet_bp.route('/vet-upload', methods=['POST'])
# def vet_upload():
#     image = request.files['image']
#     filename = image.filename
#     tag = request.form['tag']
#
#     base_path = UPLOAD_FOLDER+'/Vet_Tagging'
#     pain_path = os.path.join(base_path, 'Pain')
#     no_pain_path = os.path.join(base_path, 'No_Pain')
#
#     # Create the necessary directories if they do not exist
#     os.makedirs(pain_path, exist_ok=True)
#     os.makedirs(no_pain_path, exist_ok=True)
#     # Save the image in the appropriate
#     if tag == 'Pain':
#         image.save(os.path.join(pain_path, filename))
#         return jsonify({'success': True})
#     if tag == 'No Pain':
#         image.save(os.path.join(no_pain_path, filename))
#         return jsonify({'success': True})
#     else:
#         return jsonify({'fail': False})


import os
from flask import Blueprint, request, jsonify
from src.services.uploading_file_service import *

from Computer_vision.core_classes.face_detection_service.Object_Detector import ObjectDetector

vet_bp = Blueprint('vet_bp', __name__)
UPLOAD_FOLDER = './src/uploaded_images'
object_detector = ObjectDetector()


@vet_bp.route('/vet-upload', methods=['POST'])
def vet_upload():
    image = request.files['image']
    filename = image.filename
    tag = request.form['tag']
    type = request.form['type']
    prediction = request.form['prediction']

    class_name = object_detector.object_detection_by_image_file(image)
    class_name_lower = class_name.lower()
    type_lower = type.lower()
    if class_name_lower == type_lower:
        base_path = UPLOAD_FOLDER+'/Vet_Tagging'
        class_type = os.path.join(base_path, class_name)
        image.seek(0) # Reset the file pointer to the start

        prediction_path = os.path.join(class_type, prediction)
        # pain_path = os.path.join(class_type, 'Pain')
        # no_pain_path = os.path.join(class_type, 'No_Pain')

        # Create the necessary directories if they do not exist
        os.makedirs(prediction_path, exist_ok=True)
        image.save(os.path.join(prediction_path, filename))
        return jsonify({'success': True})
        # os.makedirs(pain_path, exist_ok=True)
        # os.makedirs(no_pain_path, exist_ok=True)
        # Save the image in the appropriate
        # if tag == 'Pain':
        #     image.save(os.path.join(pain_path, filename))
        #     return jsonify({'success': True})
        # if tag == 'No Pain':
        #     image.save(os.path.join(no_pain_path, filename))
        #     return jsonify({'success': True})
        # else:
        #     return jsonify({'fail': False})
    else:
        return jsonify({'Image Class selected do not match detection': False})
