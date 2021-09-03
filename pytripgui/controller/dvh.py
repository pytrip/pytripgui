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
        self.update_plot_dvh()

    def add_dvh_dos(self, dos, voi):
        """
        Calculates and plots a DVH based on dos and voi.
        """
        pm = self.model.plot

        dvh = self._calc_dvh(dos, voi)
        pm.dvhs.append(dvh)
        self.update_plot_dvh()

    @staticmethod
    def _calc_dvh(dos, voi):
        """ Calculates a Dvh
        """
        # TODO, this could be run threaded when loading a DOS and VDX is present.

        logger.debug("Processing VOI '{:s}'...".format(voi.name))
        return VolHist(dos, voi)

    def update_plot_dvh(self):
        """
        """
        # TODO: clear plot
        dvhs = self.model.plot.dvhs
        if dvhs:
            axes = self.fig.axes

            for dvh in dvhs:
                axes.plot(dvh.x, dvh.y, label=dvh.name)
            # labels are the same for each item in 'self.model.plot.dvhs' list
            axes.set_xlabel(dvhs[0].xlabel)
            axes.set_ylabel(dvhs[0].ylabel)

            self.fig.show()
