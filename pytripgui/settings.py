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
import sys
import logging
import ConfigParser as configparser  # this is python2 specific

from pytripgui.util import get_user_directory

if getattr(sys, 'frozen', False):
    from wx.lib.pubsub import setuparg1  # noqa
    from wx.lib.pubsub import pub
else:
    try:
        from wx.lib.pubsub import Publisher as pub
    except:
        from wx.lib.pubsub import setuparg1  # noqa
        from wx.lib.pubsub import pub

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
        :retruns: a string holding the result. If key is not found, return empty string.
        """
        self.config.read(self.path)

        # for 'trip98.spc.z6.rifi3' the first word before the dot is the section.
        _sec, _opt = key.split('.', 1)

        if not self.config.has_section(_sec):
            logger.debug("Settings: section {:s} not found, returning empty string".format(_sec))
            return ""
        if not self.config.has_option(_sec, _opt):
            logger.debug("Settings: option {:s} not found, returning empty string".format(_opt))
            return ""

        # return value is always guaranteed to be a string.
        return self.config.get(_sec, _opt)  # this is python2 specific

    def save(self, key, value):
        """
        Save a value for key. If config section does not exist, it is created.
        :params str key:  string in the form of 'trip98.spc.z6.rifi3'
        :params str value: the value to be stored. Must be string format.
        """

        self.config.read(self.path)

        # for 'trip98.spc.z6.rifi3' key the first word before the dot is the section.
        _sec, _opt = key.split('.', 1)

        if not self.config.has_section(_sec):
            self.config.add_section(_sec)

        self.config.set(_sec, _opt, value)  # this is python2 specific

        with open(self.path, 'wb') as configfile:
            self.config.write(configfile)

        text = "Updated {:s}".format(self.path)
        pub.sendMessage("statusbar.update", {"number": 0, "text": text})
