"""
    This file is part of pytripgui.

    pytripgui is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pytripgui is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pytripgui.  If not, see <http://www.gnu.org/licenses/>
"""
import logging
import ConfigParser as configparser  # this is python2 specific

from pytripgui.util import get_user_directory

logger = logging.getLogger(__name__)

class Settings:
    """ Class for interacting with saved configurations
    """
    def __init__(self):
        import os
        self.path = os.path.join(get_user_directory(), "settings.dat")
        self.config = configparser.SafeConfigParser()  # this is python2 specific

    def load(self, key):
        """
        Looks up a value in the settings file.
        :params str key: string in the form of 'trip98.spc.z6.rifi3'
        :retruns: a string holding the result.
        """
        self.config.read(self.path)

        # for 'trip98.spc.z6.rifi3' the first word before the dot is the section.
        sec, subkey = key.split('.', 1)
        return self.config.get(sec, subkey)  # this is python2 specific

    def save(self, key, value):
        """
        Save a value for key. If config section does not exist, it is created.
        :params str key:  string in the form of 'trip98.spc.z6.rifi3'
        :params str value: the value to be stored. Must be string format.
        """

        self.config.read(self.path)

        # for 'trip98.spc.z6.rifi3' key the first word before the dot is the section.
        sec, subkey = key.split('.', 1)

        if not self.config.has_section(sec):
            self.config.add_section(sec)
            
        self.config.set(sec, subkey, value)  # this is python2 specific

        with open(self.path, 'wb') as configfile:
            self.config.write(configfile)
