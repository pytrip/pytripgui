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

from pytripgui.settings import SettingsManager
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
sm = SettingsManager()

class TripConfigDialog(wx.Dialog):
    def __init__(self):
        pre = wx.PreDialog()
        self.PostCreate(pre)

    def Init(self, plan):
        """ Setup the machinery for tripconfigdialog
        :params plan: tripplan
        """
        self.plan = plan
        sm.load_settings()
        # lookup widgets and attach them to this class
        self.btn_save = XRCCTRL(self, "btn_save")
        self.btn_close = XRCCTRL(self, "btn_close")

        # here attach all the callbacks
        wx.EVT_BUTTON(self, XRCID("btn_close"), self.close)
        wx.EVT_BUTTON(self, XRCID("btn_save"), self.save)

        self.init_trip_panel()

    def close(self, evt):
        """ Close the dialog.
        """
        self.Close()

    def init_trip_panel(self):
        """ Initialize the TRiP98 Configuration Panel from saved preferences.
        """
        self.drop_location = XRCCTRL(self, "drop_location")

        if sm.get_value_str("trip98.remote") is True:
            self.drop_location.SetSelection(1)

        self.txt_working_dir = XRCCTRL(self, "txt_working_dir")
        self.txt_working_dir.SetValue(sm.get_value_str("trip98.wdir"))

        wx.EVT_BUTTON(self, XRCID('btn_browse_wdir'), self.on_browse_working_dir)

        self.txt_username = XRCCTRL(self, "txt_username")
        self.txt_username.SetValue(sm.get_value_str("trip98.username"))

        self.txt_password = XRCCTRL(self, "txt_password")
        self.txt_password.SetValue(sm.get_value_str("trip98.password"))

        self.txt_server = XRCCTRL(self, "txt_server")
        self.txt_server.SetValue(sm.get_value_str("trip98.server"))

    def on_browse_working_dir(self, evt):
        """ Select working directory for TRiP98 via file dialog
        """
        dlg = wx.DirDialog(
            self,
            defaultPath=self.txt_working_dir.GetValue(),
            message="Choose the TRiP98 working directory")

        if dlg.ShowModal() == wx.ID_OK:
            self.txt_working_dir.SetValue(dlg.GetPath())

        sm.set_value("trip98.wdir", dlg.GetPath())

    def save(self, evt):
        """ Saves the dialog settings
        TODO: could probably be omitted, moder GUIs has no Save button for prefs.
        """

        sm.set_value("trip98.wdir", self.txt_working_dir.GetValue())
        sm.set_value("trip98.username", self.txt_username.GetValue())
        sm.set_value("trip98.password", self.txt_password.GetValue())
        sm.set_value("trip98.server", self.txt_server.GetValue())
