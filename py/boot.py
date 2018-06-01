import oled

oled.printLine('Starting...', 0)

import wifi
import json
import gc

gc.collect()

wifi.auto_connect()

gc.collect()

import webrepl

webrepl.start(password='')

gc.collect()

oled.printLine('WebREPL started', 4)

import panel

panel.start_panel()

gc.collect()


# counter = store.load('counter', 0)
# printLine(str(counter), 2)
# counter = counter + 1
# store.save('counter', counter)
