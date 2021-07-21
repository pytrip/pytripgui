from pytripgui.field_vc.angles_standard import AnglesStandard
from pytripgui.view.qt_gui import UiFieldDialog

import logging

logger = logging.getLogger(__name__)


class FieldQtView:
    def __init__(self, parent=None):
        self.ui = UiFieldDialog(parent)

        self._setup_internal_callbacks()

    def show(self):
        self.ui.show()
        self.ui.exec_()

    def exit(self):
        self.ui.close()

    def set_ok_callback(self, fun):
        self.ui.accept_ButtonBox.accepted.connect(fun)

    def set_cancel_callback(self, fun):
        self.ui.accept_ButtonBox.rejected.connect(fun)

    def set_gui_needs_update_callback(self, fun):
        self.ui.anglesStandardIEC_radio.toggled.connect(fun)

    def _setup_internal_callbacks(self):
        self.ui.manualIsocenter_checkBox.stateChanged.connect(self._isocenter_checkbox_callback)
        self.ui.gantry_pushButton_p90.clicked.connect(self._gantry_p90)  # +90 deg
        self.ui.gantry_pushButton_m90.clicked.connect(self._gantry_m90)  # -90 deg
        self.ui.couch_pushButton_p90.clicked.connect(self._couch_p90)  # +90 deg
        self.ui.couch_pushButton_m90.clicked.connect(self._couch_m90)  # -90 deg

    def _isocenter_checkbox_callback(self):
        checkbox_state = self.ui.manualIsocenter_checkBox.checkState()
        self.set_isocenter_state(checkbox_state)

    @property
    def angles_standard(self):
        checked_button = self.ui.anglesStandardGroup.checkedButton()
        if checked_button == self.ui.anglesStandardTRiP_radio:
            return AnglesStandard.TRIP
        if checked_button == self.ui.anglesStandardIEC_radio:
            return AnglesStandard.IEC
        return None

    @angles_standard.setter
    def angles_standard(self, angles_standard):
        if angles_standard == AnglesStandard.TRIP:
            self.ui.anglesStandardTRiP_radio.setChecked(True)
        elif angles_standard == AnglesStandard.IEC:
            self.ui.anglesStandardIEC_radio.setChecked(True)

    def _gantry_p90(self):
        self.gantry_angle += 90.0

    def _gantry_m90(self):
        self.gantry_angle -= 90.0

    def _couch_p90(self):
        self.couch_angle += 90.0

    def _couch_m90(self):
        self.couch_angle -= 90.0

    @property
    def gantry_angle(self):
        return self.ui.gantry_doubleSpinBox.value()

    @gantry_angle.getter
    def gantry_angle(self):
        return self.ui.gantry_doubleSpinBox.value()

    @gantry_angle.setter
    def gantry_angle(self, gantry_angle):
        self.ui.gantry_doubleSpinBox.setValue(gantry_angle)

    @property
    def couch_angle(self):
        return self.ui.couch_doubleSpinBox.value()

    @couch_angle.getter
    def couch_angle(self):
        return self.ui.couch_doubleSpinBox.value()

    @couch_angle.setter
    def couch_angle(self, gantry_angle):
        self.ui.couch_doubleSpinBox.setValue(gantry_angle)

    def is_isocenter_manually(self):
        return self.ui.manualIsocenter_checkBox.isChecked()

    def get_isocenter_value(self):
        isocenter = [
            self.ui.isocenterX_doubleSpinBox.value(),
            self.ui.isocenterY_doubleSpinBox.value(),
            self.ui.isocenterZ_doubleSpinBox.value()
        ]
        return isocenter

    def set_isocenter_state(self, state):
        self.ui.manualIsocenter_checkBox.setChecked(state)
        self.ui.isocenterX_doubleSpinBox.setEnabled(state)
        self.ui.isocenterY_doubleSpinBox.setEnabled(state)
        self.ui.isocenterZ_doubleSpinBox.setEnabled(state)

    def set_isocenter_values(self, isocenter):
        self.ui.isocenterX_doubleSpinBox.setValue(isocenter[0])
        self.ui.isocenterY_doubleSpinBox.setValue(isocenter[1])
        self.ui.isocenterZ_doubleSpinBox.setValue(isocenter[2])

    @property
    def spot_size(self):
        return self.ui.spotSize_doubleSpinBox.value()

    @spot_size.getter
    def spot_size(self):
        return self.ui.spotSize_doubleSpinBox.value()

    @spot_size.setter
    def spot_size(self, spot_size):
        self.ui.spotSize_doubleSpinBox.setValue(spot_size)

    @property
    def raster_step(self):
        raster_step = [self.ui.rasterSpaceX_doubleSpinBox.value(), self.ui.rasterSpaceY_doubleSpinBox.value()]
        return raster_step

    @raster_step.getter
    def raster_step(self):
        raster_step = [self.ui.rasterSpaceX_doubleSpinBox.value(), self.ui.rasterSpaceY_doubleSpinBox.value()]
        return raster_step

    @raster_step.setter
    def raster_step(self, raster_step):
        self.ui.rasterSpaceX_doubleSpinBox.setValue(raster_step[0])
        self.ui.rasterSpaceY_doubleSpinBox.setValue(raster_step[1])

    @property
    def dose_extension(self):
        return self.ui.doseext_doubleSpinBox.value()

    @dose_extension.getter
    def dose_extension(self):
        return self.ui.doseext_doubleSpinBox.value()

    @dose_extension.setter
    def dose_extension(self, dose_extension):
        self.ui.doseext_doubleSpinBox.setValue(dose_extension)

    @property
    def contour_extension(self):
        return self.ui.contourext_doubleSpinBox.value()

    @contour_extension.getter
    def contour_extension(self):
        return self.ui.contourext_doubleSpinBox.value()

    @contour_extension.setter
    def contour_extension(self, contour_extension):
        self.ui.contourext_doubleSpinBox.setValue(contour_extension)

    @property
    def depth_steps(self):
        return self.ui.depthStep_doubleSpinBox.value()

    @depth_steps.getter
    def depth_steps(self):
        return self.ui.depthStep_doubleSpinBox.value()

    @depth_steps.setter
    def depth_steps(self, zsteps):
        self.ui.depthStep_doubleSpinBox.setValue(zsteps)
