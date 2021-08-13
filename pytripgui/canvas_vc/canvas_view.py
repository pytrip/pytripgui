import logging

from events import Events

from PyQt5.QtWidgets import QSizePolicy
from PyQt5 import QtCore

from pytripgui.canvas_vc.plotter.mpl_plotter import MplPlotter
from pytripgui.view.qt_gui import UiViewCanvas
from pytripgui.view.qt_view_adapter import ListWidget

logger = logging.getLogger(__name__)


class CanvasView:
    def __init__(self, parent=None):
        self.internal_events = Events(('on_perspective_change', 'on_display_filter_change', 'on_change_slice_position'))

        self._ui = UiViewCanvas(parent)
        self._plotter = MplPlotter()

        self.voi_list = ListWidget(self._ui.voi_listWidget, checkable=True)

        self._ui.vc_layout.addWidget(self._plotter)

        self._ui.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._ui.updateGeometry()

        self._internal_events_setup()
        self.vois_tree_set_enabled(True)

    def _internal_events_setup(self):

        self._ui.voiList_checkBox.stateChanged.connect(self.vois_tree_set_enabled)

        self._ui.perspective_comboBox.currentIndexChanged.connect(
            lambda index: self.internal_events.on_perspective_change())

        self._ui.Dose_radioButton.released.connect(self.internal_events.on_display_filter_change)
        self._ui.LET_radioButton.released.connect(self.internal_events.on_display_filter_change)
        self._ui.None_radioButton.released.connect(self.internal_events.on_display_filter_change)

    def widget(self):
        return self._ui

    def show(self):
        self._ui.show()

    def set_plotter_click_callback(self, fun):
        self._plotter.set_button_press_callback(fun)

    def set_plotter_wheel_callback(self, fun):
        self._plotter.set_scroll_event_callback(fun)

    @property
    def max_position(self):
        return self._ui.position_slider.maximum()

    @max_position.setter
    def max_position(self, max_position):
        self._ui.position_slider.setMaximum(max_position - 1)

    @property
    def position(self):
        return self._ui.position_slider.value()

    @position.setter
    def position(self, position):
        self._ui.position_slider.setValue(position)

    @property
    def perspective(self):
        return self._ui.perspective_comboBox.currentText()

    @perspective.setter
    def perspective(self, perspective):
        index_of_element = self._ui.perspective_comboBox.findText(perspective, QtCore.Qt.MatchFixedString)
        if index_of_element == -1:
            raise Exception("Cannot find given perspective to select")
        self._ui.perspective_comboBox.setCurrentIndex(index_of_element)

    @property
    def display_filter(self):
        if self._ui.Dose_radioButton.isChecked():
            return "DOS"
        if self._ui.LET_radioButton.isChecked():
            return "LET"
        return "None"

    @display_filter.setter
    def display_filter(self, display_filter):
        if display_filter == "DOS":
            self._ui.Dose_radioButton.setChecked(True)
        elif display_filter == "LET":
            self._ui.LET_radioButton.setChecked(True)
        else:
            self._ui.None_radioButton.setChecked(True)

    def enable_let(self):
        self._ui.LET_radioButton.setEnabled(True)

    def enable_dose(self):
        self._ui.Dose_radioButton.setEnabled(True)

    def reset_radiobuttons(self):
        self._ui.LET_radioButton.setEnabled(False)
        self._ui.Dose_radioButton.setEnabled(False)
        self._ui.None_radioButton.setChecked(True)

    def set_position_changed_callback(self, callback):
        self._ui.position_slider.sliderMoved.connect(callback)

    def plot_let(self, data):
        self._plotter.plot_let(data)

    def plot_dos(self, data):
        self._plotter.plot_dos(data)

    def plot_ctx(self, data):
        self._plotter.plot_ctx(data)
        self._enable_perspective_selector()

    def draw(self):
        self._plotter.draw()

    def update(self):
        self._plotter.update()

    def clear(self):
        self._plotter.remove_dos()
        self._plotter.remove_let()
        self._plotter.remove_ctx()

    def _enable_perspective_selector(self):
        self._ui.perspective_comboBox.setEnabled(True)

    def vois_tree_set_enabled(self, state):
        if state:
            self._ui.voi_listWidget.show()
            self._ui.voiList_checkBox.setCheckState(QtCore.Qt.Checked)
        else:
            self._ui.voi_listWidget.hide()
            self._ui.voiList_checkBox.setCheckState(QtCore.Qt.Unchecked)
