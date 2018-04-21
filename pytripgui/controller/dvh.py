import logging

logger = logging.getLogger(__name__)


class Dvh(object):
    """
    This class holds logic for plotting CTX stuff.
    """

    def __init__(self, model, dvh):
        """
        """
        self.model = model
        self.dvh = dvh  # plot widget, need better name, to avoid confusion

    def add_dvh(self, dos, voi):
        """
        Calculates and plots a DVH based on dos and voi.
        """
        dvh = self._calc_dvh(dos, voi)
        self.model.plot.dvhs.append(dvh)
        self.update_plot()

    @staticmethod
    def _calc_dvh(dos, voi):
        """ Calculates a Dvh
        """

        from pytrip.util import volume_histogram
        logger.debug("Processing VOI '{:s}'...".format(voi.name))
        x, y = volume_histogram(dos, voi)
        x = x * 0.1  # convert %% to %
        return [x, y]

    def update_plot(self):
        """
        """
        # TODO: clear plot

        for dvh in self.model.plot.dvhs:
            self.dvh.plot(dvh)
        self.dvh.show()
