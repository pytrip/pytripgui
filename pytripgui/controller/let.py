import logging

logger = logging.getLogger(__name__)


class Let(object):
    """
    This class holds logic for plotting LET stuff.
    """

    def __init__(self):
        pass

    @staticmethod
    def plot(plc):
        """
        Plot the active LET cube.
        :params plc: PlotController

        """
        logger.debug("plot LET cube")
