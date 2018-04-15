import logging
import pytrip as pt

# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

# from controller.plot_cont import PlotController

logger = logging.getLogger(__name__)


class MainController(object):

    # this is probably not correct solution
    # plotupdate = pyqtSignal(int, name='plotupdate')

    def __init__(self, model, app):
        self.model = model
        self.app = app  # not sure if this is correct. May controller use App?

    # called from view class
    def change_foobar(self, value):
        # put control logic here
        self.model.foobar = value
        self.model.announce_update()

    def open_ctx(self, model):
        """
        Opens a CTX file, and sets it to the model.
        """
        logger.debug("Open CTX")
        from view.dialogs import MyDialogs
        ctx_path = MyDialogs.openFileNameDialog(self.app)
        self.model.ctx = pt.CtxCube()
        self.model.ctx.read(ctx_path)

        # testing, not sure if this is proper
        # emit signal to update the plot
        # update_plot()
        # from controller.plot_cont import PlotController
        # self.plotupdate.connect(PlotController.update_plot)
        # self.plotupdate.emit()
