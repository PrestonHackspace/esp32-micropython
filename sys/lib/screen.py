try:
    from machine import Pin, I2C
    i2c = I2C(scl=Pin(4), sda=Pin(5))

    from ssd1306 import SSD1306_I2C
    fb = SSD1306_I2C(128, 64, i2c)

    COL = 1
except:
    fb = None

if fb == None:
    try:
        VSPI = 2

        from machine import Pin, SPI
        spi = SPI(VSPI, sck=Pin(18), mosi=Pin(23))

        from ili9163 import ILI9163_SPI
        fb = ILI9163_SPI(128, 128, spi, Pin(2), Pin(4), Pin(15))

        COL = 1
    except:
        fb = None

LINE_HEIGHT = 12


def print_line(msg, line):
    if fb == None:
        print('OLED: ' + msg)
        return

    nudge_y = 2

    fb.fill_rect(0, line * LINE_HEIGHT + nudge_y, 127, LINE_HEIGHT, 0)
    fb.text(msg, 0, line * LINE_HEIGHT + nudge_y, COL)
    fb.show()
