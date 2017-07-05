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
"""
All plan data are stored here.
"""
import sys
import threading
import logging

import pytrip as pt

from pytripgui.closeobj import CloseObj

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


class TRiPData:
    """
    TODO: find better name for this class (PyTripGuiData ?)

    Structure:

    Each Patient will have its own TRiPData object
    Each Data object holds
    - a list of plans
    - a list of VOIs for this particular patient


    Plans will be extended to hold VOIs as well.
    So each plan will also hold:
    - a list of VOIs (from a given VdxCube)
    - a list of DosCubes (don't call them "dose", this is ambigous)
    - a list of LETCubes

    """

    def __init__(self):
        """
        """
        self.patient_name = ""
        self.active_plan = None
        self.plans = []
        self.vois = []

    def open_ctx_vdx(self, path, threaded=True):
        """
        Top method for opening a voxelplan ctx and vdx file.
        
        :params str path: path pointing to common header file.
        :params bool threaded: enable threaded loading, GUI is not blocked while loading
        """
        self.patient_path = path
        close = CloseObj()
        if threaded:
            self.t = threading.Thread(target=self._open_ctx_vdx_thread, args=(path, close))
            self.t.start()
            pub.sendMessage("gui.wait.open", close)
        else:
            self._open_ctx_vdx_thread(path)

    def _open_ctx_vdx_thread(self, path, close=None):
        """
        Attempts to load a .ctx and .vdx, and load onto self.
        :params str path: path pointing to common header file.
        """
        # file is not compatible with required extension

        logger.debug("open path {:s}".format(path))
        
        c = pt.CtxCube()
        c.read(path)

        v = pt.VdxCube()
        v.read(c, path)

        for voi in v.vois:
            self.vois.append[voi]
            
        self.patient_name = c.patient_name

        if close is not None:
            wx.CallAfter(close.close)

