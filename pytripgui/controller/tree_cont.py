import logging
# from functools import partial

# from PyQt5 import QtCore
# from PyQt5 import QtGui
# from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QTreeWidgetItem
from pytripgui.controller.tree_cont_aux import DosCollection
from pytripgui.controller.tree_cont_aux import LetCollection
from pytripgui.controller.tree_cont_aux import PlanCollection
# from tree_cont_aux import FieldCollection

import pytrip as pt
import pytrip.tripexecuter as pte

from pytripgui.controller.tree_menu_cont import TreeMenuController

logger = logging.getLogger(__name__)


class TreeController(object):
    """
    Idea is that the tree is entirely controlled by modifying the main_model.
    After modification, update_tree() is called, which will populate accordingly.
    """

    def __init__(self, model, view, ctrl):
        """
        :param MyModel model:
        :param view:
        """
        self.model = model
        self.view = view
        self.pctrl = ctrl.plot  # this is only needed to trigger canvas update, if tree change.
        tw = view.treeWidget

        # QTreeWidgetItem placeholders, only the top level nodes.
        self.tctx = None
        self.tvdx = None
        self.tplans = None
        self.tdos = None
        self.tlet = None

        # These "articial" objects are made since they do not exist in pytrip.model
        self._doscol = DosCollection()
        self._letcol = LetCollection()
        self._plancol = PlanCollection()

        # setup the submenus:
        self.tmc = TreeMenuController(model, view, ctrl)  # self, else it goes out of scope?

        # connect checkbox change state to callback
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
                if obj not in pm.vois:
                    pm.vois.append(obj)
            if isinstance(obj, pt.DosCube):
                pm.dos = obj
            if isinstance(obj, pt.LETCube):
                pm.let = obj

        # trigger update plot after model was changed.
        self.pctrl.update_viewcanvas()

        for i, item in enumerate(pm.vois):
            logger.debug("pm.vois {}:{}".format(i, item.name))

    def update_tree(self):
        """
        Syncs the tree with the main_model, adding and removing items accordingly.
        """
        logger.debug("update_tree()")
        self._model_sync_add_items()
        self._model_sync_remove_items()

    def _model_sync_add_items(self):
        """
        Syncs the tree with the main_model, adding and removing items accordingly.

        TODO: this can probably be programmed more elegantly.
        """
        self._add_ctx()
        self._add_vdxvoi()
        self._add_plans()
        self._add_fields()
        self._add_dos()
        self._add_let()

    def _add_ctx(self):
        """
        """
        model = self.model
        tw = self.view.treeWidget

        # CTX data
        if model.ctx and not self._in_tree(model.ctx):
            # Add CTX to tree widget.
            tw.setHeaderLabels(["'{}'".format(model.ctx.basename)])  # TODO:patient name

            self.tctx = QTreeWidgetItem([model.ctx.basename])
            self.tctx.setData(0, Qt.UserRole, model.ctx)
            tw.addTopLevelItem(self.tctx)
            self.tctx.setCheckState(0, Qt.Checked)

    def _add_vdxvoi(self):
        """
        """
        model = self.model
        tw = self.view.treeWidget

        # VDX data
        if model.vdx and not self._in_tree(model.vdx):
            self.tvdx = QTreeWidgetItem(["ROIs: " + model.vdx.basename])
            self.tvdx.setData(0, Qt.UserRole, model.vdx)
            tw.addTopLevelItem(self.tvdx)
            self.tvdx.setExpanded(True)

        # VOIs
        if model.vdx and model.vdx.vois:
            vois = model.vdx.vois
            for i, voi in enumerate(vois):
                # Add only Vois which are not in the tree.
                if not self._in_tree(voi):
                    self.tvdx.addChild(QTreeWidgetItem([voi.name]))
                    child = self.tvdx.child(i)
                    child.setData(0, Qt.UserRole, voi)
                    child.setCheckState(0, Qt.Checked)

    def _add_plans(self):
        """
        This will sync the plan tree with whatever is found in model.plans.
        Missing plans in the tree will be added.
        """
        logger.debug("_add_plans()")

        model = self.model
        tw = self.view.treeWidget

        # there may be plans in the model, and then they should be shown in the tree.
        # the plans in the tree are self.tplans

        # Plans node:
        # check if there are any plans, and tplans are missing
        if model.plans and not self.tplans:
            # we need to create the Plans node then in the treeview
            self.tplans = QTreeWidgetItem(["Plans:"])
            self.tplans.setData(0, Qt.UserRole, self._plancol)
            tw.addTopLevelItem(self.tplans)
            self.tplans.setExpanded(True)

        # Plans has one child for each plan.
        if model.plans:
            for i, plan in enumerate(model.plans):
                # Add only plans, which are not already in the tree
                if not self._in_tree(plan):
                    self.tplans.addChild(QTreeWidgetItem([plan.basename]))
                    child = self.tplans.child(i)
                    child.setData(0, Qt.UserRole, plan)
                    child.setCheckState(0, Qt.Checked)

    def _add_fields(self):
        """
        This method fills root_tree->plans with fields in GUI
        """
        tplans = self.tplans
        if tplans is not None:
            for i in range(tplans.childCount()):
                # make variable for current treePlan(QT)
                tplan = tplans.child(i)
                # get plan(pytrip) from treePlan(QT)
                plan = tplan.data(0, Qt.UserRole)

                # if fields in processed plan aren't empty, add them all to the tree
                if plan is not None and len(plan.fields) > 0:
                    for field in plan.fields:
                        if not self._is_in_this_tree(field, tplan):
                            child = QTreeWidgetItem([field.basename])
                            child.setData(0, Qt.UserRole, field)
                            child.setCheckState(0, Qt.Checked)
                            tplan.addChild(child)

    @staticmethod
    def _is_in_this_tree(field, tree):
        for i in range(tree.childCount()):
            if field == tree.child(i).data(0, Qt.UserRole):
                return True
        return False

    def _add_dos(self):
        """
        """
        model = self.model
        tw = self.view.treeWidget

        # Add the top level DOS node:
        if model.dos_container.dos_list and not self.tdos:
            self.tdos = QTreeWidgetItem(["Dose Cubes"])
            self.tdos.setData(0, Qt.UserRole, self._doscol)
            tw.addTopLevelItem(self.tdos)
            self.tdos.setExpanded(True)

        # Each DosCube will be treated as a child to the top level DOS node.
        if model.dos_container.dos_list:
            for i, dos in enumerate(model.dos_container.dos_list):
                if not self._in_tree(dos):
                    self.tdos.addChild(QTreeWidgetItem([dos.basename]))
                    child = self.tdos.child(i)
                    child.setData(0, Qt.UserRole, dos)
                    child.setCheckState(0, Qt.Checked)

    def _add_let(self):
        """
        """
        model = self.model
        tw = self.view.treeWidget

        # Add the top level LET node:
        if model.let_container.let_list and not self.tlet:
            self.tlet = QTreeWidgetItem(["LET Cubes"])
            self.tlet.setData(0, Qt.UserRole, self._letcol)
            tw.addTopLevelItem(self.tlet)
            self.tlet.setExpanded(True)

        # Each LETCube will be treated as a child to the top level DOS node.
        if model.let_container.let_list:
            for i, let in enumerate(model.let_container.let_list):
                if not self._in_tree(let):
                    self.tlet.addChild(QTreeWidgetItem([let.basename]))
                    child = self.tlet.child(i)
                    child.setData(0, Qt.UserRole, let)
                    child.setCheckState(0, Qt.Checked)

    def _model_sync_remove_items(self):
        """
        Sync TreeWidget with data model.
        If items are found in TreeWidget, which are not found in
        data model, the item will be removed from TreeWidget.
        """

        tw = self.view.treeWidget

        lo = self._flat_model()

        root = tw.invisibleRootItem()
        count = root.childCount()

        # Check if TreeWidget item data object is found in model.
        # if not, remove it from TreeWidget.
        for i in range(count):
            item = root.child(i)
            if item:
                _obj = item.data(0, Qt.UserRole)
                if _obj not in lo:
                    (item.parent() or root).removeChild(item)

                count2 = item.childCount()
                for j in range(count2):
                    item2 = item.child(j)
                    if item2:
                        _obj = item2.data(0, Qt.UserRole)
                        if _obj not in lo:
                            (item2.parent() or root).removeChild(item)

    def _flat_model(self):
        """ Produces a searchable and flat array of model data
        which should be displayed in the TreeWidget.
        This array will be used for syncing the treeWidget items with the model items.
        """
        model = self.model

        # Check for items to be removed.
        # First lets make a flat list of all pytrip objects in the model (called "lo"):
        lo = [model.ctx, model.vdx]
        if model.vdx:
            if model.vdx.vois:
                lo += model.vdx.vois  # extend the list with a list of voi objects
        if model.dos_container.dos_list:
            lo += model.dos_container.dos_list
        if model.let_container.let_list:
            lo += model.let_container.let_list
        if model.plans:
            lo += model.plans
            for plan in model.plans:
                if plan.fields:
                    lo += plan.fields
        # TODO: this part needs some rework.
        # The top level nodes: plans, dos and let
        # should not be removed, if they hold data. They do not have a class, tough
        # Therefore this little hack for now:
        if model.dos_container.dos_list:
            lo += [self._doscol]
        if model.let_container.let_list:
            lo += [self._letcol]
        if model.plans:
            lo += [self._plancol]

        return lo

    def _in_tree(self, obj):
        """
        Crawls the entire treewidget, and search for the object.
        Returns corresponding QTreeWidgetItem, if found, else None.

        :params PyTRiPobject obj: such as CtxCube, DosCube, VdxCube, Plan, ...etc
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
