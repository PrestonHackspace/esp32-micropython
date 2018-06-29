#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    OS=linux
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS=osx
else
    echo 'Invalid OS'
    exit 1
fi

cd ../edublocks-micropython
yarn
yarn run build

cd ../esp32-micropython/panel
yarn
yarn run build

cd ../

yarn
yarn run mount-sys-$OS
yarn run bundle
yarn run umount-sys-$OS
yarn run flash-micropython
yarn run flash-sys
