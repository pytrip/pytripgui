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
import sys
import traceback

import wx
import wx.lib.dialogs
from pytrip.error import InputError
from wx.xrc import XRCCTRL, XRCID, XmlResource

from pytripgui.model import util
from pytripgui.model.settings import Settings
from pytripgui.model.tripdata import TRiPData
from pytripgui.view.mainframe import FileDropTarget, MainFrame

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
        # controller holds refs to models, app and views
        self.model = TRiPData()

        from pytripgui import __version__ as pytripgui_version

        self.app = app  # <- wxApp
        self.app.res = XmlResource(util.get_resource_path('main.xrc'))

        self.view = self.app.res.LoadFrame(None, 'MainFrame')  # <- wxFrame

        self.view.SetFont(wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT))
        self.view.Init(self.app.res)
        self.view.SetTitle("PyTRiPGUI v.{:s}".format(pytripgui_version))
        self.view.SetDropTarget(FileDropTarget(self.view))

        self.app.SetTopWindow(self.view)

        self.view.Centre()

        self.menu_open_voxelplan_bin()

        # finally,show the view
        self.view.Show()

    def menu_open_voxelplan_bin(self):
        wx.EVT_MENU(self.view, XRCID("menuitem_voxelplan"), self.view.open_load_voxelplan_dialog)
        pub.subscribe(self.on_voxelplan_file_selected, "voxelplan.load.dialog.new")

    def on_voxelplan_file_selected(self, msg):
        st = Settings()  # save last used DICOM path to settings file.
        st.save("general.import.voxelplan_path", msg.data)
        self.model.open_ctx_vdx(msg.data)

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

    app = wx.App(False)

    # pass the app to the controller
    controller = Controller(app)

    # start the app running
    app.MainLoop()


if __name__ == '__main__':
    sys.exit(start(sys.argv[1:]))
