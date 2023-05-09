import base64
import os
import glob
from flask import Blueprint, request, jsonify
from DB import database
from DB.SQL_scripts.db_scripts import *
from PIL import Image
from Computer_vision.core_classes.emotion_recognition_service.FER_image import FER_image
from Computer_vision.core_classes.face_detection_service.Face_detector import face_detector
from Computer_vision.Constants import emotions_constants
import cv2

FD = face_detector()
pet_bp = Blueprint('pet_bp', __name__)

UPLOAD_FOLDER = './src/uploaded_images'
USERS_PETS_FOLDER = './src/uploaded_images/users_pets'


@pet_bp.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']

        pet_id = 0
        if len(request.form) != 0:
            pet_id = request.form['pet_id']
            print('pet is',pet_id)
        if file:
            filename = file.filename
            user_mail_and_timestamp = filename.split('&')
            user_mail = user_mail_and_timestamp[0]
            file_timestamp = user_mail_and_timestamp[1]
            new_user_mail_directory = os.path.join(UPLOAD_FOLDER, user_mail)
            if not os.path.exists(new_user_mail_directory):
                os.makedirs(new_user_mail_directory)
            file.save(os.path.join(new_user_mail_directory, filename))
            ##TODO:
            ## 1. After saving the file,check if its a video or a picture
            ## 2. Picture: send to FER_image() function, and get the predection of emotion
            ## 3. Video: split into multiple pictures and send to FER_image() function to do the same
            ## 4. return the prediction of the uploaded file

            ## IMAGES - WORKING
            prediction = get_pet_emotion_prediction(new_user_mail_directory)
            print('Prediction is ', prediction)
            prediction_id = emotions_constants.get_emotion_id(prediction)
            database.insert_prediction(user_mail,pet_id,prediction_id)
            ## VIDEOS - TODO
            return 'Emotion is: ' + prediction, 200
        else:
            return 'No file found.', 400


@pet_bp.route('/get-pet-types', methods=['POST'])
def get_pet_types():
    conn = database.get_db()
    c = conn.cursor()
    c.execute(SELECT_ALL_PET_TYPES)
    types = c.fetchall()
    conn.close()

    return types


@pet_bp.route('/get-user-pets', methods=['POST'])
def get_user_pets():
    data = request.get_json()
    email = data.get('userEmail')

    conn = database.get_db()
    c = conn.cursor()
    c.execute(SELECT_PETS_BY_OWNER_EMAIL, (email,))
    pets = c.fetchall()
    conn.close()

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

    conn = database.get_db()
    c = conn.cursor()

    c.execute(INSERT_PET, (owner_email, pet_type, pet_name, pet_dob))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

def get_pet_emotion_prediction(new_user_mail_directory):
    IMAGE_FILES = face_detector.read_images_from_directory(new_user_mail_directory)
    face_images, face_landmarks = FD.detect_face(IMAGE_FILES=IMAGE_FILES, return_face_landmarks=True)
    latest_picture_uploaded = face_images[len(face_images)-1]
    cv2.imshow("the pic",latest_picture_uploaded)
    #cv2.waitKey(0)
    prediction = FER_image(latest_picture_uploaded)
    return prediction


@pet_bp.route('/get-pet-history', methods=['POST'])
def get_pet_history_predictions():
    data = request.get_json()
    pet_id = data.get('petId')
    predictions_history = database.get_pet_history_predictions(pet_id)
    print('predictions_history', predictions_history)
    return jsonify(predictions_history)

