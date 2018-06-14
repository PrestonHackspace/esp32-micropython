import gc
import webrepl
from lib import oled
from lib import wifi
from lib import panel

oled.printLine('Starting...', 0)

gc.collect()

wifi.auto_connect()

gc.collect()

webrepl.start(password='')

gc.collect()

oled.printLine('WebREPL started', 4)

panel.start_panel()

gc.collect()

try:
    from user import main
except:
    print('Could not find main start up script')
