import cv2
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

from Computer_vision.Constants.path_constants import path_to_model, path_to_face_image
from Computer_vision.core_classes.emotion_recognition_service.model import *


class EmotionDetector:
    def __init__(self, model_path = path_to_model):
        self.model_path = model_path
        self.model = self.load_trained_model()
        self.emotion_dict = {0: 'neutral', 1: 'happiness', 2: 'surprise', 3: 'sadness',
                             4: 'anger', 5: 'disgust', 6: 'fear'}
        self.val_transform = transforms.Compose([
            transforms.ToTensor()])

    def load_trained_model(self):
        model = Face_Emotion_CNN()
        model.load_state_dict(torch.load(self.model_path, map_location=lambda storage, loc: storage), strict=False)
        return model

    def FER_image(self, img, show_image=False):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        resize_frame = cv2.resize(gray, (48, 48))
        X = resize_frame/256
        X = Image.fromarray((resize_frame))
        X = self.val_transform(X).unsqueeze(0)
        with torch.no_grad():
            self.model.eval()
            log_ps = self.model.cpu()(X)
            ps = torch.exp(log_ps)
            top_p, top_class = ps.topk(1, dim=1)
            pred = self.emotion_dict[int(top_class.numpy())]
            print(f"\t*prediction: {pred}")
            if show_image:
                plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                plt.grid(False)
                plt.axis('off')
                plt.show()
            return pred


if __name__ == "__main__":
    detector = EmotionDetector()
    img = cv2.imread(r"C:\Users\user\PycharmProjects\Pet_AI_Server\src\uploaded_images\y_171095@walla.co.il\y_171095@walla.co.il&5-9-2023- 11-33-00 AM.jpeg")
    detector.FER_image(img=img, show_image=False)
