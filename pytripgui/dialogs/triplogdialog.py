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
from wx.xrc import XRCCTRL, XRCID
import logging

logger = logging.getLogger(__name__)


class TripLogDialog(wx.Dialog):
    def __init__(self):
        pre = wx.PreDialog()
        self.PostCreate(pre)

    def Init(self, tripexecuter):
        self.tripexecuter = tripexecuter
        self.tripexecuter.add_log_listener(self)
        self.txt_log = XRCCTRL(self, "txt_log")
        # use some fixed width font to mimic a proper terminal
        font_log = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)
        self.txt_log.SetFont(font_log)
        wx.EVT_BUTTON(self, XRCID("btn_ok"), self.close)
        self.btn_ok = XRCCTRL(self, "btn_ok")
        self.btn_ok.Enable(False)
        self.check_close = XRCCTRL(self, "check_close")

    def close(self, evt):
        self.Close()

    def finish(self):
        self.btn_ok.Enable(True)
        if self.check_close.IsChecked():
            self.Close()

    def write(self, txt):
        logger.debug("{:s}\n".format(txt))
        self.txt_log.AppendText("{:s}\n".format(txt))
