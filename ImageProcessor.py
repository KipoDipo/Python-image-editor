"""Image processor"""
from PIL import Image
import numpy as np

def replace(target : Image, source : Image):
    """Replaces 'target' with 'source' in place"""
    target.resize(source.size)
    target.paste(source)

def apply_fast(pixels, apply_filter, *args):
    """Faster implementation"""
    return apply_filter(pixels, *args)

def apply(img : Image, apply_filter, *args):
    """Applies a filter on a given image"""
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixel = img.getpixel((x, y))
            apply_filter(img, x, y, pixel, *args)

def inverse_fast(pixels):
    return 255 - pixels

def grayscale_fast(pixels):
    grayVec = [0.299, 0.578, 0.114] # gray vec formula
    gray = np.dot(pixels[..., :3], grayVec) # 2D gray matrix
    pixels[..., 0] = gray
    pixels[..., 1] = gray
    pixels[..., 2] = gray
    return pixels

def mono_fast(pixels, *args):
    grayVec = [0.299, 0.578, 0.114] # gray vec formula
    gray = np.dot(pixels[..., :3], grayVec) # 2D gray matrix
    
    threshold = 127
    if len(args) > 0:
        threshold = 255 - args[0]
    gray[gray>threshold] = 255
    gray[gray<=threshold] = 0
    pixels[..., 0] = gray
    pixels[..., 1] = gray
    pixels[..., 2] = gray
    return pixels

def multiply_fast(pixels, *color):
    if (len(color) == 0):
        return pixels

    a = pixels.astype(np.float64) / 255
    b =  np.asarray(color) / 255
    pixels[..., 0] = 255 * a[..., 0] * b[..., 0]  
    pixels[..., 1] = 255 * a[..., 1] * b[..., 1]  
    pixels[..., 2] = 255 * a[..., 2] * b[..., 2] 

    return pixels

def screen_fast(pixels, *color):
    if (len(color) == 0):
        return pixels

    a = pixels.astype(np.float64) / 255
    b =  np.asarray(color) / 255
    pixels[..., 0] = 255 * (1 - (1 - a[..., 0]) * (1 - b[..., 0]))  
    pixels[..., 1] = 255 * (1 - (1 - a[..., 1]) * (1 - b[..., 1]))  
    pixels[..., 2] = 255 * (1 - (1 - a[..., 2]) * (1 - b[..., 2])) 

    return pixels

#I actually discovered this by accident while trying to figure out how to do 'screen', turns out this is exactly how 'color dodge' works
def color_dodge_fast(pixels, *color):
    if (len(color) == 0):
        return pixels
    color = color[0]

    pixels = pixels.astype(np.float64)

    pixels[..., 0] *= 255 if color[0] == 255 else 255/(255 - color[0]) 
    pixels[..., 1] *= 255 if color[1] == 255 else 255/(255 - color[1]) 
    pixels[..., 2] *= 255 if color[2] == 255 else 255/(255 - color[2]) 
    pixels[pixels > 255] = 255
    return pixels

def contrast_fast(pixels, *args):
    m = pixels * (args[0] / 100.0)
    m[m > 255] = 255
    return m

def brightness_fast(pixels, *args):
    m = pixels.astype(np.uint16) + args[0]
    m[m < 0] = 0
    m[m >= 255] = 255
    return m
