from Computer_vision.core_classes.emotion_recognition_service.FER_image import FER_image
from Computer_vision.core_classes.face_detection_service.Face_detector import face_detector

if __name__ == '__main__':
    FD = face_detector()
    IMAGE_FILES = face_detector.read_images_from_directory()
    face_images,face_landmarks = FD.detect_face(IMAGE_FILES= IMAGE_FILES,return_face_landmarks=True)
    print("\n\n")
    for img_idx,image in enumerate(face_images):
        print(f"---- started processiong face image {img_idx+1} ----")
        FER_image(img=image, show_image=True)


