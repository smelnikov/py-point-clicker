# !/usr/bin/python
import daemon
import threading
import serial
from pynput.mouse import Button, Controller


SERIAL_PORT = "COM2"
BAUDRATE = 9600
BUTTON_POSITION = (1520, 510)


class ClickMouse(threading.Thread):
    def __init__(self, position, button=Button.left):
        super(ClickMouse, self).__init__()
        self.button = button
        self.position = position

    def click_button(self):
        mouse.position = self.position
        mouse.click(self.button)


mouse = Controller()
click_thread = ClickMouse(BUTTON_POSITION)
click_thread.start()


class InputHandler(object):
    def __init__(self):
        self.data = [None for i in range(0, 14)]

    def parse_data(self, value):
        if value[0] == '!':
            pin8_13 = str(bin(int('0x' + value[1] + value[2], 16))[2:]).zfill(6)
            pin0_7 = str(bin(int('0x' + value[3] + value[4], 16))[2:]).zfill(8)
            return pin8_13 + pin0_7

    def write_data(self, value):
        if value:
            for (idx, pin_data) in enumerate(reversed(self.parse_data(value))):
                if self.data[idx] and self.data[idx] != pin_data:
                    self.pin_changed(idx, pin_data)
                self.data[idx] = pin_data

    def pin_changed(self, idx, value):
        print 'Pin%s changed to %s' % (idx, value)
        if idx == 0:
            print 'Button clicked!'
            click_thread.click_button()


port = serial.Serial(SERIAL_PORT, BAUDRATE)
handler = InputHandler()


with daemon.DaemonContext():
    while True:
        port.write('$086\r')
        handler.write_data(port.read(8))
