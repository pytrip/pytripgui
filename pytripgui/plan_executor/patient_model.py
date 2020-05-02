import logging

import pytrip as pt

logger = logging.getLogger(__name__)


class PatientModel:
    def __init__(self):
        self.name = "Patient"
        self.ctx = None
        self.vdx = None

        self.plans = []

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
