import math
from enum import Enum
from pathlib import Path

from PyQt5 import QtWidgets, uic

# TODO maybe show mouse-overed VOIs that have been selected in the VOI list;
#  hovering over the diagram in the upper right corner causes problems;
#  bug with interface breaking sometimes occurs after switching patients;
#  add some comments; some UI tweaks


class DataSample(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        ui_path = Path(Path(__file__).parent.parent, "view", "data_sample.ui").resolve()
        uic.loadUi(ui_path, self)

        self.position_widget.hide()
        self.doselet_widget.hide()

        self.mode = self.Mode.ctx
        self.perspective = self.Perspective.transveral
        self.data = None
        self.cube = None
        self.x_offset = 0
        self.y_offset = 0
        self.z_offset = 0
        self.slice = 0

    def update_perspective(self, perspective_name=None):
        if perspective_name:
            self.perspective = self.Perspective(perspective_name)

        if self.perspective == self.Perspective.transveral:
            self.x_offset = self.cube.xoffset
            self.y_offset = self.cube.yoffset
        elif self.perspective == self.Perspective.sagittal:
            self.x_offset = self.cube.yoffset
            self.y_offset = self.cube.zoffset
        else:
            self.x_offset = self.cube.xoffset
            self.y_offset = self.cube.zoffset

    def update_sample(self, event):
        if event.xdata:
            self.update_position(event)
            self.position_widget.show()

            if self.mode != self.Mode.ctx:
                self.update_doselet(event)
                self.doselet_widget.show()
        else:
            self.position_widget.hide()
            self.doselet_widget.hide()

    def update_position(self, event):
        if self.perspective == self.Perspective.transveral:
            x_position = event.xdata
            y_position = event.ydata
            z_position = self.slice * self.cube.slice_distance
        elif self.perspective == self.Perspective.sagittal:
            x_position = self.slice * self.cube.pixel_size
            y_position = event.xdata
            z_position = event.ydata
        else:
            x_position = event.xdata
            y_position = self.slice * self.cube.pixel_size
            z_position = event.ydata

        # TODO clamp it to ~5 digits
        x_position = "{:.2f}".format(round(x_position, 2))
        y_position = "{:.2f}".format(round(y_position, 2))
        z_position = "{:.2f}".format(round(z_position, 2))

        self.xPosition_label.setText("(" + x_position + ",")
        self.yPosition_label.setText(y_position + ",")
        self.zPosition_label.setText(z_position + ")")

    def update_doselet(self, event):
        x = math.floor((event.xdata - self.x_offset) / self.cube.pixel_size)
        if self.perspective == self.Perspective.transveral:
            y = math.floor((event.ydata - self.y_offset) / self.cube.pixel_size)
        else:
            y = math.floor((event.ydata - self.y_offset) / self.cube.slice_distance)

        self.doseletData_label.setText(str(self.data[y][x]))

    def update_cube(self, cube):
        self.cube = cube
        self.update_perspective()

    def update_mode_data(self, mode_name, data=None):
        self.mode = self.Mode(mode_name)

        if self.mode == self.Mode.ctx:
            self.slice = data
        else:
            self.data = data.data_to_plot

        if self.mode == self.Mode.dose:
            self.doseletDescription_label.setText("Dose:")
            self.doseletUnit_label.setText("%")
        elif self.mode == self.Mode.let:
            self.doseletDescription_label.setText("LET:")
            self.doseletUnit_label.setText("keV / µm")

    class Perspective(Enum):
        transveral = "Transversal"
        sagittal = "Sagittal"
        coronal = "Coronal"

    class Mode(Enum):
        ctx = "Ctx"
        dose = "Dose"
        let = "Let"
