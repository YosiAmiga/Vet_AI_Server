import io

import cv2
import numpy as np
from Computer_vision.Constants.path_constants import path_to_video_blob


class blob_to_images_service:
    def __init__(self, video_blob_path):
        self.video_blob_path = video_blob_path
        self.video_converted = None
        self.video_frames = []

    def convert_blob_to_video(self) -> None:
        # convert the video blob to a numpy array
        video_np = np.frombuffer(self.video_blob_path, np.uint8)
        # decode the numpy array into a video using OpenCV
        self.video_converted = cv2.imdecode(video_np, cv2.IMREAD_UNCHANGED)
        print(f"Converted video is:\n\n {self.video_converted}")

    def split_video_to_frames(self) -> None:
        # extract each frame from the video and save it as an image
        for i in range(self.video_converted.shape[0]):
            frame = self.video_converted[i]
            self.video_frames.append(frame)
            print(f"Read a new frame from the blob:\n{frame}")
            # cv2.imwrite(f"frame_{i}.jpg", frame)

    def activate_service(self) -> None:
        self.convert_blob_to_video()
        self.split_video_to_frames()




if __name__ == '__main__':    # test the splitter pipeline
    with open(path_to_video_blob, "rb") as f:
        blob_content = f.read()

    # BTIS = blob_to_images_service(video_blob_path= blob_content) # create instance of the service
    # BTIS.activate_service()  # activate the service

    # decoded_data = base64.b64decode(blob_content)

    # np_data = np.frombuffer(blob_content, np.uint8)

    # Convert bytes object to NumPy array
    # nparr = np.frombuffer(blob_content, np.uint8)


