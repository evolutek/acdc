#!/bin/sh

. "./venv/bin/activate"

# libcamerify can be used for legacy camera system

filename="$1"
if [ "$filename" = "" ]; then
    filename="src/main.py"
fi

if [ "$QT_QPA_PLATFORM" = "wayland" ]; then
    export QT_QPA_PLATFORM=xcb
fi

sudo bash -c ". ./venv/bin/activate; python "$filename""
r=$?

exit $r
