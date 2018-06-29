from screen import fb

if fb != None:
    f = open('/white-logo.bmp', 'rb')

    f.read(1146)

    for l in range(0, 23):
        line = f.read(128)

        y = 63 - l
        x = 0

        for pixel in line:
            if pixel == 0:
                fb.pixel(x, y, 0)
            else:
                fb.pixel(x, y, 1)

            x = x + 1

    try:
        fb.set_line_range_palette(40, 63, 0b1111100000000000, 0xffff)
    except:
        pass

    fb.show()

    f = None
