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
        self.internal_events = Events(('on_perspective_change', 'on_change_slice_position'))

        self._ui = UiViewCanvas(parent)
        self._plotter = MplPlotter()

        self.voi_list = ListWidget(self._ui.voi_listWidget, checkable=True)

        self._ui.vc_layout.addWidget(self._plotter)

        self._ui.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._ui.updateGeometry()

        self._internal_events_setup()
        self.voi_list_set_visibility(visible=True)

        # "If tracking is disabled, the slider emits the valueChanged() signal only when the user releases the slider."
        self._ui.position_slider.setTracking(False)

    def _internal_events_setup(self):

        self._ui.voiList_checkBox.stateChanged.connect(self.voi_list_set_visibility)

        self._ui.perspective_comboBox.currentIndexChanged.connect(
            lambda index: self.internal_events.on_perspective_change())

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

    def set_position_changed_callback(self, callback):
        # event is emitted every time value od slider is changed, for example:
        #   when slider value is set by controller
        #   when user scrolls slider
        #   when user stops dragging slider - thanks to disabled tracking
        self._ui.position_slider.valueChanged.connect(callback)

    def remove_position_changed_callback(self, callback):
        self._ui.position_slider.valueChanged.disconnect(callback)

    def plot_let(self, data):
        self._plotter.plot_let(data)

    def plot_dos(self, data):
        self._plotter.plot_dos(data)

    def plot_ctx(self, data):
        self._plotter.plot_ctx(data)
        self._enable_perspective_selector()

    def plot_voi(self, vdx):
        self._plotter.plot_voi(vdx)

    def draw(self):
        self._plotter.draw()

    def update(self):
        self._plotter.update()

    def clear(self):
        self._plotter.remove_voi()
        self._plotter.remove_dos()
        self._plotter.remove_let()
        self._plotter.remove_ctx()

    def _enable_perspective_selector(self):
        self._ui.perspective_comboBox.setEnabled(True)

    def voi_list_set_visibility(self, visible: bool = True) -> None:
        """
        Method that handles displaying and hiding the VOI list.

        Parameters:
        visible(bool): Whether the list should be shown.
        """
        if visible:
            self._ui.voi_listWidget.show()
            self._ui.voiList_checkBox.setCheckState(QtCore.Qt.Checked)
        else:
            self._ui.voi_listWidget.hide()
            self._ui.voiList_checkBox.setCheckState(QtCore.Qt.Unchecked)

    def voi_list_empty(self, empty: bool = True) -> None:
        """
        Method that handles displaying and hiding the VOI list and its checkBox when VOI data is unavailable.

        Parameters:
        empty(bool): Whether the list is empty and should be hidden.
        """
        voi_list = self._ui.voi_listWidget
        checkbox = self._ui.voiList_checkBox

        if empty:
            voi_list.hide()
            checkbox.hide()
        else:
            checkbox.show()
            if checkbox.isChecked():
                voi_list.show()
            else:
                voi_list.hide()
