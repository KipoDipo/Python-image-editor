import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
from Filter import *
import numpy

sg.theme('Dark Grey 13')

original = Image.open('Image.png')
image = Image.open('Image.png')

layout = [
    [sg.Button('Reset')],
    [sg.Button('Inverse'), sg.Button('Grayscale'), sg.Button('Monochrome')],
    [sg.Button('Screen'), sg.Button('Multiply'), sg.Button('Color Dodge')],
    [sg.Image(size=image.size, key='image')]
]

window = sg.Window('Title', layout, finalize=True)

def update_image(window, image):
    data = io.BytesIO()
    image.save(data, format='PNG')
    window['image'].update(data=data.getvalue())

def replace(img : Image, original):
    img.resize(original.size)
    img.paste(original)

update_image(window, image)
while True:
    event, values = window.read()

    if (event == 'Reset'):
        replace(image, original)
        update_image(window, image)

    if (event == 'Inverse'):
        apply(image, inverse)
        update_image(window, image)

    if (event == 'Monochrome'):
        copy = Image.new(image.mode, image.size)
        copy.paste(image)
        
        layoutPopup = [
            [sg.Image(size=copy.size, key='image')],
            [sg.Text('Threshold:')],
            [sg.Slider(range=(0,255), size=(copy.size[0]/9,20), default_value=127, key='slider', orientation='h')],
            [sg.Button('OK'), sg.Button('Preview')]
        ]
        popup = sg.Window(event, layoutPopup, finalize=True)
        val = -1
        update_image(popup, copy)

        while True:
            nest_event, nest_values = popup.read()
            if (nest_event == 'Preview'):
                replace(copy, image)
                apply(copy, mono, threshold = 255 - int(nest_values['slider'])),
                update_image(popup, copy)
            if (nest_event == 'OK'):
                apply(image, mono, threshold = 255 - int(nest_values['slider']))
                update_image(window, image)
                break
            if (nest_event == sg.WINDOW_CLOSED):
                break

        popup.close()

    if event in ['Screen', 'Multiply', 'Color Dodge']:
        copy = Image.new(image.mode, image.size)
        copy.paste(image)

        layoutPopup = [
            [sg.Image(size=copy.size, key='image')],
            [sg.Text('R:'), sg.Slider(range=(0,255), size=(copy.size[0]/9 - 3,20), key='R', orientation='h')],
            [sg.Text('G:'), sg.Slider(range=(0,255), size=(copy.size[0]/9 - 3,20), key='G', orientation='h')],
            [sg.Text('B:'), sg.Slider(range=(0,255), size=(copy.size[0]/9 - 3,20), key='B', orientation='h')],
            [sg.Button('OK'), sg.Button('Preview')]
        ]

        popup = sg.Window(event, layoutPopup, finalize=True)
        val = [-1, -1, -1]
        update_image(popup, copy)
        toApply = None
        if (event == 'Screen'):
            toApply = screen
        elif (event == 'Multiply'):
            toApply = multiply
        else:
            toApply = color_dodge

        while True:
            nest_event, nest_values = popup.read()

            if (nest_event == 'Preview'):
                replace(copy, image)
                tempVals = [nest_values['R'], nest_values['G'], nest_values['B'], 255] 
                apply(copy, toApply, color=tempVals),
                update_image(popup, copy)

            if (nest_event == 'OK'):
                tempVals = [nest_values['R'], nest_values['G'], nest_values['B'], 255] 
                apply(image, toApply, color=tempVals)
                update_image(window, image)
                break
            if (nest_event == sg.WINDOW_CLOSED):
                break

        popup.close()

    if (event == 'Grayscale'):
        apply(image, grayscale)
        update_image(window, image)

    if (event == sg.WINDOW_CLOSED):
        break


window.close()