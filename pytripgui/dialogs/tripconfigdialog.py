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
import wx
import sys
import logging

from wx.xrc import XmlResource, XRCCTRL, XRCID

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


class TripConfigDialog(wx.Dialog):
    def __init__(self):
        pre = wx.PreDialog()
        self.PostCreate(pre)

    def Init(self, obj):
        """ Setup the machinery for tripconfigdialog
        """
        # lookup widgets and attach them to this class
        self.btn_save = XRCCTRL(self, "btn_save")
        self.btn_close = XRCCTRL(self, "btn_close")

        # here attach all the callbacks
        wx.EVT_BUTTON(self, XRCID("btn_close"), self.close)

    def close(self, evt):
        """ Close the dialog.
        """
        self.Close()

    def foobar(self, evt):
        """ Just testing a callback
        """
        print("Hey ho")
