# ESP32 MicroPython

Very rough install guide...

## Requirements

    Node.js (with `yarn` if building)
    Python 3
    esptool.py (`pip3 install esptool`)

## Environment

Need to discover port path on your system. Typically examples:

For macOS:

    export ESPTOOL_PORT=/dev/cu.SLAB_USBtoUART

For Windows (use Device Manager to discover the actual port number):

    export ESPTOOL_PORT=COM3

For Linux (the default):

    export ESPTOOL_PORT=/dev/ttyUSB0

## Quick Install

    npm run flash-micropython
    npm run flash-sys

## Build (for developers)

Build the panel web app:

    cd panel
    yarn
    yarn run build
    cd ..

(Optional) Clone and build EduBlocks (must reside in the parent directory to this one):

    cd ..
    git clone git@github.com:AllAboutCode/edublocks-micropython.git
    cd edublocks-micropython
    yarn
    yarn run build
    cd ../../esp32-micropython

Bundle assets and flash on to ESP32:

    yarn
    yarn run mount-sys-linux         # Or: yarn run mount-sys-osx
    yarn run bundle
    yarn run umount-sys-linux        # Or: yarn run umount-sys-osx
    yarn run flash-micropython
    yarn run flash-sys
