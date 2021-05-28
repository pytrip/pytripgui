from pytripgui.view.qt_gui import UiPlanDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QRadioButton, QMessageBox

import logging

logger = logging.getLogger(__name__)


class PlanQtView:
    """
    """
    def __init__(self, parent=None):
        self.ui = UiPlanDialog(parent)

    def show(self):
        self.ui.show()
        self.ui.exec_()

    def exit(self):
        self.ui.close()

    def set_ok_callback(self, fun):
        self.ui.accept_buttonBox.accepted.connect(fun)

    def set_cancel_callback(self, fun):
        self.ui.accept_buttonBox.rejected.connect(fun)

    def show_info(self, name, content):
        QMessageBox.information(self.ui, name, content)

    @property
    def basename(self):  # start
        return self.ui.basename_lineEdit.text()

    @basename.getter
    def basename(self):  # start
        return self.ui.basename_lineEdit.text()

    @basename.setter
    def basename(self, basename):
        self.ui.basename_lineEdit.setText(basename)

    @property
    def comment(self):
        return self.ui.comment_lineEdit.text()

    @comment.getter
    def comment(self):
        return self.ui.comment_lineEdit.text()

    @comment.setter
    def comment(self, comment):
        self.ui.comment_lineEdit.setText(comment)

    @property
    def uuid(self):
        return self.ui.uuid_lineEdit.text()

    @uuid.getter
    def uuid(self):
        return self.ui.uuid_lineEdit.text()

    @uuid.setter
    def uuid(self, uuid):
        self.ui.uuid_lineEdit.setText(uuid)

    def add_target_roi_with_name(self, target, target_name, checked=False):
        target_item = QRadioButton()
        target_item.setText(target_name)
        if checked:
            target_item.setChecked(Qt.Checked)

        item = QListWidgetItem(self.ui.targetROI_listWidget)
        item.setData(Qt.UserRole, target)

        self.ui.targetROI_listWidget.setItemWidget(item, target_item)

    def get_selected_target_roi(self):
        for item in self.ui.targetROI_listWidget.findItems("", Qt.MatchRegExp):
            target_q_radio_button = self.ui.targetROI_listWidget.itemWidget(item)
            if target_q_radio_button.isChecked():
                return item.data(Qt.UserRole)

    def add_oar_with_name(self, voi, voi_name):
        oar_item = QListWidgetItem()
        oar_item.setText(voi_name)
        oar_item.setData(Qt.UserRole, voi)
        oar_item.setCheckState(Qt.Unchecked)

        self.ui.OAR_listWidget.addItem(oar_item)

    def set_oar_as_checked(self, voi):
        oar_list = self.ui.OAR_listWidget.findItems(voi.name, Qt.MatchExactly)
        found_oar_to_check = oar_list.pop()
        found_oar_to_check.setCheckState(Qt.Checked)

    def get_all_checked_oar_as_list(self):
        oar_widget = self.ui.OAR_listWidget
        voi_count = oar_widget.count()

        checked_oars = []
        for i in range(voi_count):
            oar = oar_widget.item(i)
            if oar.checkState():
                checked_oars.append(oar.data(Qt.UserRole))

        return checked_oars

    def add_kernel_with_name(self, kernel, kernel_name):
        self.ui.kernel_comboBox.addItem(kernel_name, kernel)

    def get_selected_krenel(self):
        return self.ui.kernel_comboBox.currentData(Qt.UserRole)

    def select_kernel_view_to_this(self, kernel):
        index_of_kernel = self.ui.kernel_comboBox.findData(kernel, Qt.UserRole)
        if index_of_kernel == -1:
            logger.warning("Given kernel wasn't found on the list")
            return
        self.ui.kernel_comboBox.setCurrentIndex(index_of_kernel)

    @property
    def target_dose(self):
        return self.ui.targetDose_doubleSpinBox.value()

    @target_dose.getter
    def target_dose(self):
        return self.ui.targetDose_doubleSpinBox.value()

    @target_dose.setter
    def target_dose(self, target_dose):
        self.ui.targetDose_doubleSpinBox.setValue(target_dose)

    @property
    def relative_target_dose(self):
        return self.ui.relativeTargetDose_doubleSpinBox.value()

    @relative_target_dose.getter
    def relative_target_dose(self):
        return self.ui.relativeTargetDose_doubleSpinBox.value()

    @relative_target_dose.setter
    def relative_target_dose(self, relative_target_dose):
        self.ui.relativeTargetDose_doubleSpinBox.setValue(relative_target_dose)

    @property
    def iterations(self):
        return self.ui.iterations_spinBox.value()

    @iterations.getter
    def iterations(self):
        return self.ui.iterations_spinBox.value()

    @iterations.setter
    def iterations(self, iterations):
        self.ui.iterations_spinBox.setValue(iterations)

    @property
    def eps(self):
        return self.ui.eps_doubleSpinBox.value()

    @eps.getter
    def eps(self):
        return self.ui.eps_doubleSpinBox.value()

    @eps.setter
    def eps(self, eps):
        self.ui.eps_doubleSpinBox.setValue(eps)

    @property
    def geps(self):
        return self.ui.geps_doubleSpinBox.value()

    @geps.getter
    def geps(self):
        return self.ui.geps_doubleSpinBox.value()

    @geps.setter
    def geps(self, geps):
        self.ui.geps_doubleSpinBox.setValue(geps)

    def add_opti_method_with_name(self, opti, opti_name):
        self.ui.optiMethod_comboBox.addItem(opti_name, opti)

    def get_selected_opti_method(self):
        return self.ui.optiMethod_comboBox.currentData(Qt.UserRole)

    def select_opti_method_view_to_this(self, opti):
        index_of_kernel = self.ui.optiMethod_comboBox.findData(opti, Qt.UserRole)
        if index_of_kernel == -1:
            raise Exception("Given kernel wasn't found on the list")
        self.ui.optiMethod_comboBox.setCurrentIndex(index_of_kernel)

    def add_principle_with_name(self, principle, principle_name):
        self.ui.principle_comboBox.addItem(principle_name, principle)

    def get_selected_principle(self):
        return self.ui.principle_comboBox.currentData(Qt.UserRole)

    def select_principle_view_to_this(self, principle):
        index_of_principle = self.ui.principle_comboBox.findData(principle, Qt.UserRole)
        if index_of_principle == -1:
            raise Exception("Given principle wasn't found on the list")
        self.ui.principle_comboBox.setCurrentIndex(index_of_principle)

    def add_dose_algorithm_with_name(self, dose_alg, dose_alg_name):
        self.ui.doseAlgorithm_comboBox.addItem(dose_alg_name, dose_alg)

    def get_selected_dose_algorithm(self):
        return self.ui.doseAlgorithm_comboBox.currentData(Qt.UserRole)

    def select_dose_algorithm_view_to_this(self, dose_alg):
        index_of_dose_alg = self.ui.doseAlgorithm_comboBox.findData(dose_alg, Qt.UserRole)
        if index_of_dose_alg == -1:
            raise Exception("Given dose algorithm wasn't found on the list")
        self.ui.doseAlgorithm_comboBox.setCurrentIndex(index_of_dose_alg)

    def add_bio_algorithm_with_name(self, biol_alg, biol_alg_name):
        self.ui.bioAlgorithm_comboBox.addItem(biol_alg_name, biol_alg)

    def get_selected_bio_algorithm(self):
        return self.ui.bioAlgorithm_comboBox.currentData(Qt.UserRole)

    def select_bio_algorithm_view_to_this(self, biol_alg):
        index_of_biol_alg = self.ui.bioAlgorithm_comboBox.findData(biol_alg, Qt.UserRole)
        if index_of_biol_alg == -1:
            raise Exception("Given biological algorithm wasn't found on the list")
        self.ui.bioAlgorithm_comboBox.setCurrentIndex(index_of_biol_alg)

    def add_opti_algorithm_with_name(self, opti_alg, opti_alg_name):
        self.ui.optiAlgorithm_comboBox.addItem(opti_alg_name, opti_alg)

    def get_selected_opti_algorithm(self):
        return self.ui.optiAlgorithm_comboBox.currentData(Qt.UserRole)

    def select_opti_algorithm_view_to_this(self, opti_alg):
        index_of_opti_alg = self.ui.optiAlgorithm_comboBox.findData(opti_alg, Qt.UserRole)
        if index_of_opti_alg == -1:
            raise Exception("Given optimization algorithm wasn't found on the list")
        self.ui.optiAlgorithm_comboBox.setCurrentIndex(index_of_opti_alg)

    @property
    def physical_dose_dist(self):
        return self.ui.physicalDoseDist_checkBox.isChecked()

    @physical_dose_dist.getter
    def physical_dose_dist(self):
        return self.ui.physicalDoseDist_checkBox.isChecked()

    @physical_dose_dist.setter
    def physical_dose_dist(self, state):
        self.ui.physicalDoseDist_checkBox.setChecked(state)

    @property
    def biological_dose_dist(self):
        return self.ui.biologicalDoseDist_checkBox.isChecked()

    @biological_dose_dist.getter
    def biological_dose_dist(self):
        return self.ui.biologicalDoseDist_checkBox.isChecked()

    @biological_dose_dist.setter
    def biological_dose_dist(self, state):
        self.ui.biologicalDoseDist_checkBox.setChecked(state)

    @property
    def dose_averaged_let(self):
        return self.ui.doseAveragedLET_checkBox.isChecked()

    @dose_averaged_let.getter
    def dose_averaged_let(self):
        return self.ui.doseAveragedLET_checkBox.isChecked()

    @dose_averaged_let.setter
    def dose_averaged_let(self, state):
        self.ui.doseAveragedLET_checkBox.setChecked(state)

    @property
    def raster_scan_file(self):
        return self.ui.rasterScanFile_checkBox.isChecked()

    @raster_scan_file.getter
    def raster_scan_file(self):
        return self.ui.rasterScanFile_checkBox.isChecked()

    @raster_scan_file.setter
    def raster_scan_file(self, state):
        self.ui.rasterScanFile_checkBox.setChecked(state)

    def set_unimplemented_fields_disabled(self):
        self.ui.incube_checkBox.setDisabled(True)
        self.ui.incube_comboBox.setDisabled(True)
        self.ui.targetTissue_label.setDisabled(True)
        self.ui.targetTissue_comboBox.setDisabled(True)
        self.ui.residialTissue_comboBox.setDisabled(True)
        self.ui.residialTissue_label.setDisabled(True)
        self.ui.beamsEyeDoseView_checkBox.setDisabled(True)
        self.ui.beamsEyeLETdViewcheckBox.setDisabled(True)
