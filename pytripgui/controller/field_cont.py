import logging

from PyQt5 import QtWidgets

from pytrip.tripexecuter import Field

from pytripgui.view.gen.field import Ui_FieldDialog

logger = logging.getLogger(__name__)


class FieldController(object):
    """
    """
    def __init__(self, model):
        self.model = model

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
        self.ui = ui
        self.field = field

        self._set_form_from_model()
        self._setup_field_callbacks()

        dialog.exec_()
        dialog.show()

        return field

    def _populate_field_ui(self):
        """
        Fill all widgets with current model data.
        """
        logger.debug("_populate_field_ui()")

    def _setup_field_callbacks(self):
        """
        Connect all widgets to model.
        """
        ui = self.ui

        # isocenter
        ui.isocenterX_doubleSpinBox.valueChanged.connect(self._form_changed)
        ui.isocenterY_doubleSpinBox.valueChanged.connect(self._form_changed)
        ui.isocenterZ_doubleSpinBox.valueChanged.connect(self._form_changed)

        # gantry
        ui.gantry_doubleSpinBox.valueChanged.connect(self._form_changed)
        ui.gantry_pushButton_p90.clicked.connect(self._gantry_p90)  # +90 deg
        ui.gantry_pushButton_m90.clicked.connect(self._gantry_m90)  # -90 deg

        # couch
        ui.couch_doubleSpinBox.valueChanged.connect(self._form_changed)
        ui.couch_pushButton_p90.clicked.connect(self._couch_p90)  # +90 deg
        ui.couch_pushButton_m90.clicked.connect(self._couch_m90)  # -90 deg

        # spot size
        ui.spotSize_doubleSpinBox.valueChanged.connect(self._form_changed)

        # raster spacing
        ui.rasterSpaceX_doubleSpinBox.valueChanged.connect(self._form_changed)
        ui.rasterSpaceY_doubleSpinBox.valueChanged.connect(self._form_changed)

        # dose and contour ext, depth steps:
        ui.doseext_doubleSpinBox.valueChanged.connect(self._form_changed)
        ui.contourext_doubleSpinBox.valueChanged.connect(self._form_changed)
        ui.depthStep_doubleSpinBox.valueChanged.connect(self._form_changed)

    def _set_form_from_model(self):
        """
        Loads a field, and sets the form according to what is in the field model.
        """

        ui = self.ui
        field = self.field

        if field.isocenter:
            ui.manualIsocenter_checkBox.setChecked(True)
            ui.isocenterX_doubleSpinBox.setEnabled(True)
            ui.isocenterY_doubleSpinBox.setEnabled(True)
            ui.isocenterZ_doubleSpinBox.setEnabled(True)
            ui.isocenterX_doubleSpinBox.setValue(field.isocenter[0])
            ui.isocenterY_doubleSpinBox.setValue(field.isocenter[1])
            ui.isocenterZ_doubleSpinBox.setValue(field.isocenter[2])
        else:
            ui.manualIsocenter_checkBox.setChecked(False)
            ui.isocenterX_doubleSpinBox.setEnabled(False)
            ui.isocenterY_doubleSpinBox.setEnabled(False)
            ui.isocenterZ_doubleSpinBox.setEnabled(False)

        ui.gantry_doubleSpinBox.setValue(field.gantry)
        ui.couch_doubleSpinBox.setValue(field.couch)

        ui.spotSize_doubleSpinBox.setValue(field.fwhm)
        ui.rasterSpaceX_doubleSpinBox.setValue(field.raster_step[0])
        ui.rasterSpaceY_doubleSpinBox.setValue(field.raster_step[1])
        ui.doseext_doubleSpinBox.setValue(field.dose_extension)
        ui.contourext_doubleSpinBox.setValue(field.contour_extension)
        ui.depthStep_doubleSpinBox.setValue(field.zsteps)

        for kernel in self.model.kernels:
            ui.kernel_comboBox.addItem(kernel.name, kernel)

        for kernel in self.model.kernels:
            ui.comboBox.addItem(kernel.name, kernel)

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

        if ui.manualIsocenter_checkBox.isChecked():
            field.isocenter = [ui.isocenterX_doubleSpinBox.value(),
                               ui.isocenterY_doubleSpinBox.value(),
                               ui.isocenterZ_doubleSpinBox.value()]
        else:
            field.isocenter = None

        field.gantry = ui.gantry_doubleSpinBox.value()
        field.couch = ui.couch_doubleSpinBox.value()
        field.fwhm = ui.spotSize_doubleSpinBox.value()
        field.raster_step = [ui.rasterSpaceX_doubleSpinBox.value(), ui.rasterSpaceY_doubleSpinBox.value()]
        field.dose_extension = ui.doseext_doubleSpinBox.value()
        field.contour_extension = ui.contourext_doubleSpinBox.value()
        field.zsteps = ui.depthStep_doubleSpinBox.value()

    def _gantry_p90(self):
        self.field.gantry = self.field.gantry + 90.0

        self._set_form_from_model()

    def _gantry_m90(self):
        self.field.gantry = self.field.gantry - 90.0

        self._set_form_from_model()

    def _couch_p90(self):
        self.field.couch = self.field.couch + 90.0

        self._set_form_from_model()

    def _couch_m90(self):
        self.field.couch = self.field.couch - 90.0

        self._set_form_from_model()
