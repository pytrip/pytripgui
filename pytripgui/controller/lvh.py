import logging

from pytrip.volhist import VolHist

logger = logging.getLogger(__name__)


class Lvh:
    """
    This class holds logic for plotting CTX stuff.
    """
    def __init__(self, model, view):
        """
        """
        self.model = model
        self.view = view
        self.fig = self.view.ui.lvh
        self.fig.xlabel = "LET [keV/um]"
        self.fig.ylabel = "Volume [%]"

    def add_lvh(self, let, voi):
        """
        Calculates and plots a LVH based on let and voi.
        """
        pm = self.model.plot

        lvh = self._calc_lvh(let, voi)
        if not lvh.x or not lvh.y:
            return
        pm.lvhs.append(lvh)
        self.update_plotlvh()

    @staticmethod
    def _calc_lvh(let, voi):
        """ Calculates a Lvh
        """
        # TODO, this could be run threaded when loading a LET and VDX is present.

        logger.info("LVH Processing VOI '{:s}'...".format(voi.name))
        return VolHist(let, voi)

    def update_plotlvh(self):
        """
        """
        # TODO: clear plot
        axes = self.fig.axes

        for lvh in self.model.plot.lvhs:
            axes.plot(lvh.x, lvh.y, label=lvh.name)
        axes.set_xlabel(lvh.xlabel)
        axes.set_ylabel(lvh.ylabel)

        self.fig.show()
