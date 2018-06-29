import sys
import gc
import webrepl
from lib import screen
from lib import wifi
from lib import panel

try:
    screen.fb.set_line_range_palette(0, 12, 0b1111100000011111, 0x0000)
    screen.fb.set_line_range_palette(12, 24, 0b0000011111100000, 0xffff)

    screen.fb.set_line_range_palette(108, 120, 0b0000011111111111, 0x0000)
    screen.fb.set_line_range_palette(120, 122, 0b1111100000000000, 0xffff)
    screen.fb.set_line_range_palette(122, 124, 0b1111100000000000, 0xffff)
    screen.fb.set_line_range_palette(124, 126, 0b0000011111000000, 0xffff)
    screen.fb.set_line_range_palette(126, 128, 0b1111111111000000, 0xffff)
    screen.print_line('Pretty colours!', 9)
except:
    pass

screen.print_line('Starting...', 0)

gc.collect()

wifi.auto_connect()

gc.collect()

webrepl.start(password='')

gc.collect()

screen.print_line('WebREPL started', 4)

panel.start_panel()

gc.collect()

sys.path.append('/user')

from lib import splash

try:
    import main
except:
    print('Could not find main start up script')
