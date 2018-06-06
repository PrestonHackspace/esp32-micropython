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


# counter = store.load('counter', 0)
# printLine(str(counter), 2)
# counter = counter + 1
# store.save('counter', counter)
