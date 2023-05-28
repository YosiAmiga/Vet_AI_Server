from flask import Blueprint, request, jsonify
from Analytics.admin_analytics import admin_analytics
from src.services.prediction_service import *

object_detector = ObjectDetector()
FD = face_detector()
admin_bp = Blueprint('admin_bp', __name__)

UPLOAD_FOLDER = './src/uploaded_images'
USERS_PETS_FOLDER = './src/uploaded_images/users_pets'
UPLOAD_FOLDER_VIDEOS = './src/uploaded_videos/'


@admin_bp.route('/get-admin-analytics', methods=['POST'])
def get_admin_analytics():
    predictions_by_users = database.get_predictions_by_users()
    pet_prediction_types = database.get_pet_prediction_types()
    user_pet_count = database.get_user_pet_count()
    pet_types_count = database.get_pet_types_count()
    data = {
        'predictions_by_users': predictions_by_users,
        'pet_prediction_types': pet_prediction_types,
        'user_pet_count': user_pet_count,
        'pet_types_count': pet_types_count
    }
    return jsonify(data)


@admin_bp.route('/get-all-pets', methods=['POST'])
def get_all_pets():
    all_pets = database.get_all_pets()
    return jsonify(all_pets)


@admin_bp.route('/get-all-predictions', methods=['POST'])
def get_all_predictions():
    all_predictions = database.get_all_predictions()
    return jsonify(all_predictions)
