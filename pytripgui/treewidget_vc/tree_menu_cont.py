import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu

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




    def add_field(self):
        logger.debug("add_field_new() {}".format(None))

        from pytrip.tripexecuter import Field
        from pytripgui.field_vc import FieldQtView
        from pytripgui.field_vc import FieldController

        selected_plan = self._node_obj
        new_field = Field()
        view = FieldQtView()
        global_kernels = self.model.kernels
        default_kernel = self.model.kernels[0]  # TODO select default kernel
        new_field.kernel = default_kernel

        controller = FieldController(new_field, view, global_kernels)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            new_field.basename = "Field_{}".format(new_field.number)    # TODO it not generate unique numbers
            selected_plan.fields.append(new_field)
            self.ctrl.tree.update_tree()

    def edit_field(self):
        logger.debug("edit_field() {}".format(None))

        from pytripgui.field_vc import FieldQtView
        from pytripgui.field_vc import FieldController

        field = self._node_obj
        view = FieldQtView()
        global_kernels = self.model.kernels

        controller = FieldController(field, view, global_kernels)
        controller.set_view_from_model()
        view.show()

    def edit_plan(self):
        logger.debug("edit_plan() {}".format(None))

        from pytripgui.plan_vc import PlanQtView
        from pytripgui.plan_vc import PlanController

        plan = self._node_obj
        view = PlanQtView()
        global_kernels = self.model.kernels

        controller = PlanController(plan, view, global_kernels, self.model.vdx.vois)
        controller.set_view_from_model()
        view.show()

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
