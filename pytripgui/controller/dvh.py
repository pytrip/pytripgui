import logging

from pytrip.volhist import VolHist

logger = logging.getLogger(__name__)


class Dvh:
    """
    This class holds logic for plotting CTX stuff.
    """
    def __init__(self, model, view):
        """
        """
        self.model = model
        self.view = view
        self.fig = self.view.ui.dvh
        self.fig.xlabel = "Dose [%]"
        self.fig.ylabel = "Volume [%]"

    def add_dvh(self, dos, voi):
        """
        Calculates and plots a DVH for all dos in model based on voi.
        TODO: fix me later
        """
        pm = self.model.plot

        dvh = self._calc_dvh(dos, voi)
        pm.dvhs.append(dvh)
        if not dvh.x or not dvh.y:
            return
        self.update_plotdvh()

    def add_dvh_dos(self, dos, voi):
        """
        Calculates and plots a DVH based on dos and voi.
        """
        pm = self.model.plot

        dvh = self._calc_dvh(dos, voi)
        pm.dvhs.append(dvh)
        self.update_plotdvh()

    @staticmethod
    def _calc_dvh(dos, voi):
        """ Calculates a Dvh
        """
        # TODO, this could be run threaded when loading a DOS and VDX is present.

        logger.debug("Processing VOI '{:s}'...".format(voi.name))
        return VolHist(dos, voi)

    def update_plotdvh(self):
        """
        """
        # TODO: clear plot
        axes = self.fig.axes

        for dvh in self.model.plot.dvhs:
            axes.plot(dvh.x, dvh.y, label=dvh.name)
        axes.set_xlabel(dvh.xlabel)
        axes.set_ylabel(dvh.ylabel)

        self.fig.show()
