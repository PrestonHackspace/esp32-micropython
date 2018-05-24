# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from machine import Pin, I2C
i2c = I2C(scl=Pin(4), sda=Pin(5))

from ssd1306 import SSD1306_I2C
oled = SSD1306_I2C(128, 64, i2c)

from time import sleep

oled.fill(1)
oled.show()
sleep(0.25)

oled.fill(0)
oled.show()
sleep(0.25)

oled.pixel(0, 0, 1)
oled.show()
sleep(0.25)

oled.pixel(127, 63, 1)
oled.show()
sleep(0.25)

oled.text('Hello', 0, 0)
sleep(0.25)
oled.show()

oled.text('World', 0, 10)
sleep(0.25)
oled.show()
