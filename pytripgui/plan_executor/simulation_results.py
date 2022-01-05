import logging

from pytrip import volhist, DosCube, LETCube

logger = logging.getLogger(__name__)


class SimulationResults:
    def __init__(self, patient, plan, name):
        self.patient = patient
        self.plan = plan
        self.name = name
        self.volume_histograms = {}

        self._compute_target_dvh()
        self._compute_target_lvh()

    def get_doses(self):
        return self.plan.dosecubes

    def get_dose(self, dose_type):
        if dose_type not in DosCube.allowed_suffix:
            raise ValueError("Wrong dose type")

        for dose in self.plan.dosecubes:
            if dose.basename.endswith("." + dose_type):
                return dose
        return None

    def get_lets(self):
        return self.plan.letcubes

    def import_dos(self, dos_path):
        logger.debug("Open DosCube {:s}".format(dos_path))
        dos = DosCube()
        dos.read(dos_path)
        self.plan.dosecubes.append(dos)

    def import_let(self, let_path):
        logger.debug("Open LETCube {:s}".format(let_path))
        let = LETCube()
        let.read(let_path)
        self.plan.letcubes.append(let)

    def get_let(self, let_type):
        if let_type not in LETCube.allowed_suffix:
            raise ValueError("Wrong LET type")

        for let in self.plan.letcubes:
            if let.basename.endswith("." + let_type):
                return let
        return None

    def _compute_target_dvh(self):
        for dose in self.plan.dosecubes:
            dose_type = dose.basename.split(".")[-1]
            target_name = self.plan.voi_target.name
            dvh = {target_name: volhist.VolHist(dose, self.patient.vdx.get_voi_by_name(target_name))}
            self.volume_histograms["DVH " + dose_type] = dvh

    def _compute_target_lvh(self):
        for let in self.plan.letcubes:
            let_type = let.basename.split(".")[-1]
            target_name = self.plan.voi_target.name
            lvh = {target_name: volhist.VolHist(let, self.patient.vdx.get_voi_by_name(target_name))}
            self.volume_histograms["LVH " + let_type] = lvh

    def __str__(self):
        return "Sim: " + self.name
