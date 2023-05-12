import cv2
# import torchvision.transforms as transforms
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

from Computer_vision.Constants.path_constants import path_to_model, path_to_face_image
from Computer_vision.core_classes.emotion_recognition_service.model import *


def load_trained_model(model_path):
    model = Face_Emotion_CNN()
    model.load_state_dict(torch.load(model_path, map_location=lambda storage, loc: storage), strict=False)
    return model

def FER_image(img,show_image=False):

    model = load_trained_model(path_to_model)
    
    emotion_dict = {0: 'neutral', 1: 'happiness', 2: 'surprise', 3: 'sadness',
                    4: 'anger', 5: 'disguest', 6: 'fear'}

    val_transform = transforms.Compose([
        transforms.ToTensor()])

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    resize_frame = cv2.resize(gray, (48, 48))
    X = resize_frame/256
    X = Image.fromarray((resize_frame))
    X = val_transform(X).unsqueeze(0)
    with torch.no_grad():
        model.eval()
        log_ps = model.cpu()(X)
        ps = torch.exp(log_ps)
        top_p, top_class = ps.topk(1, dim=1)
        pred = emotion_dict[int(top_class.numpy())]
        # cv2.putText(img, pred, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1)
        print(f"\t*prediction: {pred}")
        if show_image:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.grid(False)
            plt.axis('off')
            plt.show()
        return pred




if __name__ == "__main__":
    img = cv2.imread(path_to_face_image)
    FER_image(img=img,show_image = False)

