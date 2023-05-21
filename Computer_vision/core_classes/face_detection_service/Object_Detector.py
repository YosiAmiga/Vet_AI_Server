import os
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
from PIL import Image
import matplotlib.pyplot as plt


class ObjectDetector:
    PATH_TO_LABELS = 'Computer_vision/core_classes/face_detection_service/data/mscoco_label_map.pbtxt'
    # PATH_TO_LABELS = 'Computer_vision/core_classes/ace_detection_service/data/mscoco_label_map.pbtxt'

    def __init__(self):
        self.label_map = self.load_label_map(self.PATH_TO_LABELS)
        self.model = self.load_model()


    def load_label_map(self, label_map_path):
        label_map_dict = {}
        with open(label_map_path, 'r') as f:
            lines = f.readlines()
            for i in range(0, len(lines), 5):  # step of 5 because each item spans 5 lines
                class_id = int(lines[i+2].split(': ')[1])  # extract id
                class_name = lines[i+3].split(': ')[1].strip().strip('\"')  # extract class name
                label_map_dict[class_id] = class_name
        return label_map_dict


    def load_model(self):
        detector_model = fasterrcnn_resnet50_fpn(pretrained=True)
        detector_model.eval()
        return detector_model


    def object_detection_from_folder(self, directory ='src/uploaded_images/Vet_Tagging/Pain'):
        # directory = './src/uploaded_images/Vet_Tagging/Pain/'
        image_files = os.listdir(directory)
        images_location = [os.path.join(directory, img) for img in image_files]

        for image_file in images_location:
            image = Image.open(image_file).convert("RGB")
            image_tensor = F.to_tensor(image)
            output_dict = self.model([image_tensor])

            for i in range(len(output_dict[0]['labels'])):
                if output_dict[0]['scores'][i] > 0.5:
                    class_id = output_dict[0]['labels'][i].item()
                    class_name = self.label_map[class_id]
                    print(f'Image {image_file} Detected as: {class_name} with confidence {output_dict[0]["scores"][i]}')

            #plt.imshow(image_tensor.permute(1, 2, 0))
            #plt.show()

    def object_detection_by_image_file(self, img):
        # Convert the image to PIL format
        pil_image = Image.open(img).convert("RGB")
        image_tensor = F.to_tensor(pil_image)

        # Run the model
        output_dict = self.model([image_tensor])
        max_confidence = 0
        max_class = None

        # Get the highest confidence value class
        for i in range(len(output_dict[0]['labels'])):
            if output_dict[0]['scores'][i] > max_confidence:
                max_confidence = output_dict[0]['scores'][i]
                class_id = output_dict[0]['labels'][i].item()
                max_class = self.label_map[class_id]

        print(f'Image Detected as: {max_class} with highest confidence {max_confidence}')

        # To see all detections in pictures
        # for i in range(len(output_dict[0]['labels'])):
        #     if output_dict[0]['scores'][i] > 0.5:
        #         class_id = output_dict[0]['labels'][i].item()
        #         class_name = self.label_map[class_id]
        #         print(f'Image Detected as: {class_name} with confidence {output_dict[0]["scores"][i]}')

        # Display the image
        #plt.imshow(image_tensor.permute(1, 2, 0))
        #plt.show()
        return max_class
    def object_detection_by_image(self, img):
        # Convert the image to PIL format
        pil_image = Image.fromarray(img).convert("RGB")
        image_tensor = F.to_tensor(pil_image)

        # Run the model
        output_dict = self.model([image_tensor])
        max_confidence = 0
        max_class = None

        # Get the highest confidence value class
        for i in range(len(output_dict[0]['labels'])):
            if output_dict[0]['scores'][i] > max_confidence:
                max_confidence = output_dict[0]['scores'][i]
                class_id = output_dict[0]['labels'][i].item()
                max_class = self.label_map[class_id]

        print(f'Image Detected as: {max_class} with highest confidence {max_confidence}')

        # To see all detections in pictures
        # for i in range(len(output_dict[0]['labels'])):
        #     if output_dict[0]['scores'][i] > 0.5:
        #         class_id = output_dict[0]['labels'][i].item()
        #         class_name = self.label_map[class_id]
        #         print(f'Image Detected as: {class_name} with confidence {output_dict[0]["scores"][i]}')

        # Display the image
        #plt.imshow(image_tensor.permute(1, 2, 0))
        #plt.show()
        return max_class

if __name__ == '__main__':
    detector = ObjectDetector()
    detector.object_detection_from_folder()
