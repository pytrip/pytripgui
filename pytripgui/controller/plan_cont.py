import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from pytrip.tripexecuter import Plan

from pytripgui.view.gen.plan import Ui_PlanDialog

logger = logging.getLogger(__name__)


class PlanController(object):
    """
    """

    def __init__(self, model):
        """
        """
        self.model = model

    @staticmethod
    def new_plan(model):
        """
        Creates a new instance of a plan, and adds it to model.
        """
        logger.debug("new_plan()")

        if not model.ctx:
            logger.error("No CT data loaded.")
            return

        # setup a new tripexecuter.plan object
        import pytrip.tripexecuter as pte
        plan = pte.Plan(basename=model.ctx.basename)

        # open a dialog for the user to edit it
        PlanController.edit_plan(model, plan)

        # attach this plan to the list of plans in models.
        model.plans.append(plan)

    @staticmethod
    def edit_plan(model, plan):
        """
        """
        # open the plan configuration dialog
        # https://stackoverflow.com/questions/42505429/pyqt5-gui-structure-advice-needed
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_PlanDialog()
        # plan_ui = dialog_ui # TODO why not being used ?

        dialog_ui.setupUi(dialog)
        PlanController._populate_plan_ui(dialog_ui, model, plan)
        PlanController._setup_plan_callbacks(dialog_ui, model, plan)
        dialog.exec_()
        dialog.show()

    @staticmethod
    def delete_plan(model, plan):
        """
        """
        logger.debug("delete_plan()")
        pass

    @staticmethod
    def _populate_plan_ui(ui, model, plan):
        """
        Fill all widgets with current model data.
        """
        from PyQt5.QtGui import QStandardItemModel
        from PyQt5.QtGui import QStandardItem

        # ----------- General Info Tab ---------------------------
        ui.lineEdit.setText(plan.basename)
        ui.lineEdit_2.setText(plan.comment)
        ui.lineEdit_3.setText(str(plan.__uuid__))

        # ----------- Target Tab ---------------------------------
        voinames = model.vdx.voi_names()

        # TARGET
        ui.comboBox.clear()
        for voi in model.vdx.vois:
            ui.comboBox.addItem(voi.name, voi)
            if plan.voi_target:
                _i = ui.comboBox.findData(voi)
                if _i == -1:  # not found
                    logger.warning("_populate_plan_ui() FIXME")
                else:
                    ui.comboBox.setCurrentIndex(_i)
            else:
                plan.voi_target = model.vdx.vois[0]
                ui.comboBox.setCurrentIndex(0)

        # OAR
        list = ui.listView
        # https://www.pythoncentral.io/pyside-pyqt-tutorial-qlistview-and-qstandarditemmodel/
        listmodel = QStandardItemModel(list)
        for voiname in voinames:
            item = QStandardItem(voiname)
            item.setCheckable(True)
            listmodel.appendRow(item)
        list.setModel(listmodel)

        # INCUBE
        ui.comboBox_2.clear()
        if model.dos:
            for dos in model.dos:
                ui.comboBox_2.addItem(dos.basename, dos)

            if plan.incube_basename:
                ui.comboBox_2.setEnabled(True)
                ui.checkBox.setChecked(True)
                _i = ui.comboBox_2.findText(dos.basename)
                if _i == -1:  # not found
                    logger.warning("_populate_plan_ui() FIXME 2")
                else:
                    ui.comboBox_2.setCurrentIndex(_i)
            else:
                plan.incube_basename = None
                ui.comboBox_2.setEnabled(False)
                ui.checkBox.setChecked(False)

        # TISSUE
        ui.comboBox_3.clear()
        ui.comboBox_3.addItem("(not implemented)")
        ui.comboBox_3.setEnabled(False)

        # RESIDUAL TISSUE
        ui.comboBox_4.clear()
        ui.comboBox_4.addItem("(not implemented)")
        ui.comboBox_4.setEnabled(False)

        # ----------- Dose Delivery Tab ---------------------------
        # TODO: Projectile
        PlanController._setup_plan_combobox(ui.comboBox_5, Plan.opt_methods)
        # TODO: Ripple filter

        # Target Dose Percent
        ui.doubleSpinBox.setValue(plan.target_dose_percent)
        ui.doubleSpinBox_4.setValue(plan.target_dose)

        # ----------- Optimization Tab ----------------------------
        # Iterations
        ui.spinBox.setValue(plan.iterations)
        ui.doubleSpinBox_2.setValue(plan.eps)
        ui.doubleSpinBox_3.setValue(plan.geps)

        PlanController._setup_plan_combobox(ui.comboBox_7, Plan.opt_methods)
        PlanController._setup_plan_combobox(ui.comboBox_8, Plan.opt_principles)
        PlanController._setup_plan_combobox(ui.comboBox_9, Plan.dose_algs)
        PlanController._setup_plan_combobox(ui.comboBox_10, Plan.bio_algs)
        PlanController._setup_plan_combobox(ui.comboBox_11, Plan.opt_algs)

        # ----------- Results Tab --------------------------------
        ui.checkBox_2.setChecked(plan.want_phys_dose)
        ui.checkBox_3.setChecked(plan.want_bio_dose)
        ui.checkBox_4.setChecked(plan.want_dlet)
        ui.checkBox_5.setChecked(plan.want_rst)
        ui.checkBox_6.setEnabled(False)
        ui.checkBox_7.setEnabled(False)

    @staticmethod
    def _setup_projectile_combobox(ui, model, plan):
        """
        This populates the Projectile combobox
        """
        uic = ui.combobox_5
        kernels = model.kernels

        if not kernels:
            from pytripgui.view.dialogs import MyDialogs
            MyDialogs.show_error("Setup dose kernels first in Settings.")
            return

        uic.clear()

        for kernel in kernels:
            uic.addItem(kernel.projectile_name, kernel)

    @staticmethod
    def _setup_plan_combobox(ui_combobox, plan_dict):
        """
        :params ui_combobox: combobox to setup
        :params ui_plan_dict: Plan.opt_method or similar, which will be used for setup.
        """
        uic = ui_combobox
        pdic = plan_dict

        uic.clear()
        for i, key in enumerate(pdic):
            _ttip = None
            _str = pdic[key][1]
            uic.addItem(_str, key)

            if len(pdic[key]) > 2:
                _ttip = pdic[key][2]  # ToolTip
                uic.setItemData(i, _ttip, Qt.ToolTipRole)  # set tool tip for this item

    @staticmethod
    def _setup_plan_callbacks(ui, model, plan):
        """
        Connect all widgets to model.
        No OK button needs to be pressed, when a value is changed, model is updated immediately.
        """

        ui.lineEdit.textChanged.connect(lambda: PlanController._callback(ui, model, plan, "basename"))
        ui.lineEdit_2.textChanged.connect(lambda: PlanController._callback(ui, model, plan, "comment"))

        ui.comboBox.currentIndexChanged.connect(lambda: PlanController._callback(ui, model, plan, "voi_target"))
        # TODO: OAR
        ui.comboBox.currentIndexChanged.connect(lambda: PlanController._callback(ui, model, plan, "incube"))
        ui.checkBox.stateChanged.connect(lambda: PlanController._callback(ui, model, plan, "incube_check"))

        ui.comboBox_5.currentIndexChanged.connect(lambda: PlanController._callback(ui, model, plan, "projectile"))

    @staticmethod
    def _callback(ui, model, plan, plan_attribute_name):
        """
        :params str plan_attribute_name: attribute in pytrip.Plan object.

        TODO: Leszek will kill me for this.
        """
        pa = plan_attribute_name

        if pa == "basename":
            logger.debug("_callback set basename {}".format(ui.lineEdit.text()))
            plan.basename = ui.lineEdit.text()
            return

        if pa == "comment":
            plan.comment = ui.lineEdit_2.text()
            return

        if pa == "voi_target":
            i = ui.comboBox.currentIndex()
            obj = ui.comboBox.itemData(i)
            logger.debug("Set voi_target to VOI {}".format(obj.name))
            plan.target_dose = obj
            return

        if pa == "incube":
            i = ui.comboBox.currentIndex()
            basename = ui.comboBox.itemText(i)
            logger.debug("Set incube to dos.basename {}".format(basename))
            plan.incube_basename = basename
            return

        if pa == "incube_check":
            if ui.checkBox.isChecked():
                ui.comboBox_2.setEnabled(True)
                ui.comboBox_2.setCurrentIndex(0)
                plan.incube_basename = ui.comboBox_2.currentText()
                logger.debug("incube_check: plan.incube_basename set to {}".format(plan.incube_basename))
            else:
                plan.incube_basename = None
                logger.debug("incube_check: plan.incube_basename set to {}".format(plan.incube_basename))
                ui.comboBox_2.setEnabled(False)

        if pa == "projectile":
            logger.debug("Projectile Changed")
