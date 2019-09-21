import logging
logger = logging.getLogger(__name__)


class Patient:
    def __init__(self):
        self.ctx = None
        self.vdx = None

        self.plans = None
        self.simulation = None
