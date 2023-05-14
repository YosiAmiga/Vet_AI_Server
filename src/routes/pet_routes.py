import base64
import glob
from flask import Blueprint, request, jsonify
from DB import database
from PIL import Image
from Computer_vision.core_classes.emotion_recognition_service.FER_image import FER_image
from Computer_vision.core_classes.face_detection_service.Face_detector import face_detector
from Computer_vision.Constants import emotions_constants
from Computer_vision.core_classes.video_filtering_service import VideoProcessor
import cv2
import os
from src.services.uploading_file_service import *
from src.services.prediction_service import *


FD = face_detector()
pet_bp = Blueprint('pet_bp', __name__)

UPLOAD_FOLDER = './src/uploaded_images'
USERS_PETS_FOLDER = './src/uploaded_images/users_pets'
UPLOAD_FOLDER_VIDEOS = './src/uploaded_videos/'


# def get_latest_file_in_directory(directory_path):
#     files = os.listdir(directory_path)
#     files.sort(key=lambda x: os.path.getmtime(os.path.join(directory_path, x)))
#     latest_file = files[-1]
#     return os.path.join(directory_path, latest_file)
#
#
# def predict_video(file,pet_id):
#     save_file_in_directory(file, UPLOAD_FOLDER_VIDEOS)
#     filename = file.filename
#     user_mail_and_timestamp = filename.split('&')
#     user_mail = user_mail_and_timestamp[0]
#     # file_timestamp = user_mail_and_timestamp[1]
#     new_user_mail_directory = os.path.join(UPLOAD_FOLDER_VIDEOS, user_mail)
#     latest_video_path = get_latest_file_in_directory(new_user_mail_directory)
#     prediction = VideoProcessor.process_video(latest_video_path)
#     prediction_id = emotions_constants.get_emotion_id(prediction)
#     prediction_inserted_good = database.insert_prediction(user_mail, pet_id, prediction_id)
#
#     return prediction
#
#
# def predict_image(file,pet_id):
#     save_file_in_directory(file, UPLOAD_FOLDER)
#     filename = file.filename
#     user_mail_and_timestamp = filename.split('&')
#     user_mail = user_mail_and_timestamp[0]
#     # file_timestamp = user_mail_and_timestamp[1]
#     new_user_mail_directory = os.path.join(UPLOAD_FOLDER, user_mail)
#     prediction = get_pet_emotion_prediction(new_user_mail_directory)
#     prediction_id = emotions_constants.get_emotion_id(prediction)
#     prediction_inserted_good = database.insert_prediction(user_mail, pet_id, prediction_id)
#     return prediction
#
#
# def save_file_in_directory(file, directory):
#     filename = file.filename
#     user_mail_and_timestamp = filename.split('&')
#     user_mail = user_mail_and_timestamp[0]
#     # file_timestamp = user_mail_and_timestamp[1]
#     new_user_mail_directory = os.path.join(directory, user_mail)
#     if not os.path.exists(new_user_mail_directory):
#         os.makedirs(new_user_mail_directory)
#     file.save(os.path.join(new_user_mail_directory, filename))


@pet_bp.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        pet_id = 0
        if len(request.form) != 0:
            pet_id = request.form['pet_id']
            print('pet is',pet_id)

        # VIDEOS
        if file.mimetype == 'video/webm':
            prediction = predict_video(file, pet_id)
            return 'Emotion is: ' + prediction, 200

        # IMAGES
        if file.mimetype == 'image/jpeg':
            prediction = predict_image(file, pet_id)
            return 'Emotion is: ' + prediction, 200

        return 'Error in file uploading process.', 400


@pet_bp.route('/get-pet-types', methods=['POST'])
def get_pet_types():
    types = database.get_pet_types()
    return types


@pet_bp.route('/get-user-pets', methods=['POST'])
def get_user_pets():
    data = request.get_json()
    email = data.get('userEmail')
    pets = database.get_user_pets(email)

    pet_list = []
    for pet in pets:
        pet_id, owner_email, pet_type, pet_name, pet_dob = pet
        user_folder = os.path.join(USERS_PETS_FOLDER, owner_email)
        pet_photo_path = os.path.join(user_folder, f"{pet_name}.*")
        image_list = glob.glob(pet_photo_path)
        if image_list:
            with open(image_list[0], "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            image_url = f"data:image/png;base64,{encoded_image}"
        else:
            image_url = 'https://via.placeholder.com/150'

        pet_list.append({
            'pet_id': pet_id,
            'ownerEmail': owner_email,
            'type': pet_type,
            'name': pet_name,
            'dob': pet_dob,
            'image': image_url
        })

    return jsonify(pet_list)


@pet_bp.route('/add-new-pet', methods=['POST'])
def add_new_pet():
    data = request.form
    owner_email = data.get('owner_email')
    pet_type = data.get('pet_type')
    pet_name = data.get('pet_name')
    pet_dob = data.get('pet_dob')
    pet_photo = request.files['pet_photo']

    # Create user's folder if it doesn't exist
    user_folder = os.path.join(USERS_PETS_FOLDER, owner_email)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # Resize the image to 150x150 pixels
    image = Image.open(pet_photo.stream)
    image = image.resize((150, 150), Image.ANTIALIAS)

    # Save the resized photo in the designated folder
    pet_photo_filename = f"{pet_name}{os.path.splitext(pet_photo.filename)[1]}"
    image_path = os.path.join(user_folder, pet_photo_filename)
    image.save(image_path)
    result = database.insert_pet(owner_email, pet_type, pet_name, pet_dob)

    return jsonify({'success': True})


@pet_bp.route('/get-pet-history', methods=['POST'])
def get_pet_history_predictions():
    data = request.get_json()
    pet_id = data.get('petId')
    predictions_history = database.get_pet_history_predictions(pet_id)
    print('predictions_history', predictions_history)
    return jsonify(predictions_history)


@pet_bp.route('/get-prediction-distribution', methods=['POST'])
def get_prediction_distribution():
    data = request.get_json()
    pet_id = data.get('petId')
    prediction_distribution = database.get_prediction_distribution(pet_id)
    print('prediction_distribution', prediction_distribution)
    return jsonify(prediction_distribution)


# def get_pet_emotion_prediction(new_user_mail_directory):
#     IMAGE_FILES = face_detector.read_images_from_directory(new_user_mail_directory)
#     face_images, face_landmarks = FD.detect_face(IMAGE_FILES=IMAGE_FILES, return_face_landmarks=True)
#     latest_picture_uploaded = face_images[len(face_images)-1]
#     # cv2.imshow("the pic",latest_picture_uploaded)
#     # cv2.waitKey(0)
#     prediction = FER_image(latest_picture_uploaded)
#     return prediction

