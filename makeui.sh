#!/bin/sh

set -x # Print command traces before executing command
set -e # Exit immediately if a simple command exits with a non-zero status.

pyuic5 pytripgui/view/main_window.ui > pytripgui/view/main_window.py
pyuic5 pytripgui/view/trip_config.ui > pytripgui/view/trip_config.py

