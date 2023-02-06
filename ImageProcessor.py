"""Image processor"""
from PIL import Image
import numpy as np

def replace(target : Image, source : Image):
    """Replaces 'target' with 'source' in place"""
    target.resize(source.size)
    target.paste(source)

def apply(pixels : np.ndarray, apply_filter, *args):
    """Faster implementation"""
    return apply_filter(pixels, *args)

def inverse(pixels : np.ndarray):
    return 255 - pixels

def grayscale(pixels : np.ndarray):
    grayVec = [0.299, 0.578, 0.114] # gray vec formula
    gray = np.dot(pixels[..., :3], grayVec) # 2D gray matrix
    pixels[..., 0] = gray
    pixels[..., 1] = gray
    pixels[..., 2] = gray
    return pixels

def monochrome(pixels : np.ndarray, *args):
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

def multiply(pixels : np.ndarray, *color):
    if (len(color) == 0):
        return pixels

    a = pixels.astype(np.float64) / 255
    b =  np.asarray(color) / 255
    pixels[..., 0] = 255 * a[..., 0] * b[..., 0]  
    pixels[..., 1] = 255 * a[..., 1] * b[..., 1]  
    pixels[..., 2] = 255 * a[..., 2] * b[..., 2] 

    return pixels

def screen(pixels : np.ndarray, *color):
    if (len(color) == 0):
        return pixels

    a = pixels.astype(np.float64) / 255
    b =  np.asarray(color) / 255
    pixels[..., 0] = 255 * (1 - (1 - a[..., 0]) * (1 - b[..., 0]))  
    pixels[..., 1] = 255 * (1 - (1 - a[..., 1]) * (1 - b[..., 1]))  
    pixels[..., 2] = 255 * (1 - (1 - a[..., 2]) * (1 - b[..., 2])) 

    return pixels

#I actually discovered this by accident while trying to figure out how to do 'screen', turns out this is exactly how 'color dodge' works
def color_dodge(pixels : np.ndarray, *color):
    if (len(color) == 0):
        return pixels
    color = color[0]

    pixels = pixels.astype(np.float64)

    pixels[..., 0] *= 255 if color[0] == 255 else 255/(255 - color[0]) 
    pixels[..., 1] *= 255 if color[1] == 255 else 255/(255 - color[1]) 
    pixels[..., 2] *= 255 if color[2] == 255 else 255/(255 - color[2]) 
    pixels[pixels > 255] = 255
    return pixels

def contrast(pixels : np.ndarray, *args):
    m = pixels * (args[0] / 100.0)
    m[m > 255] = 255
    return m

def brightness(pixels : np.ndarray, *args):
    m = pixels.astype(np.uint16) + args[0]
    m[m < 0] = 0
    m[m >= 255] = 255
    return m

def rotate(pixels : np.ndarray, *args):
    pixels = np.rot90(pixels, k = args[0])
    return pixels

def flipud(pixels : np.ndarray):
    pixels = np.flipud(pixels)
    return pixels

def fliplr(pixels : np.ndarray):
    pixels = np.fliplr(pixels)
    return pixels