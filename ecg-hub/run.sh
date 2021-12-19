#!/bin/sh

export QT_PLUGIN_PATH="/home/tomek/PracaInzynierska/wireless-ecg-monitor/ecg-hub/venv/lib/python3.8/site-packages/PyQt5/Qt5/plugins"
./venv/bin/python main.py "$@"
