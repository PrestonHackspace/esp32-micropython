#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    OS=linux
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS=osx
else
    echo 'Invalid OS'
    exit 1
fi

yarn
yarn run mount-sys-$OS
yarn run bundle
yarn run umount-sys-$OS
yarn run flash-sys
