import pytrip as pt

from pytrip.tripexecuter import Plan
from pytripgui.plan_vc import PlanQtView
from pytripgui.plan_vc import PlanController

from pytrip.tripexecuter import Field
from pytripgui.field_vc import FieldQtView
from pytripgui.field_vc import FieldController

from pytripgui.model.plot_model import PlotModel

import logging
logger = logging.getLogger(__name__)


class PatientTreeModel:
    def __init__(self):
        self.patient_tree = None
        self.ctx_tree = None
        self.vdx_tree = None
        self.plans_tree = None
        self.simulations_tree = None


class Patient:
    def __init__(self, global_kernels):
        self.name = "Patient"
        self.ctx = None
        self.vdx = None

        self.plans = []
        self.simulation = []
        self.global_kernels = global_kernels

        self.tree_model = PatientTreeModel()

    def open_ctx(self, path):
        ctx = pt.CtxCube()
        ctx.read(path)
        self.ctx = ctx
        self.name = ctx.basename

    def open_vdx(self, path):
        vdx = pt.VdxCube(self.ctx)
        vdx.read(path)
        self.vdx = vdx
        if self.name != vdx.basename:
            logger.error("CTX | VDX patient name not match")

    def add_new_plan(self):
        logger.debug("add_new_plan() {}".format(None))

        plan = Plan()
        plan.basename = self.ctx.basename
        view = PlanQtView()
        default_kernel = self.global_kernels[0]  # TODO select default kernel
        plan.kernel = default_kernel

        controller = PlanController(plan, view, self.global_kernels, self.vdx.vois)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            self.plans.append(plan)

    def edit_plan(self, plan):
        logger.debug("edit_plan() {}".format(None))

        view = PlanQtView()

        controller = PlanController(plan, view, self.global_kernels, self.vdx.vois)
        controller.set_view_from_model()
        view.show()

    def add_new_field(self, field):
        logger.debug("add_field_new() {}".format(None))

        new_field = Field()
        view = FieldQtView()
        default_kernel = self.global_kernels[0]  # TODO select default kernel
        new_field.kernel = default_kernel

        controller = FieldController(new_field, view, self.global_kernels)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            new_field.basename = "Field_{}".format(new_field.number)  # TODO it not generate unique numbers
            field.fields.append(new_field)

    def edit_field(self, field):
        logger.debug("edit_field() {}".format(None))

        view = FieldQtView()

        controller = FieldController(field, view, self.global_kernels)
        controller.set_view_from_model()
        view.show()
