#!/usr/bin/env bash

set -x # Print command traces before executing command

set -e # Exit immediately if a simple command exits with a non-zero status.

set -o pipefail # Return value of a pipeline as the value of the last command to
                # exit with a non-zero status, or zero if all commands in the
                # pipeline exit successfully.


# make bdist universal package
pip install wheel

# install latest version of numpy assuming it will be consistent with numpy used to built pytrip98
# TODO - this should be fixed
pip install numpy -U

# first call to version method would generate VERSION  file
PYTHONPATH=. python pytripgui/main.py --version
python setup.py bdist_wheel

# makes source package
python setup.py sdist

# install the package
pip install dist/*whl

# test if it works
pytripgui --version
pytripgui --help

# cleaning
rm -rf dist
rm -rf build
