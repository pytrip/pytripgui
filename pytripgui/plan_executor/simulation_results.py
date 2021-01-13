import os
import logging

import pytrip as pt
from pytrip import volhist

logger = logging.getLogger(__name__)


class SimulationResults:
    def __init__(self, patient, plan):
        self.patient = patient
        self.name = ""
        self.plan = None
        self.dose = None
        self.let = None
        self.volume_histograms = {}

        self._import_results(plan)

    def _import_results(self, plan):
        self.name = plan.basename
        self.plan = plan
        if plan.want_phys_dose:
            dos_path = os.path.join(plan.working_dir, plan.basename + '.phys.dos')
            self._import_dos(dos_path)
            self._compute_target_dvh()

        if plan.want_dlet:
            let_path = os.path.join(plan.working_dir, plan.basename + '.dosemlet.dos')
            self._import_let(let_path)
            self._compute_target_lvh()

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

    def _compute_target_dvh(self):
        if self.dose:
            dvh = {}
            target_name = self.plan.voi_target.name
            dvh[target_name] = volhist.VolHist(self.dose, self.patient.vdx.get_voi_by_name(target_name))
            self.volume_histograms['DVH'] = dvh

    def _compute_target_lvh(self):
        if self.let:
            lvh = {}
            target_name = self.plan.voi_target.name
            lvh[target_name] = volhist.VolHist(self.let, self.patient.vdx.get_voi_by_name(target_name))
            self.volume_histograms['LVH'] = lvh

    def __str__(self):
        return "Sim: " + self.name
