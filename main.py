import io
import PySimpleGUI as sg
import ImageProcessor as ip
from ImageEditor import ImageEditor

def main():
    """Main method"""
    sg.theme('Dark Grey 8')

    img = ImageEditor(image_path='Image.png')
    
    macro_src = ['macro_off.png', 'macro_on.png']
    macro_button = ['Record Macro', 'Save Macro']
    macro_functions = []
    macro_is_recording = False


    filters = [
        [sg.Text('Filters:')],
        [sg.Button('Inverse'), sg.Button('Grayscale'), sg.Button('Monochrome'), sg.Button('Screen'), sg.Button('Multiply'), sg.Button('Color Dodge')],
    ]

    adjustments = [
        [sg.Text('Adjustments:')],
        [sg.Button('Brightness'), sg.Button('Contrast')],
    ]

    layout = [
        [sg.Button('Save'), sg.Button('Reset'), sg.Button('Undo'), sg.Button(macro_button[0], key='MacroButton', size=(11, 1)), sg.Image(macro_src[0], key='macro'), sg.Button('Apply')],
        [sg.HorizontalSeparator()],
        [sg.Column(adjustments)],
        [sg.Column(filters)],
        [sg.Image(size=img.size(), key='image')],
    ]

    window = sg.Window('Python Image Editor', layout, finalize=True)
    img.update_window(window)
    
    while True:
        event, values = window.read()

        if event == 'MacroButton':
            macro_is_recording = not macro_is_recording
            if (macro_is_recording):
                macro_functions.clear()
            window['macro'].update(source=macro_src[int(macro_is_recording)])
            window['MacroButton'].update(text=macro_button[int(macro_is_recording)])
        
        if (event == 'Apply'):
            for x in macro_functions:
                img.edit(*x)
            img.update_window(window)

        if event == 'Save':
            img.save()

        if event == 'Reset':
            img.reset()
            img.update_window(window)

        if event == 'Undo':
            img.undo()
            if macro_is_recording:
                if len(macro_functions) > 0:
                    macro_functions.pop()
            img.update_window(window)

        if event == 'Inverse':
            img.edit(ip.inverse_fast)
            if macro_is_recording:
                macro_functions.append([ip.inverse_fast])

            img.update_window(window)

        if event == 'Grayscale':
            img.edit(ip.grayscale_fast)
            if macro_is_recording:
                macro_functions.append([ip.grayscale_fast])

            img.update_window(window)

        if event in ['Monochrome', 'Contrast', 'Brightness']:
            copy_img = ImageEditor(image_editor_copy=img)

            sl_text = 'Amount:'

            if event == 'Monochrome':
                sl_range = (0, 255)
                sl_def = 255 / 2
                sl_text = 'Threshold:'
                to_apply = ip.mono_fast
                copy_img.edit(to_apply, sl_def)

            elif event == 'Contrast':
                sl_range = (0, 1000)
                sl_def = 100
                to_apply = ip.contrast_fast

            elif event == 'Brightness':
                sl_range = (-255, 255)
                sl_def = 0
                to_apply = ip.brightness_fast

            layout_popup = [
                [sg.Image(size=copy_img.size(), key='image')],
                [sg.Text(sl_text)],
                [sg.Slider(range=sl_range, enable_events=True, size=(copy_img.size()[0]/9,20), default_value=sl_def, key='slider', orientation='h')],
                [sg.Button('OK'), sg.Button('Cancel'), sg.Button('Preview'), sg.Checkbox('Live Preview', key='live_preview', default=True)]
            ]
            popup = sg.Window(event, layout_popup, finalize=True)

            copy_img.update_window(popup)

            while True:
                nest_event, nest_values = popup.read()

                if nest_event == 'Preview' or nest_event == 'slider' and bool(nest_values['live_preview']):
                    copy_img.edit(to_apply, int(nest_values['slider']))
                    copy_img.update_window(popup)
                    copy_img.reset()

                if nest_event == 'OK':
                    img.edit(to_apply, int(nest_values['slider']))
                    if macro_is_recording:
                        macro_functions.append([to_apply, int(nest_values['slider'])])
                    img.update_window(window)
                    break

                if nest_event == 'Cancel' or nest_event == sg.WINDOW_CLOSED:
                    break

            popup.close()

        if event in ['Screen', 'Multiply', 'Color Dodge']:
            copy_img = ImageEditor(image_editor_copy=img)
            
            layout_popup = [
                [sg.Image(size=copy_img.size(), key='image')],
                [sg.Text('R:'), sg.Slider(range=(0,255), size=(copy_img.size()[0]/9 - 3,20), key='R', enable_events = True, orientation='h')],
                [sg.Text('G:'), sg.Slider(range=(0,255), size=(copy_img.size()[0]/9 - 3,20), key='G', enable_events = True, orientation='h')],
                [sg.Text('B:'), sg.Slider(range=(0,255), size=(copy_img.size()[0]/9 - 3,20), key='B', enable_events = True, orientation='h')],
                [sg.Button('OK'), sg.Button('Cancel'), sg.Button('Preview'), sg.Checkbox('Live preview', key='live_preview', default=True)]
            ]

            popup = sg.Window(event, layout_popup, finalize=True)

            copy_img.update_window(popup)

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
                    copy_img.edit(to_apply, temp_vals)
                    copy_img.update_window(popup)
                    copy_img.reset()

                if nest_event == 'OK':
                    temp_vals = [nest_values['R'], nest_values['G'], nest_values['B'], 255]
                    img.edit(to_apply, temp_vals)
                    if macro_is_recording:
                        macro_functions.append([to_apply, temp_vals])

                    img.update_window(window)
                    break
                if nest_event == 'Cancel' or nest_event == sg.WINDOW_CLOSED:
                    break

            popup.close()

        if event == sg.WINDOW_CLOSED:
            break

    window.close()

if __name__ == '__main__':
    main()
