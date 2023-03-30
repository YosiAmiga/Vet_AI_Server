import cv2
import mediapipe as mp
import os

from mediapipe.python.solutions.drawing_utils import DrawingSpec

from Computer_vision.image_transformations import image_transformations



class face_detector:
    def __init__(self):
        self.detector_api = 'mediaPipe'
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.normtlized_function = mp.solutions.drawing_utils._normalized_to_pixel_coordinates


    @staticmethod
    def read_images_from_directory(directory_path = r"C:\Users\97252\Desktop\Vet.ai\Vet_AI_Server\uploaded_images"):
        IMAGE_FILES = []
        for filename in os.listdir(directory_path):
            # Check if the file is an image file
            if filename.endswith('.jpg') or filename.endswith('.png'):
                # Read the image file
                image = cv2.imread(os.path.join(directory_path, filename))
                resized_img = image_transformations.resize_image(image)
                IMAGE_FILES.append(resized_img)
        return IMAGE_FILES



# for image in IMAGE_FILES:
#     cv2.imshow('Resized Image', image)
#     cv2.waitKey(0)


    def detect_face(self,IMAGE_FILES,bbox_drawing_spec: DrawingSpec = DrawingSpec()):
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
              print('Nose tip:')
              print(self.mp_face_detection.get_key_point(
                  detection, self.mp_face_detection.FaceKeyPoint.NOSE_TIP))
              self.mp_drawing.draw_detection(annotated_image, detection)

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
                cv2.imshow("cropped", crop_img)
                # cv2.imwrite("ROI",crop_img)
                cv2.waitKey(0)

            cv2.imshow('face_detection',annotated_image)
            cv2.waitKey(0)

            # cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)


if __name__ == '__main__':
    FD = face_detector()
    IMAGE_FILES = face_detector.read_images_from_directory()
    FD.detect_face(IMAGE_FILES= IMAGE_FILES)
