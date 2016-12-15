#!/bin/bash

$PYTHON setup.py install --old-and-unmanageable

if [ $PY3K == 1 ]; then
    rm $SP_DIR/mistune.py
fi
