import pytrip as pt

from pytrip.tripexecuter import Plan
from pytripgui.plan_vc import PlanQtView
from pytripgui.plan_vc import PlanController

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
        self.name = ""
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

        # selected_plan = self._node_obj
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
