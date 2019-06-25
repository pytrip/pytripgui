from PyQt5 import QtWidgets
from pytripgui.view.gen.field import Ui_FieldDialog

import logging
logger = logging.getLogger(__name__)


class FieldQtView(object):
    """
    """
    def __init__(self):
        self.ui = Ui_FieldDialog()
        self.widget = QtWidgets.QWidget()

        self.ui.setupUi(self.widget)
        self._setup_callbacks()

    def _setup_callbacks(self):
        ui = self.ui
        ui.manualIsocenter_checkBox.stateChanged.connect(self.isocenter_checkbox_callback)
        ui.gantry_pushButton_p90.clicked.connect(self._gantry_p90)  # +90 deg
        ui.gantry_pushButton_m90.clicked.connect(self._gantry_m90)  # -90 deg
        ui.couch_pushButton_p90.clicked.connect(self._couch_p90)  # +90 deg
        ui.couch_pushButton_m90.clicked.connect(self._couch_m90)  # -90 deg

    def isocenter_checkbox_callback(self):
        ui = self.ui
        checkboxState = ui.manualIsocenter_checkBox.checkState()
        self.set_isocenter_state(checkboxState)

    def _gantry_p90(self):
        new_gantry_angle = self.get_gantry_angle_value() + 90.0
        self.set_gantry_angle_value(new_gantry_angle)

    def _gantry_m90(self):
        new_gantry_angle = self.get_gantry_angle_value() - 90.0
        self.set_gantry_angle_value(new_gantry_angle)

    def _couch_p90(self):
        new_couch_angle = self.get_couch_angle_value() + 90.0
        self.set_couch_angle_value(new_couch_angle)

    def _couch_m90(self):
        new_couch_angle = self.get_couch_angle_value() - 90.0
        self.set_couch_angle_value(new_couch_angle)

    def get_gantry_angle_value(self):
        return self.ui.gantry_doubleSpinBox.value()

    def set_gantry_angle_value(self, gantry_angle):
        self.ui.gantry_doubleSpinBox.setValue(gantry_angle)

    def get_couch_angle_value(self):
        return self.ui.couch_doubleSpinBox.value()

    def set_couch_angle_value(self, gantry_angle):
        self.ui.couch_doubleSpinBox.setValue(gantry_angle)

    def set_isocenter_state(self, state):
        ui = self.ui
        ui.manualIsocenter_checkBox.setChecked(state)
        ui.isocenterX_doubleSpinBox.setEnabled(state)
        ui.isocenterY_doubleSpinBox.setEnabled(state)
        ui.isocenterZ_doubleSpinBox.setEnabled(state)

    def set_isocenter_values(self, isocenter):
        ui = self.ui
        ui.isocenterX_doubleSpinBox.setValue(isocenter[0])
        ui.isocenterY_doubleSpinBox.setValue(isocenter[1])
        ui.isocenterZ_doubleSpinBox.setValue(isocenter[2])

    def set_spot_size_value(self, spot_size):
        self.ui.spotSize_doubleSpinBox.setValue(spot_size)

    def set_raster_step_value(self, raster_step):
        self.ui.rasterSpaceX_doubleSpinBox.setValue(raster_step[0])
        self.ui.rasterSpaceY_doubleSpinBox.setValue(raster_step[1])

    def set_dose_extension_value(self, dose_extension):
        self.ui.doseext_doubleSpinBox.setValue(dose_extension)

    def set_contour_extension_value(self, contour_extension):
        self.ui.contourext_doubleSpinBox.setValue(contour_extension)

    def set_depth_steps_value(self, zsteps):
        self.ui.depthStep_doubleSpinBox.setValue(zsteps)

    def show(self):
        self.widget.show()
