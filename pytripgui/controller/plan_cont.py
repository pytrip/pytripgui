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

        # setup a new tripexecuter.plan object
        import pytrip.tripexecuter as pte
        plan = pte.Plan(basename=model.ctx.basename)

        # attach this plan to the list of plans in models.
        model.plans.append(plan)

        # open a dialog for the user to edit it
        PlanController.edit_plan(model, plan)
        model.plans.append(plan)

    @staticmethod
    def edit_plan(model, plan):
        """
        """
        # open the plan configuration dialog
        # https://stackoverflow.com/questions/42505429/pyqt5-gui-structure-advice-needed
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_PlanDialog()
        dialog_ui.setupUi(dialog)
        PlanController._populate_plan_ui(dialog_ui, model, plan)
        PlanController._callbacks_plan_ui(dialog_ui, model, plan)
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

        voinames = [voi.name for voi in model.vdx.vois]

        # TARGET
        ui.comboBox.clear()
        for voi in model.vdx.vois:
            ui.comboBox.addItem(voi.name, voi)

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
        for dos in model.dos:
            ui.comboBox_2.addItem(dos.basename, dos)

        # TISSUE
        ui.comboBox_3.clear()
        ui.comboBox_3.addItem("(not implemented)")
        ui.comboBox_3.setEnabled(False)

        # RESIDUAL TISSUE
        ui.comboBox_4.clear()
        ui.comboBox_4.addItem("(not implemented)")
        ui.comboBox_4.setEnabled(False)

        # TODO: Projectile

        # TODO: Ripple filter

        # Target Dose Percent
        ui.doubleSpinBox.setValue(plan.target_dose_percent)
        ui.doubleSpinBox_4.setValue(plan.target_dose)

        # Iterations
        ui.spinBox.setValue(plan.iterations)
        ui.doubleSpinBox_2.setValue(plan.eps)
        ui.doubleSpinBox_3.setValue(plan.geps)

        PlanController._setup_plan_combobox(ui.comboBox_7, Plan.opt_methods)
        PlanController._setup_plan_combobox(ui.comboBox_8, Plan.opt_principles)
        PlanController._setup_plan_combobox(ui.comboBox_9, Plan.dose_algs)
        PlanController._setup_plan_combobox(ui.comboBox_10, Plan.bio_algs)
        PlanController._setup_plan_combobox(ui.comboBox_11, Plan.opt_algs)

        ui.checkBox_2.setChecked(plan.want_phys_dose)
        ui.checkBox_3.setChecked(plan.want_bio_dose)
        ui.checkBox_4.setChecked(plan.want_dlet)
        ui.checkBox_5.setChecked(plan.want_rst)
        ui.checkBox_6.setEnabled(False)
        ui.checkBox_7.setEnabled(False)

        ui.lineEdit.setText(plan.basename)
        ui.lineEdit_2.setText(plan.comment)
        ui.lineEdit_3.setText(str(plan.__uuid__))

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
    def _callbacks_plan_ui(ui, model, plan):
        """
        Connect all widgets to model.
        No OK button needs to be pressed, when a value is changed, model is updated immediately.
        """
        pass
