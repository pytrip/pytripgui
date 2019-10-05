from pytripgui.model.config_model import Trip98ConfigModel
import pytrip.tripexecuter as pte
from pytripgui.plan_executor.simulation_results import SimulationResults

import os
import logging
logger = logging.getLogger(__name__)


class PlanExecutor:
    def __init__(self):
        self.trip_config = Trip98ConfigModel()

    def check_config(self):
        # TODO replace with
        if self.trip_config.wdir_path == "":
            return -1
        if self.trip_config.trip_path == "":
            return -1
        return 0

    def execute(self, patient, plan):
        plan.working_dir = self.trip_config.wdir_path

        current_field = plan.fields[0]
        plan.projectile = plan.kernel.projectile.iupac
        plan.projectile_a = plan.kernel.projectile.a
        plan.rifi = plan.kernel.rifi_thickness
        plan.ddd_dir = plan.kernel.ddd_path
        plan.spc_dir = plan.kernel.spc_path
        plan.sis_path = plan.kernel.sis_path

        plan.dedx_path = self.trip_config.dedx_path
        plan.hlut_path = self.trip_config.hlut_path

        te = pte.Execute(patient.ctx, patient.vdx)
        te.trip_bin_path = os.path.join(self.trip_config.trip_path, 'TRiP98')

        try:
            te.execute(plan)
        except RuntimeError:
            logger.error("TRiP98 executer: Runtime error")
            exit(-1)

        return SimulationResults(plan)
