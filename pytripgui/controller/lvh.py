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
        self.update_plot_lvh()

    @staticmethod
    def _calc_lvh(let, voi):
        """ Calculates a Lvh
        """
        # TODO, this could be run threaded when loading a LET and VDX is present.

        logger.info("LVH Processing VOI '{:s}'...".format(voi.name))
        return VolHist(let, voi)

    def update_plot_lvh(self):
        """
        """
        # TODO: clear plot
        lvhs = self.model.plot.lvhs
        if lvhs:
            axes = self.fig.axes
            for lvh in lvhs:
                axes.plot(lvh.x, lvh.y, label=lvh.name)
            # labels are the same for each item in 'self.model.plot.lvhs' list
            axes.set_xlabel(lvhs[0].xlabel)
            axes.set_ylabel(lvhs[0].ylabel)

            self.fig.show()
