import logging

from PyQt5 import QtWidgets
# from PyQt5.QtCore import Qt

from pytrip.tripexecuter import Field

from pytripgui.view.gen.field import Ui_FieldDialog

logger = logging.getLogger(__name__)


class FieldController(object):
    """
    """

    def __init__(self, model, settings):
        pass

    def edit(self, field=None):
        """
        Edits a field.

        :param field: An instance of a pytrip.tripexecuter.Field object. If None, then a new field is created.
        :returns: a link to the field object which was edited.
        """
        logger.debug("FieldController.edit()")

        # open the plan configuration dialog
        # https://stackoverflow.com/questions/42505429/pyqt5-gui-structure-advice-needed
        dialog = QtWidgets.QDialog()
        ui = Ui_FieldDialog()

        if not field:
            field = Field()

        ui.setupUi(dialog)

        self._set_form_from_model()
        self._setup_field_callbacks(ui, field)

        dialog.exec_()
        dialog.show()

        self.ui = ui
        self.field = field

        return field

    def _populate_field_ui(self):
        """
        Fill all widgets with current model data.
        """
        logger.debug("_populate_field_ui()")

    def _setup_kernel_callbacks(self):
        """
        Connect all widgets to model.
        """
        ui = self.ui

        # isocenter
        ui.doubleSpinBox.valueChanged.connect(self._form_changed)
        ui.doubleSpinBox_2.valueChanged.connect(self._form_changed)
        ui.doubleSpinBox_3.valueChanged.connect(self._form_changed)

        # gantry
        ui.doubleSpinBox_4.valueChanged.connect(self._form_changed)
        ui.pushButton_3.clicked.connect(self._gantry_p90)  # +90 deg
        ui.pushButton_4.clicked.connect(self._gantry_m90)  # -90 deg

        # couch
        ui.doubleSpinBox_5.valueChanged.connect(self._form_changed)
        ui.pushButton.clicked.connect(self._couch_p90)  # +90 deg
        ui.pushButton_2.clicked.connect(self._couch_m90)  # -90 deg

        # spot size
        ui.doubleSpinBox_6.valueChanged.connect(self._form_changed)

        # raster spacing
        ui.doubleSpinBox_7.valueChanged.connect(self._form_changed)
        ui.doubleSpinBox_8.valueChanged.connect(self._form_changed)

        # dose and contour ext, depth steps:
        ui.doubleSpinBox_9.valueChanged.connect(self._form_changed)
        ui.doubleSpinBox_10.valueChanged.connect(self._form_changed)
        ui.doubleSpinBox_11.valueChanged.connect(self._form_changed)

    def set_form_from_model(self):
        """
        Loads a field, and sets the form according to what is in the field model.
        """

        ui = self.ui
        field = self.field

        if field.isocenter:
            ui.checkBox.setChecked(True)
            ui.doubleSpinBox.setEnabled(True)
            ui.doubleSpinBox_2.setEnabled(True)
            ui.doubleSpinBox_3.setEnabled(True)
            ui.doubleSpinBox.setValue(field.isocenter[0])
            ui.doubleSpinBox_2.setValue(field.isocenter[1])
            ui.doubleSpinBox_3.setValue(field.isocenter[2])
        else:
            ui.checkBox.setChecked(False)
            ui.doubleSpinBox.setEnabled(False)
            ui.doubleSpinBox_2.setEnabled(False)
            ui.doubleSpinBox_3.setEnabled(False)

        ui.doubleSpinBox_4.setValue(field.gantry)
        ui.doubleSpinBox_5.setValue(field.couch)

        ui.doubleSpinBox_6.setValue(field.fwhm)
        ui.doubleSpinBox_7.setValue(field.raster_step[0])
        ui.doubleSpinBox_8.setValue(field.raster_step[1])
        ui.doubleSpinBox_9.setValue(field.dose_extension)
        ui.doubleSpinBox_10.setValue(field.contour_extension)
        ui.doubleSpinBox_11.setValue(field.zsteps)

    def _form_changed(self):
        """
        What to do if the form was changed.
        """

        self._set_model_from_form()

    def _set_model_from_form(self):
        """
        Read all entries in the form and fill in the values in the field model.
        """

        ui = self.ui
        field = self.field

        field.rifi_name = ui.lineEdit_6.text()

        if ui.checkBox.isChecked():
            field.isocenter = [ui.doubleSpinBox.value(),
                               ui.doubleSpinBox_2.value(),
                               ui.doubleSpinBox_3.value()]
        else:
            field.isocenter = None

        field.gantry = ui.doubleSpinBox_4.value()
        field.couch = ui.doubleSpinBox_5.value()
        field.fwhm = ui.doubleSpinBox_6.value()
        field.raster_step = [ui.doubleSpinBox_7.value(), ui.doubleSpinBox_8.value()]
        field.dose_extension = ui.doubleSpinBox_9.value()
        field.contour_extension = ui.doubleSpinBox_10.value()
        field.zsteps = ui.doubleSpinBox_11.value()
