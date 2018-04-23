import logging
import pytrip as pt

from pytripgui.controller.tree_cont import TreeController
from pytripgui.controller.plot_cont import PlotController
from pytripgui.controller.settings import Settings
from pytripgui.controller.dvh import Dvh
# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

# from pytripgui.controller.plot_cont import PlotController

logger = logging.getLogger(__name__)


class MainController(object):

    # this is probably not correct solution
    # plotupdate = pyqtSignal()

    def __init__(self, app):
        self.model = app.model  # Q: mark private? _model
        self.app = app  # not sure if this is correct. May controller use App?

        self.tree = TreeController(self.model, app.view.ui.treeView, self.app)
        self.plot = PlotController(self.model, app.view.ui)  # ViewCanvas for CTX, VDX and DOS
        self.dvh = Dvh(self.model, self.app.view)   # DVH plot

        self._connect_ui(app.view.ui)

        # self.plotupdate.connect(self.plot.update_viewcanvas)

        # prepare settings
        self.settings = Settings()

    def _connect_ui(self, ui):
        """
        Connect any signals emited from the autogenerated UI to any methods
        of home-made classes.
        """

        # QtDesigner does not really allow custom slot names of different classes.
        # I.e. you may specify "open_ctx" as a slot, but not "ctrl.open_ctx".
        # Solution is simply to manually make all the signal list here.

        ui.actionOpen_Dicom.triggered.connect(self.open_dicom_dialog)
        ui.actionOpen_Voxelplan.triggered.connect(self.open_voxelplan_dialog)
        ui.actionDoseCube.triggered.connect(self.import_dos_dialog)
        ui.actionLETCube.triggered.connect(self.import_let_dialog)
        ui.action_exec.triggered.connect(self.import_exec_dialog)
        ui.actionOpen_Project.triggered.connect(self.open_project)
        ui.actionSave_Project.triggered.connect(self.save_project)
        ui.actionExit.triggered.connect(self.on_exit)
        # ui.tab.resized.connect(self.change_foobar) wont work, doesnt exist

    # called from view class
    def change_foobar(self, event):
        # put control logic here
        logger.debug("Change foobar {}".format(event))
        # self.model.foobar = value
        # self.model.announce_update()

    def open_dicom_dialog(self, event):
        """
        Opens a DICOM set and sets it to the model.
        """
        logger.debug("Open DICOM triggered")

    def open_voxelplan_dialog(self, event):
        """
        Opens a CTX + associated VDX file, and sets it to the model.
        """

        # Start a file dialog for selecting input files
        from pytripgui.view.dialogs import MyDialogs
        ctx_path = MyDialogs.openFileNameDialog(self.app)
        self.open_voxelplan(ctx_path)

    def open_voxelplan(self, ctx_path):
        # Get the CTX cubes first
        logger.debug("Open CTX {:s}".format(ctx_path))
        ctx = pt.CtxCube()
        self.model.ctx = ctx
        self.model.plot.ctx = ctx
        ctx.read(ctx_path)

        # Point to center of slices for default plotting
        self.model.plot.xslice = int(ctx.dimx * 0.5)
        self.model.plot.yslice = int(ctx.dimy * 0.5)
        self.model.plot.zslice = int(ctx.dimz * 0.5)

        self.app.setWindowTitle("PyTRiPGUI - {}".format(ctx.basename))

        # add cube to the treeview
        self.tree.add_ctx(ctx)

        # Check if there is a VDX file with the same basename
        logger.debug("Check for VDX")
        from pytrip.util import TRiP98FilePath
        _b = TRiP98FilePath(ctx_path, ctx).basename
        _n = TRiP98FilePath(ctx_path, ctx).name
        vdx_path = ctx_path.replace(_n, _b) + '.vdx'

        logger.debug("Check if '{:s}' exists...".format(vdx_path))

        # If VDX is there, load it.
        import os.path
        if os.path.isfile(vdx_path):
            logger.debug("   Open '{:s}'".format(vdx_path))
            vdx = pt.VdxCube(self.model.ctx)
            vdx.read(vdx_path)
            self.model.vdx = vdx
            self.model.plot.vdx = vdx

        # add cube to the treeview
        self.tree.add_vdx(vdx)

        # update the canvas
        self.plot.update_viewcanvas()
        # self.updateplot.emit()
        # testing, not sure if this is proper
        # emit signal to update the plot
        # update_viewcanvas()
        # from controller.plot_cont import PlotController
        # self.plotupdate.connect(PlotController.update_viewcanvas)
        # self.plotupdate.emit()

    def import_dos_dialog(self, event):
        """
        Import dose cube.
        """
        # Start a file dialog for selecting input files
        from pytripgui.view.dialogs import MyDialogs
        dos_path = MyDialogs.openFileNameDialog(self.app)
        self.import_dos(dos_path)

    def import_dos(self, dos_path):
        """
        """
        logger.debug("Open DosCube {:s}".format(dos_path))
        dos = pt.DosCube()
        self.model.dos.append(dos)
        dos.read(dos_path)
        # add cube to the treeview
        self.tree.add_dos(dos)

    def import_let_dialog(self, event):
        """
        Import LET cube.
        """
        # Start a file dialog for selecting input files
        from pytripgui.view.dialogs import MyDialogs
        let_path = MyDialogs.openFileNameDialog(self.app)
        self.import_let(let_path)

    def import_let(self, let_path):
        """
        """
        logger.debug("Open LETCube {:s}".format(let_path))
        let = pt.LETCube()
        self.model.dos.append(let)
        let.read(let_path)
        # add cube to the treeview
        self.tree.add_let(let)

    def import_exec_dialog(self, event):
        """
        """
        logger.debug("Import .exec")
        # Start a file dialog for selecting input files
        from pytripgui.view.dialogs import MyDialogs
        exec_path = MyDialogs.openFileNameDialog(self.app)
        self.import_exec(exec_path)

    def import_exec(self, exec_path):
        """
        """
        logger.debug("Open .exec {:s}".format(exec_path))

    def open_project(self, event):
        """
        Opens a project
        """
        logger.debug("Open Project triggered")

    def save_project(self, event):
        """
        Opens a project
        """
        logger.debug("Save Project triggered")

    @staticmethod
    def on_exit(event):
        logger.debug("on_exit() triggered")
        import sys
        sys.exit()
