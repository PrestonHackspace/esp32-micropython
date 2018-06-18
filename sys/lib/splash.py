from oled import oled

f = open('/white-logo.bmp', 'rb')

f.read(1146)

for l in range(0, 23):
    line = f.read(128)

    y = 63 - l
    x = 0

    for pixel in line:
        if pixel == 0:
            oled.pixel(x, y, 0)
        else:
            oled.pixel(x, y, 1)

        x = x + 1

oled.show()

f = None
