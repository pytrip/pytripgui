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
import os
import sys
import threading
import logging
import wx

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
    Each TRiPData object holds:
    - a single CtxCube object
    - a single VdxCube object
    - a list of Plan objects

    Plans will be extended to hold VOIs as well.
    So each plan will also hold:
    - a list of VOIs (from a given VdxCube)
    - a list of DosCubes (don't call them "dose", this is ambigous)
    - a list of LETCubes

    """

    def __init__(self):
        """
        """
        self.patient_name = "(no patient loaded)"
        self.ctx = None
        self.vdx = None
        self.active_plan = None
        self.plans = []

    def open_ctx_vdx(self, path, threaded=True):
        """
        Top method for opening a voxelplan ctx and vdx file.

        :params str path: path pointing to common header file.
        :params bool threaded: enable threaded loading, GUI is not blocked while loading
        """
        self.patient_path = path

        ### Disable threaded during debugging
        #close = CloseObj()
        # if threaded:
        #    self.t = threading.Thread(target=self._open_ctx_vdx_thread, args=(path, close))
        #    self.t.start()
        #    logger.debug("send gui.wait.open(close)")
        #    pub.sendMessage("gui.wait.open", close)
        #else:
        self._open_ctx_vdx_thread(path)

    def _open_ctx_vdx_thread(self, path, close=None):
        """
        Attempts to load a .ctx and .vdx, and load onto self.

        :params str path: path pointing to common header file.
        """

        logger.debug("open path {:s}".format(path))

        # TODO: remove these once new file resolver is implemented in PyTRiP
        ctx_path = path.replace(".hed", ".ctx.gz")
        vdx_path = path.replace(".hed", ".vdx")

        logger.debug("Opening {:s}".format(ctx_path))
        if os.path.isfile(ctx_path):
            self.ctx = pt.CtxCube()
            self.ctx.read(ctx_path)
        else:
            logger.error("File not found '{:s}'".format(ctx_path))

        logger.debug("Opening {:s}".format(vdx_path))
        if os.path.isfile(vdx_path):
            self.vdx = pt.VdxCube(self.ctx)
            self.vdx.read(vdx_path)
            for voi in self.vdx.vois:
                voi.selected = False
        else:
            logger.error("File not found '{:s}'".format(vdx_path))

        if close is not None:
            wx.CallAfter(close.close)

        ### wx.CallAfter(self.patient_load)
        pub.sendMessage("patient.load", self)

    def open_dicom(self, path, threaded=True):
        """
        """
        dcm = pt.dicomhelper.read_dicom_dir(path)
        self.loaded_path = path

        ### disable threaded load during debugging
        #close = CloseObj()
        #if threaded:
        #    self.t = threading.Thread(target=self.load_from_dicom_thread, args=(dcm, close))
        #    self.t.start()
        #    pub.sendMessage("gui.wait.open", close)
        #else:
        self._open_dicom_thread(dcm)

    def _open_dicom_thread(self, dicom, close=None):
        if 'images' in dicom:
            self.ctx = pt.CtxCube()
            self.ctx.read_dicom(dicom)

        if 'rtss' in dicom:
            self.vdx = pt.VdxCube(self.ctx)
            self.vdx.read_dicom(dicom)
            for voi in self.vdx.vois:
                voi.selected = False

        if close is not None:
            wx.CallAfter(close.close)

        # wx.CallAfter(self.patient_load)
        pub.sendMessage("patient.load", self)
