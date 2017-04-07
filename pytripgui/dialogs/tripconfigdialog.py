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
        
    def Init(self, plan):
        """ Setup the machinery for tripconfigdialog
        :params plan: tripplan
        """
        self.plan = plan

        # list of all parameters which are to be stored, listed by topic : attribute name of widget object set in .xrc file
        self.params = {"trip98.s.wdir": "txt_working_dir",
                       "trip98.s.username": "txt_username",
                       "trip98.s.password": "txt_password",
                       "trip98.s.server": "txt_server",
                       "trip98.b.remote": "drop_location"}
        
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

        # load all parameter values into a dict

        self.drop_location = XRCCTRL(self, "drop_location")

        for _key in self.params:
            _attr = self.params[_key]  # string holding the attribute names
            if "trip98." in _key:
                setattr(self, _attr, XRCCTRL(self, _attr))  # lookup attributes names and populate with classes
                pub.subscribe(self._save_parameter, _key)

        # load and set all attributes from preference file
        for _key in self.params:
            pub.sendMessage('settings.value.request', _key)

        wx.EVT_BUTTON(self, XRCID('btn_browse_wdir'), self.on_browse_working_dir)

    def _save_parameter(self, msg):
        logger.debug("RECEIVED VALUE {:s}".format(msg.data))
        
        _topic = ".".join(msg.topic)
        _val = msg.data
        
        if "trip98.s." in _topic:
            _attr = self.params[_topic]
            if _val is None:
                _val = ""                
            XRCCTRL(self, _attr).SetValue(_val)

        # however attributes need special attention
        

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
        logger.debug("save preferences...")
        _save_dict = {}
        
        # make a new dict of parameters to be saved
        for _key in self.params:
            _attr = self.params[_key]  # string holding the attribute names
            _val = XRCCTRL(self, _attr).GetValue()  # look up values in the various fields

            _save_dict[_key] = _val
            logger.debug("{:s} : {:s}".format(_key,_val))
            
            
        pub.sendMessage('settings.value.updated', _save_dict)
        
