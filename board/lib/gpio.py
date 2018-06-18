import machine
import time

class LED:
    def __init__(self, pin):
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.state = 0
    def on(self):
        self.state = 1
        self.pin.value(1)
    def off(self):
        self.state = 0
        self.pin.value(0)
    def value(self):
        return self.state

class Buzzer:
    def __init__(self, pin):
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.state = 0
    def on(self):
        self.state = 1
        self.pin.value(1)
    def off(self):
        self.state = 0
        self.pin.value(0)
    def value(self):
        return self.state
        
class Button:
    def __init__(self, pin):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
    def wait_for_press(self):
        while True:
            if self.pin.value() == 1:
                break
            time.sleep(0.1)