import cv2
from Computer_vision.core_classes.emotion_recognition_service.FER_image import FER_image
from Computer_vision.core_classes.face_detection_service.Face_detector import face_detector

FD = face_detector()


class VideoProcessor:

    @staticmethod
    def split_video_into_frames(video_path):
        video = cv2.VideoCapture(video_path)
        frame_list = []

        while True:
            success, frame = video.read()
            if not success:
                break
            frame_list.append(frame)

        video.release()
        return frame_list

    @staticmethod
    def process_video(video_path):
        frames = VideoProcessor.split_video_into_frames(video_path)

        emotion_count = {}

        for frame in frames:
            # Perform face detection on the frame
            # If a face is detected, perform emotion recognition
            face_detection = FD.detect_face(frame)
            if face_detection:

                # For simplicity, let's assume that the face detection is always successful
                emotion = FER_image(face_detection)

                # Increment the count for the detected emotion
                if emotion not in emotion_count:
                    emotion_count[emotion] = 0
                emotion_count[emotion] += 1

        # Find the emotion with the highest count
        most_common_emotion = max(emotion_count, key=emotion_count.get)

        return most_common_emotion


def process_video(video_path):
    frames = VideoProcessor.split_video_into_frames(video_path)

    emotion_count = {}

    for frame in frames:
        # Perform face detection on the frame
        # If a face is detected, perform emotion recognition
        # For simplicity, let's assume that the face detection is always successful
        emotion = FER_image(frame)

        # Increment the count for the detected emotion
        if emotion not in emotion_count:
            emotion_count[emotion] = 0
        emotion_count[emotion] += 1

    # Find the emotion with the highest count
    most_common_emotion = max(emotion_count, key=emotion_count.get)

    return most_common_emotion