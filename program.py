import io
import PySimpleGUI as sg
from PIL import Image
import ImageProcessor as ip

def update_image(window : sg.Window, image : Image, key='image'):
    """Updates the window's image with a given image"""
    data = io.BytesIO()
    image.save(data, format='PNG')
    window[key].update(data=data.getvalue())

def replace(target : Image, source : Image):
    """Replaces 'target' with 'source' in place"""
    target.resize(source.size)
    target.paste(source)

def main():
    """Main method"""
    sg.theme('Dark Grey 8')

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
    update_image(window, image)
    while True:
        event, values = window.read()

        if event == 'Save':
            image.save('Modified.png')

        if event == 'Reset':
            replace(image, original)
            update_image(window, image)

        if event == 'Inverse':
            ip.apply(image, ip.inverse)
            update_image(window, image)

        if event == 'Grayscale':
            ip.apply(image, ip.grayscale)
            update_image(window, image)

        if event in ['Monochrome', 'Contrast', 'Brightness']:
            copy = Image.new(image.mode, image.size)
            copy.paste(image)

            sl_text = 'Amount:'

            if event == 'Monochrome':
                sl_range = (0, 255)
                sl_def = 255 / 2
                sl_text = 'Threshold:'
                to_apply = ip.mono
                ip.apply(copy, to_apply, sl_def)

            elif event == 'Contrast':
                sl_range = (0, 1000)
                sl_def = 100
                to_apply = ip.contrast

            elif event == 'Brightness':
                sl_range = (-255, 255)
                sl_def = 0
                to_apply = ip.brightness

            layout_popup = [
                [sg.Image(size=copy.size, key='image')],
                [sg.Text(sl_text)],
                [sg.Slider(range=sl_range, enable_events=True, size=(copy.size[0]/9,20), default_value=sl_def, key='slider', orientation='h')],
                [sg.Button('OK'), sg.Button('Preview'), sg.Checkbox('Live Preview (laggy)', key='live_preview')]
            ]
            popup = sg.Window(event, layout_popup, finalize=True)

            update_image(popup, copy)
            replace(copy, image)

            while True:
                nest_event, nest_values = popup.read()

                if nest_event == 'Preview' or nest_event == 'slider' and bool(nest_values['live_preview']):
                    ip.apply(copy, to_apply, int(nest_values['slider']))
                    update_image(popup, copy)
                    replace(copy, image)

                if nest_event == 'OK':
                    ip.apply(image, to_apply, int(nest_values['slider']))
                    update_image(window, image)
                    break

                if nest_event == sg.WINDOW_CLOSED:
                    break

            popup.close()

        if event in ['Screen', 'Multiply', 'Color Dodge']:
            copy = Image.new(image.mode, image.size)
            copy.paste(image)

            layout_popup = [
                [sg.Image(size=copy.size, key='image')],
                [sg.Text('R:'), sg.Slider(range=(0,255), size=(copy.size[0]/9 - 3,20), key='R', enable_events = True, orientation='h')],
                [sg.Text('G:'), sg.Slider(range=(0,255), size=(copy.size[0]/9 - 3,20), key='G', enable_events = True, orientation='h')],
                [sg.Text('B:'), sg.Slider(range=(0,255), size=(copy.size[0]/9 - 3,20), key='B', enable_events = True, orientation='h')],
                [sg.Button('OK'), sg.Button('Preview'), sg.Checkbox('Live preview (laggy)', key='live_preview')]
            ]

            popup = sg.Window(event, layout_popup, finalize=True)
            update_image(popup, copy)

            if event == 'Screen':
                to_apply = ip.screen
            elif event == 'Multiply':
                to_apply = ip.multiply
            else:
                to_apply = ip.color_dodge

            while True:
                nest_event, nest_values = popup.read()

                if nest_event == 'Preview' or nest_event in ['R', 'G', 'B'] and bool(nest_values['live_preview']):
                    replace(copy, image)
                    temp_vals = [nest_values['R'], nest_values['G'], nest_values['B'], 255]
                    ip.apply(copy, to_apply, temp_vals)
                    update_image(popup, copy)

                if nest_event == 'OK':
                    temp_vals = [nest_values['R'], nest_values['G'], nest_values['B'], 255]
                    ip.apply(image, to_apply, temp_vals)
                    update_image(window, image)
                    break
                if nest_event == sg.WINDOW_CLOSED:
                    break

            popup.close()

        if event == sg.WINDOW_CLOSED:
            break

    window.close()

if __name__ == '__main__':
    main()
