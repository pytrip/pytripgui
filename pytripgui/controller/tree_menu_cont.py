import logging
# from functools import partial

# from PyQt5 import QtCore
# from PyQt5 import QtGui
# from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu
# from PyQt5.QtWidgets import QDialog
# from PyQt5.QtWidgets import QTreeWidgetItem

import pytrip as pt
import pytrip.tripexecuter as pte

logger = logging.getLogger(__name__)


class TreeMenuController(object):
    """
    Here goes all the logic for the rightclick menus in TreeWidget
    """

    def __init__(self, model, view, ctrl):

        self.model = model
        self.view = view
        self.ctrl = ctrl
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
            popup_menu.addAction("New Plan", self.menu_newplan)  # TODO: may move somewhere else
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
            popup_menu.addAction("Add field", self.add_field)
            popup_menu.addSeparator()
            popup_menu.addAction("Execute plan", self.execute_plan)
            popup_menu.addAction("Edit", self.menu_open)
            popup_menu.addAction("Export", self.menu_open)
            popup_menu.addAction("Rename", self.menu_open)
            popup_menu.addSeparator()
            popup_menu.addAction("Delete", self.menu_open)

        if isinstance(obj, pte.Field):
            popup_menu.addAction("Edit", self.edit_field)
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

    def execute_plan(self):
        logger.debug("execute_plan".format())
        plan = self._node_obj

        import tempfile, os
        self.model.wdir = tempfile.gettempdir() + "/pytripgui/"

        try:
            os.mkdir(self.model.wdir)
        except OSError:
            pass

        logger.debug("Temporary dir:{}".format(self.model.wdir))

        plan.working_dir = self.model.wdir

        import pytrip.tripexecuter as pte

        current_field = plan.fields[0]
        plan.projectile = current_field.kernel.projectile.iupac
        plan.projectile_a = current_field.kernel.projectile.a
        plan.rifi = current_field.kernel.rifi_thickness
        plan.ddd_dir = current_field.kernel.ddd_path
        plan.spc_dir = current_field.kernel.spc_path
        plan.sis_path = current_field.kernel.sis_path
        plan.dedx_path = "$TRIP98/DATA/DEDX/20000830.dedx"

        te = pte.Execute(self.model.ctx, self.model.vdx)

        try:
            te.execute(plan)
        except RuntimeError:
            pass

    def add_field(self):
        logger.debug("add_field_new() {}".format(None))

        from pytripgui.controller.field_cont import FieldController
        new_field = FieldController(self.model).edit()
        new_field.basename = "Field_{}".format(new_field.number)    # TODO it not generate unique numbers
        self._node_obj.fields.append(new_field)
        self.ctrl.tree.update_tree()

    def edit_field(self):
        logger.debug("edit_field() {}".format(None))

        from pytripgui.controller.field_cont import FieldController
        FieldController(self.model).edit(self._node_obj)
        self.ctrl.tree.update_tree()

    def menu_open(self):
        logger.debug("menu_open() {}".format(None))

    def menu_newplan(self):
        logger.debug("menu_plan() {}".format(None))
        model = self.model

        from pytripgui.controller.plan_cont import PlanController

        PlanController.new_plan(model)
        self.ctrl.tree.update_tree()

    def menu_dvh(self):
        logger.debug("menu_dvh() {}".format(None))
        logger.debug("this was from VOI '{}'".format(self._node_obj.name))

        voi = self._node_obj
        ctrl = self.ctrl

        # calculate DVH for all DOS cubes available.
        for dos in self.model.dos:
            ctrl.dvh.add_dvh(dos, voi)

    def menu_lvh(self):
        logger.debug("menu_lvh() {}".format(None))
        logger.debug("this was from VOI '{}'".format(self._node_obj.name))

        voi = self._node_obj
        ctrl = self.ctrl

        # calculate DVH for all DOS cubes available.
        for let in self.model.let:
            ctrl.lvh.add_lvh(let, voi)
