# ESP32 MicroPython

Very rough install guide...

## Requirements

    Node.js
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

    yarn run flash-micropython
    yarn run flash-fs

## Build (for developers)

Build the panel web app:

    cd panel
    yarn
    yarn run build
    cd ..

Build EduBlocks:

    TODO

Bundle assets and flash on to ESP32:

    yarn
    yarn run mount-fs-osx
    yarn run bundle
    yarn run flash-micropython
    yarn run flash-fs
