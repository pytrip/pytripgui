import logging
# from functools import partial

# from PyQt5 import QtCore
# from PyQt5 import QtGui
# from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu
# from PyQt5.QtWidgets import QTreeWidgetItem

import pytrip as pt
import pytrip.tripexecuter as pte

logger = logging.getLogger(__name__)


class TreeMenuController(object):
    """
    Here goes all the logic for the rightclick menus in TreeWidget
    """

    def __init__(self, model, view):

        self.model = model
        self.view = view
        tw = view.treeWidget

        tw.setContextMenuPolicy(Qt.CustomContextMenu)
        tw.customContextMenuRequested.connect(self.on_context_menu)

    def on_context_menu(self, pos):
        """
        Callback if rightclick on treeWidget.
        """

        logger.debug("on_context_menu() {}".format(pos))

        tw = self.view.treeWidget

        getSelected = tw.selectedItems()
        if getSelected:
            baseNode = getSelected[0]  # QTreeWidgetItem
            obj = baseNode.data(0, Qt.UserRole)
        else:
            obj = pt.CtxCube  # if nothing selected, put up Ctx menu

        popup_menu = self.create_popup_menu(obj)
        node = tw.mapToGlobal(pos)

        self._node_menu = node
        self._node_obj = obj

        action = popup_menu.exec_(node)
        logger.debug("action {}".format(action))

    def create_popup_menu(self, obj):
        """
        obj is the data object for the QTreeWidgetItem (CtxCube VdxCube ... etc)
        """
        tw = self.view.treeWidget
        popup_menu = QMenu(tw)

        if isinstance(obj, pt.CtxCube):
            popup_menu.addAction("Open DICOM", self.menu_open)
            popup_menu.addAction("Open .ctx", self.menu_open)
            popup_menu.addAction("Rename", self.menu_open)
            popup_menu.addAction("Export .ctx", self.menu_open)
            popup_menu.addSeparator()
            popup_menu.addAction("Delete", self.menu_open)

        if isinstance(obj, pt.VdxCube):
            popup_menu.addAction("New", self.menu_open)
            popup_menu.addAction("Open .vdx", self.menu_open)
            popup_menu.addAction("Rename", self.menu_open)
            popup_menu.addAction("Export .vdx", self.menu_open)
            popup_menu.addSeparator()
            popup_menu.addAction("Delete all", self.menu_open)

        if isinstance(obj, pt.Voi):
            popup_menu.addAction("Color", self.menu_open)
            popup_menu.addAction("Rename", self.menu_open)
            popup_menu.addAction("Calculate DVH", self.menu_dvh)
            popup_menu.addAction("Calculate LVH", self.menu_lvh)
            popup_menu.addSeparator()
            popup_menu.addAction("Delete", self.menu_open)

        if isinstance(obj, pte.Plan):
            popup_menu.addAction("Edit", self.menu_open)
            popup_menu.addAction("Export", self.menu_open)
            popup_menu.addAction("Rename", self.menu_open)
            popup_menu.addSeparator()
            popup_menu.addAction("Delete", self.menu_open)

        if isinstance(obj, pte.Field):
            popup_menu.addAction("Edit", self.menu_open)
            popup_menu.addAction("Rename", self.menu_open)
            popup_menu.addSeparator()
            popup_menu.addAction("Delete", self.menu_open)

        if isinstance(obj, pt.DosCube):
            popup_menu.addAction("Export", self.menu_open)
            popup_menu.addAction("Rename", self.menu_open)
            popup_menu.addSeparator()
            popup_menu.addAction("Delete", self.menu_open)

        if isinstance(obj, pt.LETCube):
            popup_menu.addAction("Export", self.menu_open)
            popup_menu.addAction("Rename", self.menu_open)
            popup_menu.addSeparator()
            popup_menu.addAction("Delete", self.menu_open)

        return popup_menu

    def menu_open(self):
        logger.debug("menu_open() {}".format(None))

    def menu_dvh(self):
        logger.debug("menu_dvh() {}".format(None))
        logger.debug("this was from VOI '{}'".format(self._node_obj.name))

        voi = self.node_obj

        # calculate DVH for all DOS cubes available.
        for dos in self.model.dos:
            tctrl.dvh.add_dvh(dos, voi)

    def menu_lvh(self):
        logger.debug("menu_lvh() {}".format(None))
