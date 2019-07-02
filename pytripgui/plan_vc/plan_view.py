from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem
from pytripgui.view.gen.plan import Ui_PlanDialog

import logging
logger = logging.getLogger(__name__)


class PlanQtView(object):
    """
    """
    def __init__(self):
        self.ui = Ui_PlanDialog()
        self.dialog = QtWidgets.QDialog()

        self.ui.setupUi(self.dialog)
        self._setup_callbacks()

    def show(self):
        self.dialog.show()
        self.dialog.exec_()

    def exit(self):
        self.dialog.close()

    def set_ok_callback(self, fun):
        self.ui.accept_buttonBox.accepted.connect(fun)

    def set_cancel_callback(self, fun):
        self.ui.accept_buttonBox.rejected.connect(fun)

    def _setup_callbacks(self):
        pass

    def get_basename_value(self):
        return self.ui.basename_lineEdit.text()

    def set_basename_value(self, basename):
        self.ui.basename_lineEdit.setText(basename)

    def get_comment_value(self):
        return self.ui.comment_lineEdit.text()

    def set_comment_value(self, comment):
        self.ui.comment_lineEdit.setText(comment)

    def get_uuid_value(self):
        return self.ui.uuid_lineEdit.text()

    def set_uuid_value(self, uuid):
        self.ui.uuid_lineEdit.setText(uuid)

    def add_target_roi_with_name(self, target, target_name):
        self.ui.targetROI_comboBox.addItem(target_name, target)

    def set_target_roi_to_this(self, target):
        ui = self.ui

        index_of_target = ui.targetROI_comboBox.findData(target, Qt.UserRole)
        if index_of_target == -1:
            raise Exception("Given kernel wasn't found on the list")
        ui.targetROI_comboBox.setCurrentIndex(index_of_target)

    def get_selected_target_roi(self):
        return self.ui.targetROI_comboBox.currentData()

    def add_oar_with_name(self, voi, voi_name):
        oar_list = self.ui.OAR_treeWidget

        oar_item = QTreeWidgetItem()
        oar_item.setText(0, voi_name)
        oar_item.setData(0, Qt.UserRole, voi)
        oar_item.setCheckState(0, Qt.Unchecked)

        oar_list.addTopLevelItem(oar_item)

    def set_oar_as_checked(self, voi):
        pass    # todo

    def add_kernel_with_name(self, kernel, kernel_name):
        self.ui.kernel_comboBox.addItem(kernel_name, kernel)

    def select_kernel_view_to_this(self, kernel):
        ui = self.ui

        index_of_kernel = ui.kernel_comboBox.findData(kernel, Qt.UserRole)
        if index_of_kernel == -1:
            raise Exception("Given kernel wasn't found on the list")
        ui.kernel_comboBox.setCurrentIndex(index_of_kernel)

    def set_target_dose_value(self, target_dose):
        self.ui.targetDose_doubleSpinBox.setValue(target_dose)

    def set_relative_target_dose_value(self, relative_target_dose):
        self.ui.relativeTargetDose_doubleSpinBox.setValue(relative_target_dose)

    def set_iterations_value(self, iterations):
        self.ui.iterations_spinBox.setValue(iterations)

    def set_eps_value(self, eps):
        self.ui.eps_doubleSpinBox.setValue(eps)

    def set_geps_value(self, geps):
        self.ui.geps_doubleSpinBox.setValue(geps)

    def add_opti_method_with_name(self, opti, opti_name):
        self.ui.optiMethod_comboBox.addItem(opti_name, opti)

    def select_opti_method_view_to_this(self, opti):
        ui = self.ui

        index_of_kernel = ui.optiMethod_comboBox.findData(opti, Qt.UserRole)
        if index_of_kernel == -1:
            raise Exception("Given kernel wasn't found on the list")
        ui.optiMethod_comboBox.setCurrentIndex(index_of_kernel)

    def add_principle_with_name(self, principle, principle_name):
        self.ui.principle_comboBox.addItem(principle_name, principle)

    def select_principle_view_to_this(self, principle):
        ui = self.ui

        index_of_principle = ui.principle_comboBox.findData(principle, Qt.UserRole)
        if index_of_principle == -1:
            raise Exception("Given principle wasn't found on the list")
        ui.principle_comboBox.setCurrentIndex(index_of_principle)

    def add_dose_algorithm_with_name(self, dose_alg, dose_alg_name):
        self.ui.doseAlgorithm_comboBox.addItem(dose_alg_name, dose_alg)

    def select_dose_algorithm_view_to_this(self, dose_alg):
        ui = self.ui

        index_of_dose_alg = ui.doseAlgorithm_comboBox.findData(dose_alg, Qt.UserRole)
        if index_of_dose_alg == -1:
            raise Exception("Given dose algorithm wasn't found on the list")
        ui.doseAlgorithm_comboBox.setCurrentIndex(index_of_dose_alg)

    def add_biol_algorithm_with_name(self, biol_alg, biol_alg_name):
        self.ui.bioAlgorithm_comboBox.addItem(biol_alg_name, biol_alg)

    def select_biol_algorithm_view_to_this(self, biol_alg):
        ui = self.ui

        index_of_biol_alg = ui.bioAlgorithm_comboBox.findData(biol_alg, Qt.UserRole)
        if index_of_biol_alg == -1:
            raise Exception("Given biological algorithm wasn't found on the list")
        ui.bioAlgorithm_comboBox.setCurrentIndex(index_of_biol_alg)

    def add_opti_algorithm_with_name(self, opti_alg, opti_alg_name):
        self.ui.optiAlgorithm_comboBox.addItem(opti_alg_name, opti_alg)

    def select_opti_algorithm_view_to_this(self, opti_alg):
        ui = self.ui

        index_of_opti_alg = ui.optiAlgorithm_comboBox.findData(opti_alg, Qt.UserRole)
        if index_of_opti_alg == -1:
            raise Exception("Given optimization algorithm wasn't found on the list")
        ui.optiAlgorithm_comboBox.setCurrentIndex(index_of_opti_alg)

    def set_physical_dose_dist_state(self, state):
        if state is True:
            self.ui.physicalDoseDist_checkBox.setCheckState(Qt.Checked)
        else:
            self.ui.physicalDoseDist_checkBox.setCheckState(Qt.Unchecked)

    def set_biological_dose_dist_state(self, state):
        if state is True:
            self.ui.biologicalDoseDist_checkBox.setCheckState(Qt.Checked)
        else:
            self.ui.biologicalDoseDist_checkBox.setCheckState(Qt.Unchecked)

    def set_dose_averaged_let_state(self, state):
        if state is True:
            self.ui.doseAveragedLET_checkBox.setCheckState(Qt.Checked)
        else:
            self.ui.doseAveragedLET_checkBox.setCheckState(Qt.Unchecked)

    def set_raster_scan_file_state(self, state):
        if state is True:
            self.ui.rasterScanFile_checkBox.setCheckState(Qt.Checked)
        else:
            self.ui.rasterScanFile_checkBox.setCheckState(Qt.Unchecked)