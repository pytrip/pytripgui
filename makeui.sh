#!/bin/sh
set -x # Print command traces before executing command
set -e # Exit immediately if a simple command exits with a non-zero status.

mkdir -p pytripgui/view/gen/
pyuic5 pytripgui/view/main_window.ui -o pytripgui/view/gen/main_window.py
pyuic5 pytripgui/view/trip_config.ui -o pytripgui/view/gen/trip_config.py
