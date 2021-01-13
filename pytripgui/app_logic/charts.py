from pytripgui.view.chart_widget import ChartWidget

from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt


class Charts:
    def __init__(self, parent_gui):
        self._parent_gui = parent_gui

        self._charts = []
        self._dock_widgets = []

    def set_simulation_result(self, simulation_result):
        self._charts = []

        for histogram_name in simulation_result.volume_histograms:
            widget = ChartWidget()
            widget.title = histogram_name

            histogram = simulation_result.volume_histograms[histogram_name]
            for name, value in histogram.items():
                widget.add_series(value.x, value.y, name)

            self._charts.append(widget)

        self._show()

    def _show(self):
        self._close_all()
        self._dock_widgets = []

        for chart in self._charts:
            widget = QDockWidget()
            widget.setWidget(chart.view)
            self._parent_gui.ui.addDockWidget(Qt.RightDockWidgetArea, widget)
            self._dock_widgets.append(widget)

    def _close_all(self):
        for _dock_widget in self._dock_widgets:
            _dock_widget.close()
