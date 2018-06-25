#!/bin/bash

cd ../edublocks-micropython
yarn
yarn run build

cd ../esp32-micropython/panel
yarn
yarn run build

cd ../

yarn
yarn run mount-sys-linux
yarn run bundle
yarn run umount-sys-linux
yarn run flash-micropython
yarn run flash-sys
