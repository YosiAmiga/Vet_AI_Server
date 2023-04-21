from Computer_vision.core_classes.emotion_recognition_service.FER_image import FER_image
from Computer_vision.core_classes.face_detection_service.Face_detector import face_detector

if __name__ == '__main__':
    FD = face_detector()
    IMAGE_FILES = face_detector.read_images_from_directory()
    face_images = FD.detect_face(IMAGE_FILES= IMAGE_FILES)

    for img_idx,image in enumerate(face_images):
        print(f"---- started processiong image {img_idx} ----")
        FER_image(img=image, show_image=True)


