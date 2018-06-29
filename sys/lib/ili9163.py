# MicroPython ILI9163 OLED driver, I2C and SPI interfaces

import time
from micropython import const
import framebuf

# Subclassing FrameBuffer provides support for graphics primitives
# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
class ILI9163(framebuf.FrameBuffer):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = bytearray(self.width * self.height // 8)

        self.palette = bytearray(self.height * 4)

        for y in range(0, self.height):
            pb = y * 4
            self.palette[pb + 0] = 0x00
            self.palette[pb + 1] = 0x00
            self.palette[pb + 2] = 0xff
            self.palette[pb + 3] = 0xff

        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HMSB)
        self.init_display()

    def set_line_range_palette(self, y0, y1, bcol, fcol):
        for y in range(y0, y1):
            pb = y * 4
            self.palette[pb + 0] = bcol & 0xff
            self.palette[pb + 1] = bcol >> 8
            self.palette[pb + 2] = fcol & 0xff
            self.palette[pb + 3] = fcol >> 8

    def init_display(self):
        self.write_cmd(0x11) # Exit Sleep

        time.sleep_ms(20)

        self.write_cmd(0x26, [0x04]) # Set Default Gamma
        self.write_cmd(0xB1, [0x0e,0x10]) # Set Frame Rate
        self.write_cmd(0xC0, [0x08,0]) # Set VRH1[4:0] & VC[2:0] for VCI1 & GVDD
        self.write_cmd(0xC1, [0x05]) # Set BT[2:0] for AVDD & VCL & VGH & VGL
        self.write_cmd(0xC5, [0x38,0x40]) # Set VMH[6:0] & VML[6:0] for VOMH & VCOML

        self.write_cmd(0x3a, [5]) # Set Color Format, 5=16 bit,3=12 bit
        self.write_cmd(0x36, [0xc8]) # RGB

        self.write_cmd(0x2A, [0,0,0,self.width]) # Set Column Address
        self.write_cmd(0x2B, [0,0,0,self.height + 32]) # Set Page Address

        self.write_cmd(0xB4, [0]) #  display inversion

        self.write_cmd(0xf2, [1]) # Enable Gamma bit
        self.write_cmd(0xE0, [0x3f,0x22,0x20,0x30,0x29,0x0c,0x4e,0xb7,0x3c,0x19,0x22,0x1e,0x02,0x01,0x00])
        self.write_cmd(0xE1, [0x00,0x1b,0x1f,0x0f,0x16,0x13,0x31,0x84,0x43,0x06,0x1d,0x21,0x3d,0x3e,0x3f])

        self.write_cmd(0x29) #  Display On
        self.write_cmd(0x2C) #  reset frame ptr

        self.fill(0)
        self.show()

    def poweroff(self):
        pass

    def poweron(self):
        self.write_cmd(0x29)

    def contrast(self, contrast):
        pass

    def invert(self, invert):
        pass

    def show(self):
        x0 = 0
        x1 = self.width - 1

        y0 = 32
        y1 = self.height + 32 - 1

        self.write_cmd(0x2A, [x0, 0, x1])
        self.write_cmd(0x2B, [y0, 0, y1])
        self.write_cmd(0x2C)
        self.write_data(self.buffer)


class ILI9163_SPI(ILI9163):
    def __init__(self, width, height, spi, dc, res, cs):
        self.rate = 10 * 1024 * 1024
        
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs

        self.res(1)
        time.sleep_ms(1)
        self.res(0)
        time.sleep_ms(10)
        self.res(1)

        super().__init__(width, height)

    def write_cmd(self, cmd, data=None):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))

        if data != None:
            self.cs(1)
            self.dc(1)
            self.cs(0)
            self.spi.write(bytearray(data))

        self.cs(1)

    def write_data(self, buf):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)

        line_buffer = bytearray(self.width * 2)
        
        # 32 lines of padding...
        for _ in range(0, 32):
            self.spi.write(line_buffer)
        
        for y in range(0, self.height):
            pb = y * 4

            bcoll = self.palette[pb + 0]
            bcolh = self.palette[pb + 1]
            fcoll = self.palette[pb + 2]
            fcolh = self.palette[pb + 3]

            for x in range(0, self.width // 8):
                b = buf[y * (self.width // 8) + x]
                
                for i in range(0, 8):
                    bit = b & 1
                    b = b >> 1

                    px = x * 8 + i
                    bo = px * 2

                    coll = fcoll if bit == 1 else bcoll
                    colh = fcolh if bit == 1 else bcolh

                    line_buffer[bo + 0] = coll
                    line_buffer[bo + 1] = colh

            self.spi.write(line_buffer)

        self.cs(1)

# Convert RGB888 to BRG565
# ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

# Sample code
# ===========

# HSPI = 1
# VSPI = 2

# from machine import Pin, SPI
# spi = SPI(VSPI, sck=Pin(18), mosi=Pin(23))

# ili = ILI9163_SPI(128, 128, spi, Pin(2), Pin(4), Pin(15))

# ili.text('Hello World', 0, 0, 1)
