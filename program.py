import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
from Filter import *
import numpy

sg.theme('Dark Grey 13')

original = Image.open('Image.png')
image = Image.open('Image.png')

filters = [
    [sg.Text('Filters:')],
    [sg.Button('Inverse'), sg.Button('Grayscale'), sg.Button('Monochrome'), sg.Button('Screen'), sg.Button('Multiply'), sg.Button('Color Dodge')],
]

adjustments = [
    [sg.Text('Adjustments:')],
    [sg.Button('Brightness'), sg.Button('Contrast')],
]

layout = [
    [sg.Button('Save'), sg.Button('Reset')],
    [sg.HorizontalSeparator()],
    [sg.Column(adjustments)],
    [sg.Column(filters)],
    [sg.Image(size=image.size, key='image')],
]

window = sg.Window('Python Image Editor', layout, finalize=True)

def update_image(window, image, key='image'):
    data = io.BytesIO()
    image.save(data, format='PNG')
    window[key].update(data=data.getvalue())

def replace(target : Image, source : Image):
    target.resize(source.size)
    target.paste(source)

update_image(window, image)

while True:
    event, values = window.read()

    if event == 'Save':
        image.save('Modified.png')

    if event == 'Reset':
        replace(image, original)
        update_image(window, image)

    if event == 'Inverse':
        apply(image, inverse)
        update_image(window, image)

    if event == 'Grayscale':
        apply(image, grayscale)
        update_image(window, image)

    if event in ['Monochrome', 'Contrast', 'Brightness']:
        copy = Image.new(image.mode, image.size)
        copy.paste(image)
        
        if event == 'Monochrome':
            sl_range = (0, 255)
            sl_def = 255/2
            toApply = mono
            apply(copy, toApply, sl_def)
        elif event == 'Contrast':
            sl_range = (0, 1000)
            sl_def = 100
            toApply = contrast
        else:
            sl_range = (-255, 255)
            sl_def = 0
            toApply = brightness
        

        layoutPopup = [
            [sg.Image(size=copy.size, key='image')],
            [sg.Text('Amount:')],
            [sg.Slider(range=sl_range, enable_events=True, size=(copy.size[0]/9,20), default_value=sl_def, key='slider', orientation='h')],
            [sg.Button('OK'), sg.Button('Preview'), sg.Checkbox('Live Preview (laggy)', key='live_preview')]
        ]
        popup = sg.Window(event, layoutPopup, finalize=True)
        val = -1

        update_image(popup, copy)
        replace(copy, image)

        while True:
            nest_event, nest_values = popup.read()

            if (nest_event == 'Preview' or nest_event == 'slider' and nest_values['live_preview'] == True):
                apply(copy, toApply, int(nest_values['slider'])),
                update_image(popup, copy)
                replace(copy, image)
                

            if (nest_event == 'OK'):
                apply(image, toApply, int(nest_values['slider']))
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
            [sg.Text('R:'), sg.Slider(range=(0,255), size=(copy.size[0]/9 - 3,20), key='R', enable_events = True, orientation='h')],
            [sg.Text('G:'), sg.Slider(range=(0,255), size=(copy.size[0]/9 - 3,20), key='G', enable_events = True, orientation='h')],
            [sg.Text('B:'), sg.Slider(range=(0,255), size=(copy.size[0]/9 - 3,20), key='B', enable_events = True, orientation='h')],
            [sg.Button('OK'), sg.Button('Preview'), sg.Checkbox('Live preview (laggy)', key='live_preview')]
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

            if (nest_event == 'Preview' or nest_event in ['R', 'G', 'B'] and nest_values['live_preview'] == True):
                replace(copy, image)
                tempVals = [nest_values['R'], nest_values['G'], nest_values['B'], 255] 
                apply(copy, toApply, tempVals)
                update_image(popup, copy)

            if (nest_event == 'OK'):
                tempVals = [nest_values['R'], nest_values['G'], nest_values['B'], 255] 
                apply(image, toApply, tempVals)
                update_image(window, image)
                break
            if (nest_event == sg.WINDOW_CLOSED):
                break

        popup.close()

    if event == sg.WINDOW_CLOSED:
        break

window.close()