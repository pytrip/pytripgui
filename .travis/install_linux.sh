#!/usr/bin/env bash

set -x # Print command traces before executing command

set -e # Exit immediately if a simple command exits with a non-zero status.

set -o pipefail # Return value of a pipeline as the value of the last command to
                # exit with a non-zero status, or zero if all commands in the
                # pipeline exit successfully.

# check ubuntu version

# instruction valid for Ubuntu 14.04
#sudo apt-get -qq update
# pkg-config libwxgtk2.8-dev freeglut3-dev
# http://tutorialforlinux.com/2014/11/09/how-to-install-wxpython-python-3-on-ubuntu-14-04-trusty-lts-32-64bit-easy-guide/
# http://stackoverflow.com/questions/27240143/installing-wxpython-on-ubuntu-14-04
#sudo apt-get install -y libblas-dev liblapack-dev gfortran python-wxgtk2.8 python-tk libfreetype6-dev libwxgtk2.8-dev libwxgtk-media2.8-dev libwxgtk-media2.8-0 libwxgtk-media3.0-0  libwxgtk2.8-0 make gcc libgtkgl2.0-dev libgstreamer* libwebkit-dev pkg-config freeglut3-dev
#pip install -U --trusted-host wxpython.org --pre -f http://wxpython.org/Phoenix/snapshot-builds/ wxPython_Phoenix==3.0.3.dev2487+3b86464

pip install --upgrade pip setuptools wheel

pip install -r requirements.txt
