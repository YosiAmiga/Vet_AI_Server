import torch
import torchvision.transforms as transforms
from PIL import Image

# Load the pre-trained model
model = torch.hub.load('ishay2b/fer2013_resnet18', 'resnet18', pretrained=True)

# Set the model to evaluation mode
model.eval()

# Define the transformation to apply to the input image
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load and transform the input image
image = Image.open('example_image.jpg')
input_tensor = transform(image).unsqueeze(0)

# Make a prediction using the model
with torch.no_grad():
    output = model(input_tensor)

# Get the predicted emotion label
_, predicted = torch.max(output.data, 1)
emotion_label = predicted.item()

print('Predicted emotion label:', emotion_label)
