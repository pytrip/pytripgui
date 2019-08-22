from PyQt5 import QtWidgets, uic

from pytrip.tripexecuter import KernelModel
from pytrip.tripexecuter import Projectile

import logging
logger = logging.getLogger(__name__)


class UiKernelDialog(QtWidgets.QDialog):
    def __init__(self):
        super(UiKernelDialog, self).__init__()
        uic.loadUi('../pytripgui/view/kernel.ui', self)


class KernelController(object):
    """
    """

    def __init__(self, model, settings):
        """
        """
        self.model = model
        self.settings = settings
        self.current_kernel_idx = -1
        self.current_kernel = None
        self._kcounter = 0  # internal counter for new kernels
        self._kernel_changed = False  # hack to avoid messy signal firing

        self.edit()

    def edit(self):
        """
        Edits the kernels
        """
        logger.debug("edit_kernel()")

        # open the plan configuration dialog
        # https://stackoverflow.com/questions/42505429/pyqt5-gui-structure-advice-needed
        self.ui = UiKernelDialog()

        self._populate_kernel_ui()
        self._setup_kernel_callbacks()

        self.ui.exec_()
        self.ui.show()

    def delete_kernel(self):
        """
        Deletes a kernel from the model.
        """
        logger.debug("edit_kernel()")

    def _populate_kernel_ui(self):
        """
        Fill all widgets with current model data.
        """
        logger.debug("----------------------------------------------------")
        logger.debug("_populate_kernel_ui()")

        model = self.model
        ui = self.ui

        # import export currently disabled
        ui.pushButton_3.setEnabled(False)
        ui.pushButton_4.setEnabled(False)

        # Handle Projectiles
        ui.comboBox.clear()  # list of projectiles
        projs = Projectile._projectile_defaults
        for proj in projs:
            ui.comboBox.addItem(proj)

        # If there are no kernels present: start by adding an empty kernel
        if not model.kernels:
            self._new()

        self.current_kernel = model.kernels[0]

        ui.comboBox_5.clear()  # list of kernels
        for kernel in model.kernels:
            logger.debug("_populate_kernel_ui() kernels: {}".format(kernel.name))
            ui.comboBox_5.addItem(kernel.name, kernel)

        self.current_kernel = model.kernels[0]

        self._show_kernel(self.current_kernel)

        ui.plainTextEdit.setFocus()

    def _show_kernel(self, kernel):
        """
        Update all widgets for a given kernel to be shown.
        """
        logger.debug("----------------------------------------------------")
        logger.debug("KernelCrontroller._show_kernel() '{}'".format(kernel.name))

        ui = self.ui

        ui.plainTextEdit.setPlainText(kernel.comment)

        ui.lineEdit.setText(kernel.projectile.name)
        _i = ui.comboBox.findText(kernel.projectile.iupac)
        if _i == -1:  # not found
            logger.warning("_show_kernel() FIXME")
        else:
            ui.comboBox.setCurrentIndex(_i)

        ui.spinBox.setValue(kernel.projectile.z)
        ui.spinBox_2.setValue(kernel.projectile.a)

        if kernel.rifi_thickness:
            ui.checkBox.setChecked(True)
            ui.lineEdit_6.setText(kernel.rifi_name)
            ui.doubleSpinBox.setValue(float(kernel.rifi_thickness))  # TODO: pytrip should have it as float, not str.
            ui.lineEdit_6.setEnabled(True)
            ui.doubleSpinBox.setEnabled(True)
        else:
            ui.checkBox.setChecked(False)
            ui.lineEdit_6.setEnabled(False)
            ui.doubleSpinBox.setEnabled(False)

        ui.lineEdit_8.setText(kernel.ddd_path)
        ui.lineEdit_9.setText(kernel.spc_path)
        ui.lineEdit_10.setText(kernel.sis_path)

    def _setup_kernel_callbacks(self):
        """
        Connect all widgets to model.
        """
        ui = self.ui

        ui.comboBox_5.currentIndexChanged.connect(self._change_kernel)
        ui.comboBox_5.lineEdit().textEdited.connect(self._kernel_name_changed)
        # ui.comboBox_5.editTextChanged.connect(self._kernel_name_changed)
        ui.pushButton.clicked.connect(self._new)
        ui.pushButton_2.clicked.connect(self._remove)
        ui.pushButton_3.clicked.connect(self._import)
        ui.pushButton_4.clicked.connect(self._export)
        ui.pushButton_5.clicked.connect(self._save)

        # comment box
        ui.plainTextEdit.textChanged.connect(self._comment_changed)

        # projectile
        ui.lineEdit.textEdited.connect(self._projectile_name_changed)
        ui.comboBox.currentIndexChanged.connect(self._projectile_symbol_changed)

        # RiFi stuff
        ui.checkBox.toggled.connect(self._rifi_toggled)
        ui.lineEdit_6.textEdited.connect(self._rifi_name_changed)
        ui.doubleSpinBox.valueChanged.connect(self._rifi_thickness_changed)

        # paths
        ui.lineEdit_8.textEdited.connect(self._ddd_changed)
        ui.lineEdit_9.textEdited.connect(self._spc_changed)
        ui.lineEdit_10.textEdited.connect(self._sis_changed)

    def _save(self):
        """
        """
        logger.debug("KernelController._save()")
        self.settings.save()

    def _new(self):
        """
        Append a new kernel to model.kernels[]
        """
        logger.debug("----------------------------------------------------")
        logger.debug("KernelController._new()")
        model = self.model
        ui = self.ui

        self._kcounter += 1
        _str = "New kernel ({:d})".format(self._kcounter)  # default string for new kenrel

        model.kernels.append(KernelModel(name=_str))
        self.current_kernel = model.kernels[-1]
        kernel = self.current_kernel
        self.current_kernel_idx = model.kernels.index(self.current_kernel)
        self.current_kernel.projectile = Projectile("H", a=1)

        ui.comboBox_5.addItem(kernel.name, kernel)
        # combobox should point to next item
        _last = ui.comboBox_5.count() - 1
        ui.comboBox_5.setCurrentIndex(_last)

        # set focus to editable name, to encourage user to enter a new name.
        ui.comboBox_5.lineEdit().setFocus()
        ui.comboBox_5.lineEdit().selectAll()

    def _remove(self):
        """
        """
        logger.debug("----------------------------------------------------")
        logger.debug("KernelController._remove()")
        model = self.model
        ui = self.ui
        kernel = self.current_kernel

        if kernel in model.kernels:
            model.kernels.remove(kernel)
            i = ui.comboBox_5.currentIndex()  # hope current kernel is in sync with currentIndex. Not too robust this.
            ui.comboBox_5.removeItem(i)
            if model.kernels:
                self.current_kernel = model.kernels[-1]
            else:
                # if there are no more kernels in model.kernels, point to a fresh new one.
                self._new()

    def _import(self):
        """
        """
        logger.debug("KernelController._import()")
        logger.warning("KernelController._import() - not implemented")

    def _export(self):
        """
        """
        logger.debug("KernelController._export()")
        logger.warning("KernelController._export() - not implemented")

    def _kernel_name_changed(self):
        """
        """
        logger.debug("----------------------------------------------------")
        logger.debug("KernelController._kernel_name_changed()")
        model = self.model
        ui = self.ui

        # if this signal was called because kernel was changed, do not update any models
        if self._kernel_changed:
            self._kernel_changed = False
            return

        i = ui.comboBox_5.currentIndex()
        kernel = model.kernels[i]

        # Get the text which is entered into the comboBox line edit:
        _txt = ui.comboBox_5.lineEdit().text()
        model.kernels[i].name = _txt  # this should also update model.kernel[].name as they are linked

        # reset the data in the Combobox model
        ui.comboBox_5.setItemText(i, kernel.name)
        ui.comboBox_5.setItemData(i, kernel)

        # ui.comboBox_5.clear()  # list of kernels
        # for kernel in model.kernels:
        #     ui.comboBox_5.addItem(kernel.name, kernel)
        # ui.comboBox_5.setCurrentIndex(i)

    def _comment_changed(self):
        """
        """
        logger.debug("----------------------------------------------------")
        logger.debug("KernelController._comment_changed()")
        ui = self.ui
        kernel = self.current_kernel

        kernel.comment = ui.plainTextEdit.toPlainText()

    def _ddd_changed(self):
        """
        """
        logger.debug("KernelController._ddd_changed()")
        ui = self.ui

        self.current_kernel.ddd_path = ui.lineEdit_8.text()

    def _projectile_name_changed(self):
        """
        """
        logger.debug("KernelController._projectile_name_changed")
        ui = self.ui
        kernel = self.current_kernel
        kernel.projectile.name = ui.lineEdit.text()

    def _projectile_symbol_changed(self):
        """
        """
        logger.debug("KernelController._projectile_symbol_changed")
        ui = self.ui
        kernel = self.current_kernel

        i = ui.comboBox.currentIndex()
        if i > -1:
            iupac = ui.comboBox.itemText(i)
            kernel.projectile.iupac = iupac
            _z = Projectile._projectile_defaults[iupac][0]  # extract z from default list
            _a = Projectile._projectile_defaults[iupac][1]  # extract A from default list
            logger.debug("Set projectile: iupac, z, a: {} {} {}".format(iupac, _z, _a))

            kernel.projectile.z = _z
            kernel.projectile.a = _a

            ui.spinBox.setValue(_z)
            ui.spinBox_2.setValue(_a)

    def _rifi_toggled(self):
        """
        """
        logger.debug("KernelController._rifi_toggled")
        ui = self.ui

        if ui.checkBox.isChecked():
            ui.lineEdit_6.setEnabled(True)
            ui.doubleSpinBox.setEnabled(True)
        else:
            ui.lineEdit_6.setEnabled(False)
            ui.doubleSpinBox.setEnabled(False)

    def _rifi_name_changed(self):
        """
        """
        logger.debug("KernelController._rifi_name_changed")
        ui = self.ui
        kernel = self.current_kernel
        kernel.rifi_name = ui.lineEdit_6.text()

    def _rifi_thickness_changed(self):
        """
        """
        logger.debug("KernelController._rifi_thickness_changed")
        ui = self.ui
        kernel = self.current_kernel
        kernel.rifi_thickness = str(ui.doubleSpinBox.value())  # TODO: change this to a float

    def _spc_changed(self):
        """
        """
        logger.debug("KernelController._spc_changed()")
        ui = self.ui
        self.current_kernel.spc_path = ui.lineEdit_9.text()

    def _sis_changed(self):
        """
        """
        logger.debug("KernelController._sis_changed()")
        ui = self.ui
        self.current_kernel.sis_path = ui.lineEdit_10.text()

    def _change_kernel(self):
        """
        :params str attribute_name: attribute in pytrip.kernel object.
        """
        logger.debug("----------------------------------------------------")
        logger.debug("KernelController._change_kernel()")

        self._kernel_changed = True
        model = self.model
        ui = self.ui

        i = ui.comboBox_5.currentIndex()
        if i > -1:
            self.current_kernel = model.kernels[i]
            self.current_kernel_idx = i
            self._show_kernel(self.current_kernel)

        ui.plainTextEdit.setFocus()
