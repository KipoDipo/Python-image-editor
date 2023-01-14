"""Some docstring"""
from PIL import Image

im = Image.open('Image.png')

def edit(img : Image, modify):
    """Edits an image with a given function"""
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            modify(img, (x, y))

def invert(img : Image, *pos):
    """Inverts an image"""
    pixel = img.getpixel(*pos)
    img.putpixel(*pos, (255 - pixel[0], 255 - pixel[1], 255 - pixel[2], pixel[3]))

def grayscale(img : Image, *pos):
    """Inverts an image"""
    pixel = img.getpixel(*pos)
    img.putpixel(*pos, (
        round(0.299 * pixel[0]),
        round(0.587 * pixel[1]),
        round(0.114 * pixel[2]),
        pixel[3]))

edit(im, grayscale)

im.save("Inverted.png")
