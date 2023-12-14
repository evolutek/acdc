#!/bin/sh

. "./venv/bin/activate"

# libcamerify can be used for legacy camera system

filename="$1"
if [ "$filename" = "" ]; then
    filename="src/main.py"
fi

sudo bash -c ". ./venv/bin/activate; python "$filename""
r=$?

exit $r
