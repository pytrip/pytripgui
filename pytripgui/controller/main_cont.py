import os
import pytrip as pt

from pytripgui.controller.tree_cont import TreeController
from pytripgui.viewcanvas_vc.viewcanvas_cont import ViewCanvasCont
from pytripgui.controller.settings_cont import SettingsController
from pytripgui.controller.dvh import Dvh
from pytripgui.controller.lvh import Lvh

import logging
logger = logging.getLogger(__name__)


class MainController(object):

    # this is probably not correct solution
    # plotupdate = pyqtSignal()

    def __init__(self, app):
        self.model = app.model  # Q: mark private? _model
        self.app = app  # not sure if this is correct. May controller use App?

        self.plot = ViewCanvasCont(self.model.one_plot, app.view.ui.one_viewcanvas)  # ViewCanvas for CTX, VDX and DOS
        self.tree = TreeController(self.model, app.view.ui, self)  # TODO: get rid of self here
        self.dvh = Dvh(self.model, self.app.view)   # DVH plot
        self.lvh = Lvh(self.model, self.app.view)   # DVH plot

        self._connect_ui()     # connect signals to autogenerated UI
        self._open_settings()  # open settings file and update model

        # self.plotupdate.connect(self.plot.update_viewcanvas)

    def _open_settings(self):
        """
        """
        model = self.model

        self.settings = SettingsController(model)

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

        ui.actionExport_Dicom.triggered.connect(self.export_dicom_dialog)
        ui.actionExport_Voxelplan.triggered.connect(self.export_voxelplan_dialog)

        ui.actionExit.triggered.connect(self.on_exit)
        ui.actionAbout.triggered.connect(self.on_about)
        ui.actionNew_Plan.triggered.connect(self.on_new_plan)

        ui.actionTRiP98_Config.triggered.connect(self.on_trip98_config)
        ui.actionBeam_Kernels.triggered.connect(self.on_kernel)

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

        ddir = os.path.dirname(model.dicom_path)

        # Start a file dialog for selecting input files
        from pytripgui.view.dialogs import MyDialogs
        ddir = MyDialogs.openDirectoryDialog(self.app,
                                             "Open Directory with DICOM Files",
                                             ddir)
        if not ddir:
            return
        self.open_dicom(ddir)
        model.dicom_path = ddir
        self.settings.save()

    def open_dicom(self, ddir):
        """
        Open a DICOM directory. Images must be present. RTSS is optional.
        """
        model = self.model    # local object of plot_model
        pm = self.model.plot  # local object of plot_model

        logger.debug("open dicom '{}'".format(ddir))
        dcm = pt.dicomhelper.read_dicom_dir(ddir)

        ctx = None
        vdx = None

        if 'images' in dcm:
            logger.debug("Found images in DICOM")
            ctx = pt.CtxCube()
            ctx.read_dicom(dcm)

            model.ctx = ctx
            pm.ctx = ctx
        else:
            from pytripgui.view.dialogs import MyDialogs
            MyDialogs.show_error("No images found in selected DICOM directory.")
            return

        if 'rtss' in dcm:
            logger.debug("Found rtss in DICOM")
            vdx = pt.VdxCube(cube=ctx)
            vdx.read_dicom(dcm)
            for voi in vdx.vois:
                pm.vois.append(voi)

            # This is a workaround for pytrip issue #455 https://github.com/pytrip/pytrip/issues/455
            vdx.basename = "basename"

            model.vdx = vdx
            pm.vdx = vdx

        # TODO: RTplan data

        # add cube to the treeviews
        self.tree.update_tree()

        # update the canvas
        self.plot.update_viewcanvas()

    def open_voxelplan_dialog(self, event):
        """
        Opens a CTX + associated VDX file, and sets it to the model.
        Path will be saved to settings.
        """
        model = self.model

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

        self.settings.save()

    def open_voxelplan(self, ctx_path):
        """
        Open a Voxelplan type CTX and possibly a VDX if one exists with the same basename.
        """

        model = self.model    # local object of plot_model

        # Get the CTX cubes first
        logger.debug("Open CTX {:s}".format(ctx_path))
        ctx = pt.CtxCube()
        ctx.read(ctx_path)

        # update model
        model.ctx = ctx
        self.model.one_plot.set_ctx(ctx)

        # show file basename in window title
        self.app.setWindowTitle("PyTRiPGUI - {}".format(ctx.basename))

        # Check if there is a VDX file with the same basename
        logger.debug("Check for VDX")
        from pytrip.util import TRiP98FilePath
        _d = TRiP98FilePath(ctx_path, ctx).dir_basename  # returns full path, but without suffix.
        vdx_path = _d + ".vdx"

        logger.debug("Check if '{:s}' exists...".format(vdx_path))

        # If VDX is there, load it.
        if os.path.isfile(vdx_path):
            logger.debug("   Open '{:s}'".format(vdx_path))
            vdx = pt.VdxCube(self.model.ctx)
            vdx.read(vdx_path)

            # update model
            model.vdx = vdx

        # update the canvas
        self.plot.update_viewcanvas()

    def export_voxelplan_dialog(self, event):
        """
        Choose path for CTX + associated VDX file Export.
        """
        model = self.model

        from pytripgui.view.dialogs import MyDialogs

        if not model.ctx:
            MyDialogs.show_error("No CTX data available for export.")
            return None

        import os
        model.wdir = os.path.dirname(model.voxelplan_path)
        path_guess = os.path.join(model.wdir, model.ctx.basename + ".hed")

        # Start a file dialog for selecting input files
        path = MyDialogs.saveFileNameDialog(self.app,
                                            "Open Voxelplan file",
                                            path_guess,
                                            'hed')

        if path:
            self.export_voxelplan(path)
            model.voxelplan_path = path
            self.settings.save()

    def export_voxelplan(self, ctx_path):
        """
        Saves CTX and optional VDX data.
        Changes the ctx.basename to be in sync with the stem of the ctx_path. Same for optional VDX.
        """
        logger.debug("export_voxelplan() ctx_path={}".format(ctx_path))

        vdx_path = ctx_path   # hardcoded: VDX will always be stored along with CTX.
        if ".hed" in ctx_path:
            vdx_path = vdx_path.replace(".hed", ".vdx")
        elif ".ctx" in ctx_path:
            vdx_path = vdx_path.replace(".ctx", ".vdx")
        model = self.model
        ctx = self.model.ctx

        # If filename is not the default basename, then change the basename to the new stem of new path.
        from pytrip.util import TRiP98FilePath

        # os.path.basename(): see pytrip #456 https://github.com/pytrip/pytrip/issues/456
        _new_basename = TRiP98FilePath(os.path.basename(ctx_path), pt.CtxCube).basename
        if _new_basename != ctx.basename:
            logger.info("ctx.basename changed '{}' -> '{}'".format(ctx.basename, _new_basename))
            ctx.basename = _new_basename
            self.tree.update_tree()  # to trigger update of basenames in tree
            self.app.setWindowTitle("PyTRiPGUI - {}".format(ctx.basename))  # update window

        # Get the CTX cubes first
        logger.debug("Export CTX {:s}".format(ctx_path))
        ctx.write(ctx_path)

        # Check if there is a VDX file with the same basename
        if model.vdx:
            vdx = model.vdx
            # see pytrip #456 https://github.com/pytrip/pytrip/issues/456
            _new_basename = TRiP98FilePath(os.path.basename(vdx_path), pt.Cube).basename
            if _new_basename != vdx.basename:
                logger.info("vdx.basename changed '{}' -> '{}'".format(vdx.basename, _new_basename))
                vdx.basename = _new_basename
                self.tree.update_tree()  # to trigger update of basenames in tree
            logger.debug("Export VDX {:s}".format(vdx_path))
            vdx.write(vdx_path)

    def export_dicom_dialog(self, event):
        """
        Choose dir for DICOM Export.
        """
        logger.warning("export_dicom_dialog()")

        model = self.model

        ddir = os.path.dirname(model.dicom_path)

        from pytripgui.view.dialogs import MyDialogs
        ddir = MyDialogs.saveDirectoryDialog(self.app, "Export DICOM to Directory", ddir)

        if not ddir:
            return

        self.export_dicom(ddir)
        model.dicom_path = ddir
        self.settings.save()
        return None

    def export_dicom(self, ddir):
        """
        Export model.ctx data to directory "ddir" as DICOM.
        If model.ctx is absent, throw an error dialog.
        if model.vdx is present, export these as well.
        """
        logger.warning("export_dicom() ddir={}".format(ddir))
        ctx = self.model.ctx
        vdx = self.model.vdx

        if ctx:
            logger.debug("export CTX to DICOM")
            ctx.write_dicom(ddir)
        else:
            from pytripgui.view.dialogs import MyDialogs
            MyDialogs.show_error("No CT Data available for export.")

        if vdx:
            logger.debug("export VDX to DICOM")
            vdx.write_dicom(ddir)

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
        dos = self.model.dos_container.import_from_file(dos_path)
        self.model.plot.dos = dos  # display new loaded cube immediately.

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
        pm = self.model.plot  # local object of plot_model

        let = self.model.let_container.import_let_from_file(let_path)
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

        # with open(os.path.join(main_dir(), "res", "LICENSE.rst"), "rU") as fp:
        #     licence = fp.read()

        title = "PyTRiPGUI"
        text = ""
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

    def on_trip98_config(self, event):
        """
        Config menu opened from window->Settings->TRiP98 Config
        """
        logger.debug("TRiP config menu()")

        from pytripgui.config_vc import ConfigQtView
        from pytripgui.config_vc import ConfigController

        view = ConfigQtView()

        controller = ConfigController(self.model.trip_config, view)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            self.settings.save()

    def on_new_plan(self, event):
        """
        New plan opened from window->plan->New Plan
        """
        logger.debug("add_new_plan() {}".format(None))

        from pytrip.tripexecuter import Plan
        from pytripgui.plan_vc import PlanQtView
        from pytripgui.plan_vc import PlanController

        # selected_plan = self._node_obj
        plan = Plan()
        plan.basename = self.model.ctx.basename
        view = PlanQtView()
        global_kernels = self.model.kernels
        default_kernel = self.model.kernels[0]  # TODO select default kernel
        plan.kernel = default_kernel

        controller = PlanController(plan, view, global_kernels, self.model.vdx.vois)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            self.model.plans.append(plan)
            self.tree.update_tree()

    def on_kernel(self, event):
        """
        Kernel dialog opened from window->settings->kernel
        """
        from pytripgui.kernel_vc import KernelQtView
        from pytripgui.kernel_vc import KernelController

        model = self.model.kernels
        view = KernelQtView()
        controller = KernelController(model, view)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            self.settings.save()

    @staticmethod
    def on_exit(event):
        logger.debug("on_exit() triggered")
        import sys
        sys.exit()
