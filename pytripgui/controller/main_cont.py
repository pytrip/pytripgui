import logging
import pytrip as pt

from pytripgui.controller.tree_cont import TreeController
from pytripgui.controller.plot_cont import PlotController
from pytripgui.controller.plan_cont import PlanController
from pytripgui.controller.settings import Settings
from pytripgui.controller.dvh import Dvh
from pytripgui.controller.lvh import Lvh
# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

logger = logging.getLogger(__name__)


class MainController(object):

    # this is probably not correct solution
    # plotupdate = pyqtSignal()

    def __init__(self, app):
        self.model = app.model  # Q: mark private? _model
        self.app = app  # not sure if this is correct. May controller use App?

        self.plot = PlotController(self.model, app.view.ui)  # ViewCanvas for CTX, VDX and DOS
        self.tree = TreeController(self.model, app.view.ui, self)  # TODO: get rid of self here
        self.dvh = Dvh(self.model, self.app.view)   # DVH plot
        self.lvh = Lvh(self.model, self.app.view)   # DVH plot
        self.plnc = PlanController(self.model)

        self._connect_ui()     # connect signals to autogenerated UI
        self._open_settings()  # open settings file and update model

        # self.plotupdate.connect(self.plot.update_viewcanvas)

    def _open_settings(self):
        """
        """
        model = self.model
        st = Settings()
        self.settings = st

        model.dicom_path = st.load("general.import.dicom_path")
        model.voxelplan_path = st.load("general.import.voxelplan_path")
        model.tripexec_path = st.load("general.import.tripexec_path")

    def _connect_ui(self):
        """
        Connect any signals emited from the autogenerated UI to any methods
        of home-made classes.
        """

        ui = self.app.view.ui
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
        ui.actionAbout.triggered.connect(self.on_about)
        ui.actionNew_Plan.triggered.connect(self.on_new_plan)

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
        model = self.model
        st = self.settings

        import os
        dir = os.path.dirname(model.dicom_path)

        # Start a file dialog for selecting input files
        from pytripgui.view.dialogs import MyDialogs
        dir = MyDialogs.openDirectoryDialog(self.app,
                                            "Open Directory with DICOM Files",
                                            dir)
        if not dir:
            return
        self.open_dicom(dir)
        model.dicom_path = dir
        st.save("general.import.dicom_path", dir)

    def open_dicom(self, dir):
        """
        """
        model = self.model    # local object of plot_model
        pm = self.model.plot  # local object of plot_model

        logger.debug("open dicom '{}'".format(dir))
        dcm = pt.dicomhelper.read_dicom_dir(dir)

        ctx = None
        vdx = None

        if 'images' in dcm:
            logger.debug("Found images in DICOM")
            ctx = pt.CtxCube()
            ctx.read_dicom(dcm)
            model.ctx = ctx
            pm.ctx = ctx

        if 'rtss' in dcm:
            logger.debug("Found rtss in DICOM")
            vdx = pt.VdxCube(cube=ctx)
            vdx.read_dicom(dcm)
            for voi in vdx.vois:
                pm.vois.append(voi)

            model.vdx = vdx
            pm.vdx = vdx

        # TODO: plan data

        # add cube to the treeview
        self.tree.add_vdx(vdx)

        # update the canvas
        self.plot.update_viewcanvas()

    def open_voxelplan_dialog(self, event):
        """
        Opens a CTX + associated VDX file, and sets it to the model.
        Path will be saved to settings.
        """
        model = self.model
        st = self.settings

        import os
        model.wdir = os.path.dirname(model.voxelplan_path)

        # Start a file dialog for selecting input files
        from pytripgui.view.dialogs import MyDialogs
        path = MyDialogs.openFileNameDialog(self.app,
                                            "Open Voxelplan file",
                                            model.wdir,
                                            'hed')
        if not path:
            return
        self.open_voxelplan(path)
        model.voxelplan_path = path
        st.save("general.import.voxelplan_path", path)

    def open_voxelplan(self, ctx_path):
        """
        Open a Voxelplan type CTX and possibly a VDX if one exists with the same basename.
        """

        model = self.model    # local object of plot_model
        pm = self.model.plot  # local object of plot_model

        # Get the CTX cubes first
        logger.debug("Open CTX {:s}".format(ctx_path))
        ctx = pt.CtxCube()
        ctx.read(ctx_path)

        # update model
        model.ctx = ctx
        pm.ctx = ctx

        # Point to center of slices for default plotting
        pm.xslice = int(ctx.dimx * 0.5)
        pm.yslice = int(ctx.dimy * 0.5)
        pm.zslice = int(ctx.dimz * 0.5)
        # TODO: we assume transversal view as start. fixme.
        pm.slice_pos_idx = int(ctx.dimz * 0.5)

        # show file basename in window title
        self.app.setWindowTitle("PyTRiPGUI - {}".format(ctx.basename))

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

            # update model
            model.vdx = vdx
            pm.vdx = vdx

            # enable all VOIs to be plotted
            for voi in vdx.vois:
                pm.vois.append(voi)

        # add cube to the treeview<s
        self.tree.update_tree()

        # update the canvas
        self.plot.update_viewcanvas()

    def import_dos_dialog(self, event):
        """
        Open the import dose cube dialog.
        """
        model = self.model

        # offer to look for .dos in the same path as where CTX/VDX was found.
        # however, contrary to CTX/VDX this is not saved to settings.
        import os
        model.wdir = os.path.dirname(model.voxelplan_path)

        from pytripgui.view.dialogs import MyDialogs
        path = MyDialogs.openFileNameDialog(self.app,
                                            "Import DoseCube",
                                            model.wdir,
                                            'dos')
        if not path:
            return
        self.import_dos(path)

    def import_dos(self, dos_path):
        """
        Import a dos cube, add it to the list of loaded dos cubes.
        """

        model = self.model    # local object of plot_model
        pm = self.model.plot  # local object of plot_model

        logger.debug("Open DosCube {:s}".format(dos_path))
        dos = pt.DosCube()

        dos.read(dos_path)

        # update model
        model.dos.append(dos)
        pm.dos = dos  # display new loaded cube immediately.

        # add cube to the treeview
        self.tree.update_tree()
        self.plot.update_viewcanvas()

    def import_let_dialog(self, event):
        """
        Open the import LET cube dialog.
        """
        model = self.model

        # offer to look for .dos in the same path as where CTX/VDX was found.
        # however, contrary to CTX/VDX this is not saved to settings.
        import os
        model.wdir = os.path.dirname(model.voxelplan_path)

        from pytripgui.view.dialogs import MyDialogs
        path = MyDialogs.openFileNameDialog(self.app,
                                            "Import LETCube",
                                            model.wdir,
                                            'let')
        if not path:
            return

        self.import_let(path)

    def import_let(self, let_path):
        """
        Import a let cube, add it to the list of loaded dos cubes.
        """

        model = self.model    # local object of plot_model
        pm = self.model.plot  # local object of plot_model

        logger.debug("Open LETCube {:s}".format(let_path))
        let = pt.LETCube()
        let.read(let_path)

        # update model
        model.let.append(let)
        pm.let = let  # display new loaded cube immediately.

        # add cube to the treeview
        self.tree.update_tree()
        self.plot.update_viewcanvas()

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

    def on_about(self, event):
        """
        """
        # import os
        from PyQt5.QtWidgets import QMessageBox
        from pytripgui import __version__ as pytripgui_version
        from pytrip import __version__ as pytrip_version
        # from pytripgui.util import main_dir

        # with open(os.path.join(main_dir(), "res", "LICENSE.rst"), "rU") as fp:
        #     licence = fp.read()

        title = "PyTRiPGUI"
        text = ""
        # text += "PyTRiPGUI is a webfrontend to PyTRiP and TRiP98.\n"
        text += "PyTRipGUI Version: " + pytripgui_version + "\n"
        text += "PyTRiP Version:" + pytrip_version + "\n"
        text += "\n"
        text += "(c) 2012 - 2018 PyTRiP98 Developers\n"
        # text += "<a href=\"https://github.com/pytrip/pytripgui\">'https://github.com/pytrip/pytripgui'</a>\n"
        # text += licence

        text += "    Niels Bassler\n"
        text += "    Leszek Grzanka\n"
        text += "\n"
        text += "Previous contributors:\n"
        text += "    Jakob Toftegaard\n"

        QMessageBox.about(self.app, title, text)

    def on_new_plan(self, event):
        """
        New plan opened from window->plan->New Plan
        """
        model = self.model
        from pytripgui.controller.plan_cont import PlanController
        PlanController.new_plan(model)



    @staticmethod
    def on_exit(event):
        logger.debug("on_exit() triggered")
        import sys
        sys.exit()
