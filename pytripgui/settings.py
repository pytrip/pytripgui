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
import os
import json
import logging

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


class SettingsManager:
    """
    Manager for handling settings which are saved in .pytrip/ as JSON object.
    """
    def __init__(self):
        self.path = os.path.join(get_user_directory(), "preferences.dat")
        self.values = {}
        self.template = {}
        pub.subscribe(self.get_requested_value, "settings.value.request")
        pub.subscribe(self.get_requested_values, "settings.values.request")
        pub.subscribe(self.value_updated, "settings.value.updated")
        logger.debug("preferences path: {:s}".format(self.path))

    def value_updated(self, msg):
        for key, value in msg.data.iteritems():
            self.set_value(key, value)
            pub.sendMessage(key, value)

    def get_requested_value(self, msg):
        """ callback function for "settings.value.request" message
        """
        query = msg.data
        value = self.get_value(query)
        pub.sendMessage(msg.data, value)
        logger.debug("SettingsManager::get_requested_value: {:s} {:s}".format(msg.data, value))
        
    def get_requested_values(self, msg):
        """ callback function for "settings.values.request" message
        this one may contain multiple values, and interates over these, sending 
        one message back for each value.
        """
        _query = msg.data
        values = self.get_value(_query)
        for key, value in values.iteritems():
            pub.sendMessage(msg.data + "." + key, value)

    def load_settings(self, path=""):
        """ Loads the settings from path
        """
        if path == "":
            path = self.path
        if os.path.exists(path):
            with open(path, mode='r') as settings:
                try:
                    self.values = json.load(settings)
                except ValueError:
                    self.values = {}
        else:
            self.values = {}

    def save_settings(self, path=""):
        """ Saves the settings to path as json object.
        """
        if path == "":
            path = self.path
        with open(path, mode='w+') as set_file:
            json.dump(self.values, set_file, sort_keys=True, indent=4)

    def get_value(self, query):
        q = query.split(".")
        temp = self.values
        for key in q:
            try:
                temp = temp[key]
            except KeyError:
                return None
        return temp

    def get_value_str(self, query):
        """ Wrapper which will return empty string if key is not found.
        """
        # TODO: better to test if temp is string, and if not return ""
        temp = self.get_value(query)
        if temp is None:
            return ""
        return temp

    def load_template(self, template):
        self.template = template
        save = False
        for group in template:
            for item in group:
                if self.get_value(item["callback"]) is None:
                    self.set_value(item["callback"], item["default"])
                    save = True
        if save is True:
            self.save_settings()

    def set_value(self, query, value, save_file=True):
        q = query.split(".")
        last_key = q.pop()
        temp = self.values
        for key in q:
            if key not in temp:
                temp[key] = {}
            temp = temp[key]
        temp[last_key] = value
        if save_file is True:
            self.save_settings()
