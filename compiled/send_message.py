import webbrowser as web
import time
import win32gui #pywin32
from pynput.keyboard import Key, Controller
import json
import os


class Job:
    def __init__(self, text, num, repeat, index):
        self.text = text
        self.num = num
        self.repeat = repeat
        self. index = index
        self.appdata = os.environ['APPDATA'] + r'\WPPScheduler'

        self.send_message()
        self.send_enter()
        if self.repeat == 0:
            self.delete_message()

    def open_json(self):
        with open(self.appdata + r'\data.json', 'r') as file:
            data = json.load(file)
        return data

    def send_message(self):
        # Open Whatsapp and type message
        print(f'{self.text}, para o número {self.num}')
        web.open(f'https://web.whatsapp.com/send?phone={self.num}&text={self.text}')
        time.sleep(0.1)
        self.browser_window = win32gui.GetForegroundWindow() # gets browser window handle
        time.sleep(10)

    def send_enter(self):
        # Init keyboard
        keyboard = Controller()

        # Set browser as foreground window
        keyboard.press(Key.alt)
        win32gui.SetForegroundWindow(self.browser_window)
        keyboard.release(Key.alt)

        # Send enter
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    def delete_message(self):
        data = self.open_json()
        new_data = []
        for i, element in enumerate(data):
            if i == self.index:
                print(element)
                pass
            else:
                new_data.append(element)
        with open(self.appdata + r'\data.json', 'w') as file:
            json.dump(new_data, file, indent=4)