from Computer_vision.core_classes.face_detection_service.Face_detector import face_detector


class image_filtering:
    def __init__(self, object_for_lookup='human', filtering_type='object'):
        """
        Constructor for image filtering service:

        :param filtering_type: filtering criteria on a set of images
        :param object_for_lookup: if filtering images by object then we need to define object to filter by it's detection in the image

        """
        self.filtering_type = filtering_type

        if self.filtering_type == 'object':  # currently default --> can be later changed as a new feature
            self.filter_by_object = object_for_lookup

    def filter_images(self):
        FD = face_detector()
        IMAGE_FILES = face_detector.read_images_from_directory()
        face_images, face_landmarks = FD.detect_face(IMAGE_FILES=IMAGE_FILES, return_face_landmarks=True)



