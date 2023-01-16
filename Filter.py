from PIL import Image

def apply(img : Image, apply_filter, *args):
    """Applies a filter on a given image"""
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixel = img.getpixel((x, y))
            apply_filter(img, x, y, pixel, *args)

def inverse(img : Image, x, y, pixel):
    """Inverses a pixel"""
    img.putpixel((x, y), (255 - pixel[0], 255 - pixel[1], 255 - pixel[2]))

def grayscale(img : Image, x, y, pixel):
    """Grayscales a pixel"""
    gray = round(0.299 * pixel[0]) + round(0.587 * pixel[1]) + round(0.114 * pixel[2])
    img.putpixel((x, y), (gray, gray, gray))

def mono(img : Image, x, y, pixel, *args):
    """Monochromes a pixel by a given threshold"""
    gray = round(0.299 * pixel[0]) + round(0.587 * pixel[1]) + round(0.114 * pixel[2])

    threshold = 127
    if len(args) > 0:
        threshold = 255 - args[0]

    val = 0 if gray < threshold else 255 
    img.putpixel((x, y), (val, val, val))

def multiply(img: Image, x, y, pixel, *args):
    """Multiplies a pixel by a given color (r, g, b)"""
    if len(args) > 0:
        color = args[0]
        
        a = [pixel[0]/255, pixel[1]/255, pixel[2]/255]
        b = [color[0]/255, color[1]/255, color[2]/255]
        change = [
            255 * a[0] * b[0], 
            255 * a[1] * b[1],
            255 * a[2] * b[2]]
        img.putpixel((x,y), (
            int(change[0]), 
            int(change[1]), 
            int(change[2])
            ))

def screen(img: Image, x, y, pixel, *args):
    """Screens pixel a by a given color (r, g, b)"""
    if len(args) > 0:
        color = args[0]

        a = [pixel[0]/255, pixel[1]/255, pixel[2]/255]
        b = [color[0]/255, color[1]/255, color[2]/255]
        change = [
            255 * (1 - (1 - a[0]) * (1 - b[0])),
            255 * (1 - (1 - a[1]) * (1 - b[1])),
            255 * (1 - (1 - a[2]) * (1 - b[2]))]

        img.putpixel((x,y), (
            int(change[0]), 
            int(change[1]), 
            int(change[2])
            ))

#I actually discovered this by accident while trying to figure out how to do 'screen', turns out this is exactly how 'color dodge' works
def color_dodge(img: Image, x, y, pixel, *args):
    """Color Dodges a pixel by a given color (r, g, b)"""
    if len(args) > 0:
        color = args[0]

        change = [
            pixel[0] * (255 if color[0] == 255 else 255/(255 - color[0])),
            pixel[1] * (255 if color[1] == 255 else 255/(255 - color[1])),
            pixel[2] * (255 if color[2] == 255 else 255/(255 - color[2]))
        ]
        img.putpixel((x,y), (
            int(change[0]), 
            int(change[1]), 
            int(change[2]) 
            ))

def contrast(img: Image, x, y, pixel, *args):
    """Applies contrast to a pixel by a given threshold"""
    c = 1
    if len(args) > 0:
        c = (args[0]) / 100.0
    change = [
        (pixel[0] * c),
        (pixel[1] * c),
        (pixel[2] * c),
    ]
    img.putpixel((x,y), (
        int(change[0]),
        int(change[1]),
        int(change[2])
        ))

def brightness(img: Image, x, y, pixel, *args):
    """Applies brightness to a pixel by a given threshold"""
    c = 1
    if len(args) > 0:
        c = (args[0])
    change = [
        (pixel[0] + c),
        (pixel[1] + c),
        (pixel[2] + c),
    ]
    img.putpixel((x,y), (
        int(change[0]),
        int(change[1]),
        int(change[2])
        ))