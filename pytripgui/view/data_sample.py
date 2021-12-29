import math
from enum import Enum
from pathlib import Path
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from numpy import ndarray

from PyQt5 import QtWidgets, uic

from pytrip import CtxCube
from pytripgui.view.qt_gui import UiMainWindow


class DataSample(QtWidgets.QWidget):
    def __init__(self, parent: UiMainWindow, axes: Axes):
        super().__init__(parent)
        ui_path = Path(Path(__file__).parent, "data_sample.ui").resolve()
        uic.loadUi(ui_path, self)

        self.axes: Axes = axes

        self.mode: DataSample.Mode = self.Mode.ctx
        self.perspective: DataSample.Perspective = self.Perspective.transversal
        self.data: ndarray = ndarray(shape=())
        self.cube: CtxCube = CtxCube()
        self.x_offset: float = 0
        self.y_offset: float = 0
        self.z_offset: float = 0
        self.slice_no: int = 0

        self.position_widget.hide()
        self.doselet_widget.hide()

    def update_perspective(self, perspective_name: str) -> None:
        self.perspective = self.Perspective(perspective_name)

        if self.perspective == self.Perspective.transversal:
            self.x_offset = self.cube.xoffset
            self.y_offset = self.cube.yoffset
        elif self.perspective == self.Perspective.sagittal:
            self.x_offset = self.cube.yoffset
            self.y_offset = self.cube.zoffset
        else:
            self.x_offset = self.cube.xoffset
            self.y_offset = self.cube.zoffset

    def update_sample(self, event: MouseEvent) -> None:
        if event.xdata and event.inaxes == self.axes:
            self.update_position(event.xdata, event.ydata)
            self.position_widget.show()

            if self.mode != self.Mode.ctx:
                self.update_doselet(event.xdata, event.ydata)
                self.doselet_widget.show()
        else:
            self.position_widget.hide()
            self.doselet_widget.hide()

    def update_position(self, xdata: float, ydata: float) -> None:
        if self.perspective == self.Perspective.transversal:
            x_position = xdata
            y_position = ydata
            z_position = self.slice_no * self.cube.slice_distance
        elif self.perspective == self.Perspective.sagittal:
            x_position = self.slice_no * self.cube.pixel_size
            y_position = xdata
            z_position = ydata
        else:
            x_position = xdata
            y_position = self.slice_no * self.cube.pixel_size
            z_position = ydata

        x_position = "{:.2f}".format(round(x_position, 2))
        y_position = "{:.2f}".format(round(y_position, 2))
        z_position = "{:.2f}".format(round(z_position, 2))

        self.xPosition_label.setText("(" + x_position + ",")
        self.yPosition_label.setText(y_position + ",")
        self.zPosition_label.setText(z_position + ")")

    def update_doselet(self, xdata: float, ydata: float) -> None:
        x = math.floor((xdata - self.x_offset) / self.cube.pixel_size)
        if self.perspective == self.Perspective.transversal:
            y = math.floor((ydata - self.y_offset) / self.cube.pixel_size)
        else:
            y = math.floor((ydata - self.y_offset) / self.cube.slice_distance)

        self.doseletData_label.setText(str(self.data[y][x]))

    def update_cube(self, cube: CtxCube) -> None:
        # update cube when changing the patient
        self.cube = cube

    def update_mode(self, mode_name: str) -> None:
        self.mode = self.Mode(mode_name)

        if self.mode == self.Mode.dose:
            self.doseletDescription_label.setText("Dose:")
            self.doseletUnit_label.setText("%")
        elif self.mode == self.Mode.let:
            self.doseletDescription_label.setText("LET:")
            self.doseletUnit_label.setText("keV / µm")

    def update_slice_no(self, slice_no: int) -> None:
        self.slice_no = slice_no

    def update_doselet_data(self, data: ndarray) -> None:
        self.data = data

    class Perspective(Enum):
        transversal = "Transversal"
        sagittal = "Sagittal"
        coronal = "Coronal"

    class Mode(Enum):
        ctx = "Ctx"
        dose = "Dose"
        let = "Let"
