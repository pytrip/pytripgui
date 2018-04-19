import logging

logger = logging.getLogger(__name__)


class Dos(object):
    """
    This class holds logic for plotting DOS stuff.
    """
    def __init__(self):
        pass

    @staticmethod
    def plot(plc):
        """
        Plot the active dos cube.
        :params plc: PlotController

        """
        logger.debug("plot Dos cube")
