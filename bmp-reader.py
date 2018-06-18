f = open('white-logo.bmp', 'rb')

f.read(1146)

for i in range(0, 23):
    line = f.read(128)

    for pixel in line:
        if pixel == 0:
            print(' ', end = '')
        else:
            print('X', end = '')

