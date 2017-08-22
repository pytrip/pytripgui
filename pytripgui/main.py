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
import argparse
import logging
import os
import sys
import traceback

import wx
import wx.lib.dialogs
from pytrip.error import InputError
from wx.xrc import XRCID, XmlResource

from pytripgui import util
from pytripgui.plugin import PluginManager
from pytripgui.util import get_resource_path
from pytripgui.view.mainframe import FileDropTarget

if getattr(sys, 'frozen', False):
    pass
else:
    try:
        from wx.lib.pubsub import Publisher as pub
    except:
        from wx.lib.pubsub import setuparg1  # noqa
        from wx.lib.pubsub import pub

logger = logging.getLogger(__name__)


class Controller(object):
    def __init__(self, app):
        pass
        # controller holds refs to models, app and views
        # self.model = Model('Goku', 9001)

        self.app = app  # <- wxApp

        # self.view = View(None)  # <- wxFrame

        # finally,show the view
        # self.view.Show()

        from pytripgui import __version__ as pytripgui_version
        app.SetAppName("pytrip")
        # Load the XRC file for our gui resources
        self.app.res = XmlResource(util.get_resource_path('main.xrc'))
        pytripFrame = self.app.res.LoadFrame(None, 'MainFrame')
        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        pytripFrame.SetFont(font)
        pytripFrame.Init(self.app.res)
        pytripFrame.SetTitle("PyTRiPGUI v.{:s}".format(pytripgui_version))
        dt1 = FileDropTarget(pytripFrame)
        pytripFrame.SetDropTarget(dt1)
        self.app.SetTopWindow(pytripFrame)
        pytripFrame.Centre()
        pytripFrame.Show()


class pytripgui(wx.App):
    def OnInit(self):
        from pytripgui import __version__ as pytripgui_version

        wx.GetApp().SetAppName("pytrip")
        # Load the XRC file for our gui resources
        self.res = XmlResource(util.get_resource_path('main.xrc'))
        pytripFrame = self.res.LoadFrame(None, 'MainFrame')
        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        pytripFrame.SetFont(font)
        pytripFrame.Init(self.res)
        pytripFrame.SetTitle("PyTRiPGUI v.{:s}".format(pytripgui_version))
        dt1 = FileDropTarget(pytripFrame)
        pytripFrame.SetDropTarget(dt1)
        self.SetTopWindow(pytripFrame)
        pytripFrame.Centre()
        pytripFrame.Show()
        return 1


def handleInputException(exc_type, exc_value, exc_traceback):
    if exc_type is InputError:
        dlg = wx.MessageDialog(None, str(exc_value), 'Input Error', wx.OK | wx.ICON_ERROR)
    else:
        err_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        dlg = wx.MessageDialog(None, err_msg, 'Termination dialog', wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()

sys.excepthook = handleInputException

def start(args=sys.argv[1:]):
    from pytripgui import __version__ as _ptgv
    from pytrip import __version__ as _ptv
    _vers = "PyTRiP98GUI {} using PyTRiP98 {}".format(_ptgv, _ptv)
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", action='count', help="increase output verbosity", default=0)
    parser.add_argument('-V', '--version', action='version', version=(_vers))
    parsed_args = parser.parse_args(args)

    if parsed_args.verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    elif parsed_args.verbosity > 1:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    # app = pytripgui(0)
    app = wx.App(False)

    # pass the app to the controller
    controller = Controller(app)

    # start the app running
    app.MainLoop()


if __name__ == '__main__':
    sys.exit(start(sys.argv[1:]))
