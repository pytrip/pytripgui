mkdir -p pytripgui\view\gen\
pyuic5 pytripgui\view\main_window.ui -o pytripgui\view\gen\main_window.py
pyuic5 pytripgui\view\trip_config.ui -o pytripgui\view\gen\trip_config.py
pyuic5 pytripgui\view\field.ui -o pytripgui\view\gen\field.py
pyuic5 pytripgui\view\plan.ui -o pytripgui\view\gen\plan.py
