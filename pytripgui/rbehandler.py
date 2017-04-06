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
import os
import sys

import pytrip.tripexecuter.rbehandler as rh

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


class RBEHandler(rh.RBEHandler):
    def __init__(self):
        pub.subscribe(self.on_rbefolder_changed, "datafiles.rbefolder")
        pub.sendMessage("settings.value.request", "datafiles.rbefolder")
        self.datafile = os.path.join(get_user_directory(), "rbe.dat")

    def on_rbefolder_changed(self, msg):
        self.rbe_folder = msg.data
