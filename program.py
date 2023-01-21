import io
import PySimpleGUI as sg
from PIL import Image
import ImageProcessor as ip
import numpy as np

def update_image(window : sg.Window, pixels : np.ndarray, key='image'):
    image = Image.fromarray(pixels.astype(np.uint8)).convert('RGB')
    data = io.BytesIO()
    image.save(data, format='PNG')
    window[key].update(data=data.getvalue())
    del image

def main():
    """Main method"""
    sg.theme('Dark Grey 8')

    original = Image.open('Image.png')
    orig_pixels = np.array(original)
    img_pixels = np.copy(orig_pixels)

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
        [sg.Image(size=original.size, key='image')],
    ]

    window = sg.Window('Python Image Editor', layout, finalize=True)
    update_image(window, img_pixels)
    while True:
        event, values = window.read()

        if event == 'Save':
            image = Image.fromarray(img_pixels.astype(np.uint8)).convert('RGB')
            image.save('Modified.png')

        if event == 'Reset':
            img_pixels = orig_pixels
            update_image(window, img_pixels)

        if event == 'Inverse':
            img_pixels = ip.apply_fast(img_pixels, ip.inverse_fast)
            update_image(window, img_pixels)

        if event == 'Grayscale':
            img_pixels = ip.apply_fast(img_pixels, ip.grayscale_fast)
            update_image(window, img_pixels)

        if event in ['Monochrome', 'Contrast', 'Brightness']:
            copy_pixels = img_pixels.copy()
            width = copy_pixels.shape[0]
            height = copy_pixels.shape[0]

            sl_text = 'Amount:'

            if event == 'Monochrome':
                sl_range = (0, 255)
                sl_def = 255 / 2
                sl_text = 'Threshold:'
                to_apply = ip.mono_fast
                copy_pixels = ip.apply_fast(copy_pixels, to_apply, sl_def)

            elif event == 'Contrast':
                sl_range = (0, 1000)
                sl_def = 100
                to_apply = ip.contrast_fast

            elif event == 'Brightness':
                sl_range = (-255, 255)
                sl_def = 0
                to_apply = ip.brightness_fast

            layout_popup = [
                [sg.Image(size=(width, height), key='image')],
                [sg.Text(sl_text)],
                [sg.Slider(range=sl_range, enable_events=True, size=(width/9,20), default_value=sl_def, key='slider', orientation='h')],
                [sg.Button('OK'), sg.Button('Cancel'), sg.Button('Preview'), sg.Checkbox('Live Preview', key='live_preview', default=True)]
            ]
            popup = sg.Window(event, layout_popup, finalize=True)

            update_image(popup, copy_pixels)

            while True:
                nest_event, nest_values = popup.read()

                if nest_event == 'Preview' or nest_event == 'slider' and bool(nest_values['live_preview']):
                    copy_pixels = ip.apply_fast(copy_pixels, to_apply, int(nest_values['slider']))
                    update_image(popup, copy_pixels)
                    copy_pixels = img_pixels.copy()

                if nest_event == 'OK':
                    img_pixels = ip.apply_fast(img_pixels, to_apply, int(nest_values['slider']))
                    update_image(window, img_pixels)
                    break

                if nest_event == 'Cancel' or nest_event == sg.WINDOW_CLOSED:
                    break

            popup.close()

        if event in ['Screen', 'Multiply', 'Color Dodge']:
            copy_pixels = img_pixels.copy()
            width = copy_pixels.shape[0]
            height = copy_pixels.shape[0]
            
            layout_popup = [
                [sg.Image(size=(width, height), key='image')],
                [sg.Text('R:'), sg.Slider(range=(0,255), size=(width/9 - 3,20), key='R', enable_events = True, orientation='h')],
                [sg.Text('G:'), sg.Slider(range=(0,255), size=(width/9 - 3,20), key='G', enable_events = True, orientation='h')],
                [sg.Text('B:'), sg.Slider(range=(0,255), size=(width/9 - 3,20), key='B', enable_events = True, orientation='h')],
                [sg.Button('OK'), sg.Button('Cancel'), sg.Button('Preview'), sg.Checkbox('Live preview', key='live_preview', default=True)]
            ]

            popup = sg.Window(event, layout_popup, finalize=True)
            update_image(popup, copy_pixels)

            if event == 'Screen':
                to_apply = ip.screen_fast
            elif event == 'Multiply':
                to_apply = ip.multiply_fast
            else:
                to_apply = ip.color_dodge_fast

            while True:
                nest_event, nest_values = popup.read()

                if nest_event == 'Preview' or nest_event in ['R', 'G', 'B'] and bool(nest_values['live_preview']):
                    temp_vals = [nest_values['R'], nest_values['G'], nest_values['B'], 255]
                    copy_pixels = ip.apply_fast(copy_pixels, to_apply, temp_vals)
                    update_image(popup, copy_pixels)
                    copy_pixels = img_pixels.copy()

                if nest_event == 'OK':
                    temp_vals = [nest_values['R'], nest_values['G'], nest_values['B'], 255]
                    img_pixels = ip.apply_fast(img_pixels, to_apply, temp_vals)
                    update_image(window, img_pixels)
                    break
                if nest_event == 'Cancel' or nest_event == sg.WINDOW_CLOSED:
                    break

            popup.close()

        if event == sg.WINDOW_CLOSED:
            break

    window.close()

if __name__ == '__main__':
    main()
