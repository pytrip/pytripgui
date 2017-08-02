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
from wx.xrc import XmlResource, XRCCTRL, XRCID


class DoseDialog(wx.Dialog):
    def __init__(self):
        pre = wx.PreDialog()
        self.PostCreate(pre)

    def Init(self, dos):
        """
        :params pytrip.DosCube() dos:
        """
        self.dos = dos
        self.txt_targetdose = XRCCTRL(self, "txt_targetdose")
        self.txt_targetdose.SetValue("{:.1f}".format(self.dos.target_dose))

        self.btn_ok = XRCCTRL(self, 'btn_ok')
        wx.EVT_BUTTON(self, XRCID('btn_ok'), self.save_and_close)

        self.btn_cancel = XRCCTRL(self, 'btn_close')
        wx.EVT_BUTTON(self, XRCID('btn_close'), self.close)

    def save_and_close(self, evt):
        self.dos.target_dose = float(self.txt_targetdose.GetValue())
        self.Close()

    def close(self, evt):
        self.Close()
