from machine import Pin, I2C
i2c = I2C(scl=Pin(4), sda=Pin(5))

from ssd1306 import SSD1306_I2C
# oled = SSD1306_I2C(128, 64, i2c)

LINE_HEIGHT = 12

def printLine(msg, line):
    pass
    # oled.fill_rect(0, line * LINE_HEIGHT, 127, LINE_HEIGHT, 0)
    # oled.text(msg, 0, line * LINE_HEIGHT)
    # oled.show()
