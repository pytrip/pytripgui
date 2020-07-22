import os
import logging

import pytrip as pt

logger = logging.getLogger(__name__)


class SimulationResults:
    def __init__(self, patient):
        self.patient = patient
        self.name = ""
        self.plan = None
        self.dose = None
        self.let = None
        self.dvh = None
        self.lvh = None

    def import_results(self, plan):
        self.name = plan.basename
        if plan.want_phys_dose:
            dos_path = os.path.join(plan.working_dir, plan.basename + '.phys.dos')
            self._import_dos(dos_path)

        if plan.want_dlet:
            let_path = os.path.join(plan.working_dir, plan.basename + '.dosemlet.dos')
            self._import_let(let_path)

    def _import_dos(self, dos_path):
        logger.debug("Open DosCube {:s}".format(dos_path))
        dos = pt.DosCube()
        dos.read(dos_path)
        self.dose = dos

    def _import_let(self, let_path):
        logger.debug("Open LETCube {:s}".format(let_path))
        let = pt.LETCube()
        let.read(let_path)
        self.let = let

    def __str__(self):
        return "Sim: " + self.name
