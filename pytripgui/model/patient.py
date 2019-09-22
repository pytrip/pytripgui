import pytrip as pt

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
    def __init__(self):
        self.name = ""
        self.ctx = None
        self.vdx = None

        self.plans = None
        self.simulation = None

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
