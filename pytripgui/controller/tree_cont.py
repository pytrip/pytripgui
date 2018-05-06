import logging
# from functools import partial

# from PyQt5 import QtCore
# from PyQt5 import QtGui
# from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QTreeWidgetItem

import pytrip as pt
import pytrip.tripexecuter as pte

from pytripgui.controller.tree_menu_cont import TreeMenuController

logger = logging.getLogger(__name__)


class TreeController(object):
    """
    Idea is that the tree is entirely controlled by modifying the main_model.
    After modification, update_tree() is called, which will populate accordingly.
    """

    def __init__(self, model, view, plot_ctrl):
        """
        :param MyModel model:
        :param view:
        """
        self.model = model
        self.view = view
        self.pctrl = plot_ctrl  # this is only needed to trigger canvas update, if tree change.
        tw = view.treeWidget

        # QTreeWidgetItem placeholders
        self.tctx = None
        self.tvdx = None
        self.vois = []
        self.tplans = []
        self.tdos = []
        self.tlet = []

        # setup the submenus:
        self.tmc = TreeMenuController(model, view)  # self, else it goes out of scope?

        tw.itemClicked.connect(self.on_checked_changed)

    def on_checked_changed(self, pos):
        """
        If checkbox is changed in the TreeWidget, then then corresponding object is removed
        or added to the plot_model.
        """
        logger.debug("on_checked_changed() {}".format(pos))

        pm = self.model.plot
        obj = pos.data(0, Qt.UserRole)
        # state = pos.data(0, Qt.CheckStateRole)
        # tw = self.view.tw

        if pos.checkState(0) == Qt.Unchecked:
            if isinstance(obj, pt.CtxCube):
                logger.debug("set pm.ctx = None")
                pm.ctx = None

            if isinstance(obj, pt.Voi):
                logger.debug("remove Voi {}".format(obj.name))
                if obj in pm.vois:
                    pm.vois.remove(obj)
                else:
                    logger.warning("Tried to remove Voi {} which is not in pm.vois.")

            if isinstance(obj, pte.Plan):
                logger.debug("remove Plan {}".format(obj.name))
                if obj in pm.plans:
                    pm.plans.remove(obj)
                else:
                    logger.warning("Tried to remove Plan {} which is not in pm.plans.")

            # TODO: Field

            if isinstance(obj, pt.DosCube):
                logger.debug("set pm.dos = None")
                pm.dos = None

            if isinstance(obj, pt.LETCube):
                logger.debug("set pm.let = None")
                pm.let = None

        else:  # select something and add it to model.plot
            logger.debug("{} isChecked(True)".format(pos))
            if isinstance(obj, pt.CtxCube):
                pm.ctx = obj
            if isinstance(obj, pt.Voi):
                pm.vois.append(obj)
            if isinstance(obj, pt.DosCube):
                pm.dos = obj
            if isinstance(obj, pt.LETCube):
                pm.let = obj

        # trigger update plot after model was changed.
        self.pctrl.update_viewcanvas()

    def update_tree(self):
        """
        Syncs the tree with the main_model, adding and removing items accordingly.
        """
        model = self.model
        # view = self.view
        tw = self.view.treeWidget

        # CTX data
        if model.ctx and not self._in_tree(model.ctx):
            # Add CTX to tree widget.
            tw.setHeaderLabels(["'{}'".format(model.ctx.basename)])  # TODO:patient name

            self.tctx = QTreeWidgetItem([model.ctx.basename])
            self.tctx.setData(0, Qt.UserRole, model.ctx)
            tw.addTopLevelItem(self.tctx)
            self.tctx.setCheckState(0, Qt.Checked)

        # VDX data
        if model.vdx and not self._in_tree(model.vdx):
            self.tvdx = QTreeWidgetItem(["ROIs: " + model.vdx.basename])
            self.tvdx.setData(0, Qt.UserRole, model.vdx)
            tw.addTopLevelItem(self.tvdx)
            self.tvdx.setExpanded(True)

        # VOIS
        if model.vdx:
            vois = model.vdx.vois

            for i, voi in enumerate(vois):
                # child = QTreeWidgetItem(parent)
                self.tvdx.addChild(QTreeWidgetItem([voi.name]))
                child = self.tvdx.child(i)
                child.setData(0, Qt.UserRole, voi)
                child.setCheckState(0, Qt.Checked)

        if model.plans and not self._in_tree(model.plans):
            self.plans.append(QTreeWidgetItem(["Plan: {}".format(model.plan.basename)]))
            self.tdoss[-1].setData(0, Qt.UserRole, model.plan)
            tw.addTopLevelItem(self.tdoss[-1])
            self.tplans.setExpanded(True)

        if model.dos and not self._in_tree(model.dos):
            self.tdoss.append(QTreeWidgetItem(["DOS: {}".format(model.dos.basename)]))
            self.tdoss[-1].setData(0, Qt.UserRole, model.dos)
            tw.addTopLevelItem(self.tdoss[-1])
            self.tdos.setExpanded(True)

        if model.let and not self._in_tree(model.let):
            self.tlets.append(QTreeWidgetItem(["LET: {}".format(model.let.basename)]))
            self.tlets[-1].setData(0, Qt.UserRole, model.let)
            tw.addTopLevelItem(self.tlet)
            self.tlet.setExpanded(True)

        # TODO: check for items to be removed.

    def _in_tree(self, obj):
        """
        Crawls the entire treewidget, and search for the object.
        Returns corresponding QTreeWidgetItem, if found, else None.
        """
        tw = self.view.treeWidget

        root = tw.invisibleRootItem()
        count = root.childCount()

        for i in range(count):
            child = root.child(i)
            _obj = child.data(0, Qt.UserRole)
            if obj == _obj:
                return child

            count2 = child.childCount()
            for j in range(count2):
                child2 = child.child(j)
                _obj = child2.data(0, Qt.UserRole)
                if obj == _obj:
                    return child2

        return None
