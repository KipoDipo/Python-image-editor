import io
from PIL import Image
import numpy as np
import ImageProcessor as ip
import PySimpleGUI as sg

class ImageEditor:

    def __init__(self, image_path : str = None, image_editor_copy : 'ImageEditor' = None):
        
        if image_path is not None:
            image = Image.open(image_path)
            pixels = np.array(image)

            self.__original_pixels = pixels.copy()
            self.__current_pixels = pixels.copy()
            self.__history = [pixels.copy()]

        elif image_editor_copy is not None:
            pixels = image_editor_copy.__current_pixels
            self.__original_pixels = pixels.copy()
            self.__current_pixels = pixels.copy()
            self.__history = [pixels.copy()]

    def size(self) -> tuple:
        return (self.__current_pixels.shape[0], self.__current_pixels.shape[1])

    def edit(self, filter, *args):
        self.__current_pixels = ip.apply(self.__current_pixels, filter, *args)
        self.__history.append(self.__current_pixels.copy())

    def reset(self):
        self.__current_pixels = self.__original_pixels.copy()
        self.__history.clear()

    def undo(self):
        if (len(self.__history) > 1):
            self.__history.pop()
            self.__current_pixels = self.__history[-1].copy()
    
    def update_window(self, window : sg.Window, key='image'):
        image = Image.fromarray(self.__current_pixels.astype(np.uint8)).convert('RGB')
        image.thumbnail((400,400))
        data = io.BytesIO()
        image.save(data, format='PNG')
        window[key].update(data=data.getvalue())
        del image

    def save(self, name = "Modified.png"):
        image = Image.fromarray(self.__current_pixels.astype(np.uint8)).convert('RGB')
        image.save(name)

