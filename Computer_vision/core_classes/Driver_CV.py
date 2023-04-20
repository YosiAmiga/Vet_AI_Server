from Computer_vision.core_classes.face_detection_service.Face_detector import face_detector

if __name__ == '__main__':
    FD = face_detector()
    IMAGE_FILES = face_detector.read_images_from_directory()
    FD.detect_face(IMAGE_FILES= IMAGE_FILES)
