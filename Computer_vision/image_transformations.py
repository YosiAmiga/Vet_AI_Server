import cv2
import numpy as np



class image_transformations:

    def __init__(self):
        self.types_of_transformations = ['resize']


    def get_transformations(self,printer = True):
        if printer:
            print(self.types_of_transformations)
        return self.types_of_transformations

    @staticmethod
    def resize_image(image ,desired_size = (640, 480)):
        desired_size = (640, 480)
        resized_img = cv2.resize(image, desired_size)
        return resized_img
