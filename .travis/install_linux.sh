#!/usr/bin/env bash

set -x # Print command traces before executing command

set -e # Exit immediately if a simple command exits with a non-zero status.

set -o pipefail # Return value of a pipeline as the value of the last command to
                # exit with a non-zero status, or zero if all commands in the
                # pipeline exit successfully.

# check ubuntu version
lsb_release -a

# freetype v2.3.0 installation, some versions of matplotlib require it
# docker image has only freetype v2.2
install_freetype() {
    wget http://downloads.sourceforge.net/freetype/freetype-2.3.0.tar.gz
    tar -zxvf freetype-2.3.0.tar.gz
    cd freetype-2.3.0
    ./configure --prefix=/usr
    make -j4
    sudo make install
    cd ..
}

# instruction valid for Ubuntu 14.04
if [[ $TOXENV == py27* ]] || [[ $TOXENV == pep8* ]] || [[ $TOXENV == py32* ]] || [[ $TOXENV == py33* ]] || [[ $TOXENV == py36* ]];
then
    sudo apt-get -qq update
#    install_freetype
    sudo apt-get install -y libblas-dev liblapack-dev gfortran python-wxgtk2.8 python-tk libfreetype6-dev
fi

# instruction valid for Ubuntu 14.04
if [[ $TOXENV == py35* ]];
then
    sudo apt-get -qq update
    sudo apt-get install -y libblas-dev liblapack-dev gfortran libfreetype6-dev
    pip install -U --pre -f http://wxpython.org/Phoenix/snapshot-builds/ wxPython_Phoenix
fi


pip install --upgrade virtualenv$VENVVER pip$PIPVER setuptools tox wheel

if [[ $TOXENV == py32 ]];
then
  pip install git+https://github.com/grzanka/python-versioneer.git@support_python32
else
  pip install --upgrade versioneer
fi
pip install -r requirements.txt
