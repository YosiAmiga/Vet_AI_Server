import cv2
import mediapipe as mp
import os
from mediapipe.python.solutions.drawing_utils import DrawingSpec
from Computer_vision.Constants.path_constants import *
from Computer_vision.core_classes.helpers.image_transformations import image_transformations


class face_detector:
    def __init__(self):
        self.is_local_save = True
        self.detector_api = 'mediaPipe'
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.normtlized_function = mp.solutions.drawing_utils._normalized_to_pixel_coordinates

    @staticmethod
    def read_images_from_directory(directory_path=path_to_images):
        print(f"--- started reading images from the users directory ----")
        IMAGE_FILES = []
        for img_idx,filename in enumerate(os.listdir(directory_path)):
            # Check if the file is an image file
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
                # Read the image file
                image = cv2.imread(os.path.join(directory_path, filename))
                resized_img = image_transformations.resize_image(image)
                IMAGE_FILES.append(resized_img)
                print(f"\t*read image number: {img_idx+1}")
        return IMAGE_FILES

    def save_image(self, image: cv2.imread, user_name: str = "detected_face",
                   filename=path_to_face_images_folder) -> None:
        if self.is_local_save:
            cv2.imwrite(filename + fr"/{user_name}.png", image)
            print("\n\n---- face image saved to " + filename + " ----")
        return None

    def detect_face(self, IMAGE_FILES, bbox_drawing_spec: DrawingSpec = DrawingSpec(), return_face_landmarks=False):
        face_images = []
        face_landmarks = []
        with self.mp_face_detection.FaceDetection(
                model_selection=1, min_detection_confidence=0.5) as face_detection:
            for idx, file in enumerate(IMAGE_FILES):
                image = file
                # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
                results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

                # Draw face detections of each face.
                if not results.detections:
                    continue
                annotated_image = image.copy()
                for detection in results.detections:
                    if return_face_landmarks:
                        face_landmarks.append(detection)
                    # print('Nose tip:')
                    # print(self.mp_face_detection.get_key_point(
                    #     detection, self.mp_face_detection.FaceKeyPoint.NOSE_TIP))
                    # self.mp_drawing.draw_detection(annotated_image, detection)

                location = detection.location_data
                for keypoint in range(1):
                    relative_bounding_box = location.relative_bounding_box
                    image_rows, image_cols, _ = image.shape
                    rect_start_point = self.normtlized_function(
                        relative_bounding_box.xmin, relative_bounding_box.ymin, image_cols,
                        image_rows)
                    rect_end_point = self.normtlized_function(
                        relative_bounding_box.xmin + relative_bounding_box.width,
                        relative_bounding_box.ymin + relative_bounding_box.height, image_cols,
                        image_rows)

                    ROI = cv2.rectangle(image, rect_start_point, rect_end_point,
                                        bbox_drawing_spec.color, bbox_drawing_spec.thickness)

                    crop_img = image[rect_start_point[1]:rect_end_point[1], rect_start_point[0]:rect_end_point[0]]
                    # cv2.imshow("cropped", crop_img)
                    face_images.append(crop_img)

                    # cv2.imwrite("ROI",crop_img)
                    self.save_image(image=crop_img)
                    # cv2.waitKey(0)

            # cv2.imshow('face_detection',annotated_image)
            if return_face_landmarks:
                return face_images, face_landmarks
            else:
                return face_images

                # cv2.waitKey(0)

                # cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
