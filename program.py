import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
from Filter import *
import numpy

sg.theme('Dark Grey 13')

original = Image.open('Image.png')
image = Image.open('Image.png')

first_col = [
    [sg.Text('Filters:')],
    [sg.Button('Inverse'), sg.Button('Grayscale'), sg.Button('Monochrome')],
    [sg.Button('Screen'), sg.Button('Multiply'), sg.Button('Color Dodge')],
]

second_col = [
    [sg.Text('Actions:')],
    [sg.Button('Rotate')],
    [sg.Button('Flip')],
]

layout = [
    [sg.Button('Save'), sg.Button('Reset')],
    [sg.Column(first_col), sg.VerticalSeparator(), sg.Column(second_col)],
    [sg.Image(size=image.size, key='image')],
]

window = sg.Window('Python Image Editor', layout, finalize=True)

def update_image(window, image):
    data = io.BytesIO()
    image.save(data, format='PNG')
    window['image'].update(data=data.getvalue())

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

    if event == 'Monochrome':
        copy = Image.new(image.mode, image.size)
        copy.paste(image)
        
        apply(copy, mono, threshold = 255 - 127),
        
        layoutPopup = [
            [sg.Image(size=copy.size, key='image')],
            [sg.Text('Threshold:')],
            [sg.Slider(range=(0,255), enable_events=True, size=(copy.size[0]/9,20), default_value=127, key='slider', orientation='h')],
            [sg.Button('OK'), sg.Button('Preview'), sg.Checkbox('Live Preview (laggy)', key='live_preview')]
        ]
        popup = sg.Window(event, layoutPopup, finalize=True)
        val = -1

        update_image(popup, copy)
        replace(copy, image)

        while True:
            nest_event, nest_values = popup.read()

            if (nest_event == 'Preview' or nest_event == 'slider' and nest_values['live_preview'] == True):
                apply(copy, mono, threshold = 255 - int(nest_values['slider'])),
                update_image(popup, copy)
                replace(copy, image)
                

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

    if event == 'Grayscale':
        apply(image, grayscale)
        update_image(window, image)

    if event == sg.WINDOW_CLOSED:
        break

window.close()