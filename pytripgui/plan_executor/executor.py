import os
import copy
import logging

from pytripgui.plan_executor.trip_config import Trip98ConfigModel
import pytrip.tripexecuter as pte
from pytripgui.plan_executor.simulation_results import SimulationResults

logger = logging.getLogger(__name__)


class PlanExecutor:
    def __init__(self):
        self.trip_config = Trip98ConfigModel()

    def check_config(self):
        # TODO replace with function that actually runs trip, and collect returned errors
        if self.trip_config.wdir_path == "":
            return -1
        if self.trip_config.trip_path == "":
            return -1
        return 0

    def execute(self, patient, plan):
        plan = copy.deepcopy(plan)

        plan.working_dir = self.trip_config.wdir_path
        plan.dedx_path = self.trip_config.dedx_path
        plan.hlut_path = self.trip_config.hlut_path

        te = pte.Execute(patient.ctx, patient.vdx)
        te.trip_bin_path = os.path.join(self.trip_config.trip_path, 'TRiP98')

        try:
            te.execute(plan)
        except RuntimeError:
            logger.error("TRiP98 executer: Runtime error")
            exit(-1)

        results = SimulationResults(patient)
        results.import_results(plan)

        return results
