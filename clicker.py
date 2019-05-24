import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

CLICK_KEY = KeyCode(char='k')
EXIT_KEY = KeyCode(char='e')


class ClickMouse(threading.Thread):
    def __init__(self, position, button=Button.left):
        super(ClickMouse, self).__init__()
        self.button = button
        self.position = position

    def click(self):
        mouse.position = self.position
        mouse.click(self.button)


mouse = Controller()
pos = (1520, 510)
click_thread = ClickMouse(pos)
click_thread.start()


def on_press(key):
    if key == CLICK_KEY:
        click_thread.click()
    elif key == EXIT_KEY:
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
