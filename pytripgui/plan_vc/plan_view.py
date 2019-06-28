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
