import threading
import os
import serial
from pynput.mouse import Button, Controller


SERIAL_PORT = os.environ.get('BTN_PORT')
BAUDRATE = os.environ.get('BTN_RATE')
BUTTON_POSITION = [int(v) for v in os.environ.get('BTN_POS').split(',')]


mouse = Controller()


class ClickMouse(threading.Thread):
    def __init__(self, position, button=Button.left):
        super(ClickMouse, self).__init__()
        self.button = button
        self.position = position

    def click_button(self):
        mouse.position = self.position
        mouse.click(self.button)


click_thread = ClickMouse(BUTTON_POSITION)
click_thread.start()


class InputHandler(object):
    initial_bytes = b'!3FFF00'

    def __init__(self):
        self._initial = [pin for pin in self.parse_data(self.initial_bytes)]
        self._data = self._initial.copy()

    def parse_data(self, value):
        """ Parse bytes to values """
        if value[0] == b'!'[0]:
            pin13to8 = str(bin(int('0x' + value[1:3].decode(), 16))[2:]).zfill(6)
            pin0_7 = str(bin(int('0x' + value[3:5].decode(), 16))[2:]).zfill(8)
            return pin13to8 + pin0_7

    def data(self, value):
        """ Set values for pins from parsed data """
        if value:
            for (idx, pin_data) in enumerate(reversed(self.parse_data(value))):
                if self._data[idx] != pin_data:
                    self.pin_changed(idx, pin_data)

                    if self._initial[idx] == pin_data:
                        self.pin_pressed(idx)
                self._data[idx] = pin_data

    def pin_changed(self, idx, value):
        """ Handle pin changed value """

    def pin_pressed(self, idx):
        """ Handle pin pressed (changed value to initial) """
        if idx == 0:
            click_thread.click_button()


port = serial.Serial(SERIAL_PORT, BAUDRATE)
handler = InputHandler()


while True:
    port.write(b'$086\r')
    handler.data(port.read(8))
