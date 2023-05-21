from Computer_vision.Constants import emotions_constants
from Computer_vision.core_classes.emotion_recognition_service.FER_image import EmotionDetector
from Computer_vision.core_classes.face_detection_service.Face_detector import face_detector
from Computer_vision.core_classes.face_detection_service.Object_Detector import ObjectDetector
from Computer_vision.core_classes.video_filtering_service import VideoProcessor
from DB import database
from src.services.uploading_file_service import *
FD = face_detector()
object_detector = ObjectDetector()


def make_prediction(file_type,file, pet_id, directory, prediction_function):
    save_file_in_directory(file, directory)
    user_mail = get_user_mail(file)
    new_user_mail_directory = os.path.join(directory, user_mail)
    latest_file_path = get_latest_file_in_directory(new_user_mail_directory)
    if file_type == "video":
        prediction = prediction_function(latest_file_path)
    if file_type == "image":
        prediction = prediction_function(new_user_mail_directory)
    prediction_id = emotions_constants.get_emotion_id(prediction)
    prediction_inserted_good = database.insert_prediction(user_mail, pet_id, prediction_id)
    return prediction


def predict_video(file, pet_id):
    return make_prediction("video",file, pet_id, UPLOAD_FOLDER_VIDEOS, VideoProcessor.process_video)


def predict_image(file, pet_id):
    return make_prediction("image",file, pet_id, UPLOAD_FOLDER, get_pet_emotion_prediction)


def get_pet_emotion_prediction(new_user_mail_directory):
    detector = EmotionDetector()
    IMAGE_FILES = face_detector.read_images_from_directory(new_user_mail_directory)
    face_images, face_landmarks = FD.detect_face(IMAGE_FILES=IMAGE_FILES, return_face_landmarks=True)
    latest_picture_uploaded = face_images[len(face_images)-1]
    # cv2.imshow("the pic",latest_picture_uploaded)
    # cv2.waitKey(0)
    class_name = object_detector.object_detection_by_image(latest_picture_uploaded)
    prediction = 'no prediction'
    if class_name == 'person':
        prediction = detector.FER_image(latest_picture_uploaded)
    # prediction = FER_image(latest_picture_uploaded)
    return prediction