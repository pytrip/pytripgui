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

        self.current_slice = 0  # current slice to be viewed

    # called from view class
    def change_foobar(self, value):
        # put control logic here
        self.model.foobar = value
        self.model.announce_update()

    def open_voxelplan(self, model):
        """
        Opens a CTX + associated VDX file, and sets it to the model.
        """

        # Start a file dialog for selecting input files
        from view.dialogs import MyDialogs
        ctx_path = MyDialogs.openFileNameDialog(self.app)

        # Get the CTX cubes first
        logger.debug("Open CTX {:s}".format(ctx_path))
        self.model.ctx = pt.CtxCube()
        self.model.ctx.read(ctx_path)

        # Check if there is a VDX file with the same basename
        logger.debug("Check for VDX")
        from pytrip.util import TRiP98FilePath
        _b = TRiP98FilePath(ctx_path, self.model.ctx).basename
        _n = TRiP98FilePath(ctx_path, self.model.ctx).name
        vdx_path = ctx_path.replace(_n, _b) + '.vdx'

        logger.debug("Check if '{:s}' exists...".format(vdx_path))

        import os.path
        if os.path.isfile(vdx_path):
            logger.debug("   Open '{:s}'".format(vdx_path))
            self.model.vdx = pt.VdxCube(self.model.ctx)
            self.model.vdx.read(vdx_path)

        self.app.tctrl.update_tree()
        self.app.pctrl.update_plot()

        # testing, not sure if this is proper
        # emit signal to update the plot
        # update_plot()
        # from controller.plot_cont import PlotController
        # self.plotupdate.connect(PlotController.update_plot)
        # self.plotupdate.emit()
