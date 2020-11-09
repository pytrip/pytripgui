import numpy as np

from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ChartWidget:
    def __init__(self):
        self.model = QChart()
        self.view = QChartView()

        self.view.setChart(self.model)

        self.model.legend().setAlignment(Qt.AlignBottom)
        self.view.setRenderHint(QPainter.Antialiasing)

    def show(self):
        self.view.show()

    def exit(self):
        self.view.close()

    @property
    def title(self):
        return self.model.title()

    @title.setter
    def title(self, title):
        self.model.setTitle(title)

    def add_series(self, x, y, name):
        series = QLineSeries()
        series.setName(name)

        let_chart = np.vstack((x, y)).T

        for x, y in let_chart:
            series.append(x, y)

        self.model.addSeries(series)
        self.model.createDefaultAxes()

        # axis = QValueAxis()
        # axis.setTitleText("Dose")
        #
        # self.model.setAxisX(axis, series)
        # self.model.axisY(series).setTitleText("Dose")
