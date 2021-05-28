import copy
import logging

import pytrip.tripexecuter as pte
from pytripgui.plan_executor.simulation_results import SimulationResults
import sys

logger = logging.getLogger(__name__)


class PlanExecutor:
    def __init__(self, trip_config, listener=None):
        self.trip_config = trip_config
        self.listener = listener

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
        if self.trip_config.remote_execution:
            te.remote = True
            te.servername = self.trip_config.host_name
            te.username = self.trip_config.user_name
            te.password = self.trip_config.password
            print(self.trip_config.pkey_path)
            te.pkey_path = self.trip_config.pkey_path
            te.remote_base_dir = self.trip_config.wdir_remote_path + '/'

        te.trip_bin_path = self.trip_config.trip_path + '/' + 'TRiP98'

        if self.listener:
            te.add_log_listener(self.listener)

        try:
            te.execute(plan)
        except BaseException as e:
            self.listener.write(e.__str__())
            logger.error(e.__str__())
            sys.exit(-1)

        results = SimulationResults(patient, plan)

        return results
