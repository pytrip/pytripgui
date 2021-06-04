import os
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QIntValidator, QValidator, QRegularExpressionValidator
from pytrip.cube import Cube, validate_cube_voi
from pytrip.ctx import CtxCube
from pytrip.vdx import VdxCube, create_sphere, create_cube

import logging

from pytripgui.view.qt_view_adapter import LineEdit, PushButton

logger = logging.getLogger(__name__)


class EmptyPatientController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_cancelled = True
        self._setup_callbacks()

        self._set_validators()
        self._validate_tabs()

        self.parameters = dict.fromkeys([
            "width",
            "height",
            "depth",
            "slice_distance",
            "slice_number",
            "pixel_number_x",
            "pixel_number_y",
            "pixel_size"
        ])

    def _setup_callbacks(self):
        self.view.accept_buttons.accepted.disconnect()
        self.view.accept_buttons.accepted.connect(self._save_and_exit)

        self.view.dimensions_tabs.emit_on_tab_change(self._convert_tab_contents)

        self.view.add_spherical_voi_button.emit_on_click(
            lambda: self._add_voi_widget(SphericalVOIWidget)
        )
        self.view.add_cuboidal_voi_button.emit_on_click(
            lambda: self._add_voi_widget(CuboidalVOIWidget)
        )

    def _save_and_exit(self):
        self._calculate_fields(self.view.dimensions_tabs.current_index)

        if self._validate_all():
            self.is_cancelled = False
            self._set_model_from_view()
            self.view.accept()

    def _convert_tab_contents(self):
        previous_index = self.view.dimensions_tabs.previous_index
        current_index = self.view.dimensions_tabs.current_index

        if self._validate_tab(previous_index) and \
                (self.view.dimensions_tabs.previous_index != 1 or self._validate_pixel_values_relation()):
            self._calculate_fields(previous_index)

            for field in self.view.dimensions_fields[current_index]:
                self.view.dimensions_fields[current_index][field].text = self.parameters[field]
        else:
            self._clear_tab(previous_index)

        self.view.dimensions_tabs.update_previous_index()

    def _calculate_fields(self, index):
        p = self.parameters
        prev = self.view.dimensions_fields[index]
        if index == 0:
            p["width"] = float(prev["width"].text)
            p["height"] = float(prev["height"].text)
            p["depth"] = float(prev["depth"].text)
            p["slice_distance"] = float(prev["slice_distance"].text)
            p["slice_number"] = int(float(prev["depth"].text) / float(prev["slice_distance"].text))
            p["pixel_number_x"] = int(float(prev["width"].text) / float(prev["pixel_size"].text))
            p["pixel_number_y"] = int(float(prev["width"].text) / float(prev["pixel_size"].text))
            p["pixel_size"] = float(prev["pixel_size"].text)
        elif index == 1:
            p["width"] = float(prev["width"].text)
            p["height"] = float(prev["height"].text)
            p["depth"] = float(prev["depth"].text)
            p["slice_distance"] = float(prev["depth"].text) / int(prev["slice_number"].text)
            p["slice_number"] = int(prev["slice_number"].text)
            p["pixel_number_x"] = int(prev["pixel_number_x"].text)
            p["pixel_number_y"] = int(prev["pixel_number_y"].text)
            p["pixel_size"] = float(prev["width"].text) / int(prev["pixel_number_x"].text)
        else:
            p["width"] = int(prev["pixel_number_x"].text) * float(prev["pixel_size"].text)
            p["height"] = int(prev["pixel_number_y"].text) * float(prev["pixel_size"].text)
            p["depth"] = int(prev["slice_number"].text) * float(prev["slice_distance"].text)
            p["slice_distance"] = float(prev["slice_distance"].text)
            p["slice_number"] = int(prev["slice_number"].text)
            p["pixel_number_x"] = int(prev["pixel_number_x"].text)
            p["pixel_number_y"] = int(prev["pixel_number_y"].text)
            p["pixel_size"] = float(prev["pixel_size"].text)

    def _validate_all(self):
        return self._validate_general_parameters() and self._validate_tab(self.view.dimensions_tabs.current_index) and \
               (self.view.dimensions_tabs.current_index != 1 or self._validate_pixel_values_relation()) and \
               self._validate_vois() and self._validate_vois_patient()

    def _validate_general_parameters(self):
        return self.view.hu_value.validate() and self.view.slice_offset.validate()

    def _validate_tabs(self):
        result = True
        for index in range(len(self.view.dimensions_fields)):
            if not self._validate_tab(index):
                result = False
        return result

    def _validate_tab(self, index):
        result = True
        for field in self.view.dimensions_fields[index].values():
            if not field.validate():
                result = False
        return result

    def _validate_pixel_values_relation(self):
        dim = self.view.dimensions_fields[1]
        fields = [dim["width"], dim["height"], dim["pixel_number_x"], dim["pixel_number_y"]]

        p = self.parameters
        if p["width"] / p["pixel_number_x"] != p["height"] / p["pixel_number_y"]:
            [x.highlight_border(True) for x in fields]
            return False
        else:
            [x.highlight_border(False) for x in fields]
            return True

    def _validate_vois(self):
        result = True
        vois = self.view.voi_scroll_area.widget().layout()
        for index in range(vois.count()):
            voi = vois.itemAt(index).widget()
            if not voi.validate():
                result = False
        return result

    def _validate_vois_patient(self):
        result = True
        vois = self.view.voi_scroll_area.widget().layout()
        for index in range(vois.count()):
            voi = vois.itemAt(index).widget()
            cube_dims = [
                self.parameters["width"],
                self.parameters["height"],
                self.parameters["depth"]
            ]
            voi_center = voi.get_center()
            if isinstance(voi, SphericalVOIWidget):
                voi_params = [float(voi.radius.text)]
            else:
                voi_params = [
                    float(voi.width.text),
                    float(voi.height.text),
                    float(voi.depth.text)
                ]
            if not validate_cube_voi(cube_dims, voi_center, voi_params):
                voi.highlight_border(True)
                result = False
            else:
                voi.highlight_border(False)

        return result

    def _clear_tab(self, index):
        for field in self.view.dimensions_fields[index].values():
            field.clear()

    def _set_validators(self):
        validator = QIntValidator()
        self.view.hu_value.enable_validation(validator)

        validator = QIntValidator()
        validator.setBottom(1)
        self.view.dimensions_fields[1]["slice_number"].enable_validation(validator)
        self.view.dimensions_fields[1]["pixel_number_x"].enable_validation(validator)
        self.view.dimensions_fields[1]["pixel_number_y"].enable_validation(validator)
        self.view.dimensions_fields[2]["slice_number"].enable_validation(validator)
        self.view.dimensions_fields[2]["pixel_number_x"].enable_validation(validator)
        self.view.dimensions_fields[2]["pixel_number_y"].enable_validation(validator)

        validator = DoubleValidatorLowerLimit()
        self.view.slice_offset.enable_validation(validator)

        validator = DoubleValidatorLowerLimit()
        validator.setBottom(0, False)
        self.view.dimensions_fields[0]["width"].enable_validation(validator)
        self.view.dimensions_fields[0]["height"].enable_validation(validator)
        self.view.dimensions_fields[0]["depth"].enable_validation(validator)
        self.view.dimensions_fields[0]["slice_distance"].enable_validation(validator)
        self.view.dimensions_fields[0]["pixel_size"].enable_validation(validator)
        self.view.dimensions_fields[1]["width"].enable_validation(validator)
        self.view.dimensions_fields[1]["height"].enable_validation(validator)
        self.view.dimensions_fields[1]["depth"].enable_validation(validator)
        self.view.dimensions_fields[2]["slice_distance"].enable_validation(validator)
        self.view.dimensions_fields[2]["pixel_size"].enable_validation(validator)

    def _add_voi_widget(self, widget_type):
        widget = widget_type()
        self.view.voi_scroll_area.widget().layout().addWidget(widget)

    def _set_model_from_view(self):
        cube = Cube()

        cube.create_empty_cube(
            dimx=self.parameters["pixel_number_x"],
            dimy=self.parameters["pixel_number_y"],
            dimz=self.parameters["slice_number"],
            slice_offset=float(self.view.slice_offset.text),
            slice_distance=self.parameters["slice_distance"],
            pixel_size=self.parameters["pixel_size"],
            value=int(self.view.hu_value.text)
        )

        self.model.ctx = CtxCube(cube)
        self.model.ctx.basename = self.view.name.text

        vdxCube = VdxCube(self.model.ctx)
        vdxCube.basename = self.view.name.text

        vois = self.view.voi_scroll_area.widget().layout()
        for index in range(vois.count()):
            voi = vois.itemAt(index).widget()
            center = voi.get_center()

            if isinstance(voi, SphericalVOIWidget):
                sphere = create_sphere(
                    cube=self.model.ctx,
                    name=voi.name.text,
                    center=[
                        center[0],
                        center[1],
                        center[2],
                    ],
                    radius=float(voi.radius.text)
                )
                vdxCube.add_voi(sphere)
            else:
                cube = create_cube(
                    cube=self.model.ctx,
                    name=voi.name.text,
                    center=[
                        center[0],
                        center[1],
                        center[2],
                    ],
                    width=float(voi.width.text),
                    height=float(voi.height.text),
                    depth=float(voi.depth.text),
                )
                vdxCube.add_voi(cube)

        self.model.vdx = vdxCube
        self.model.name = self.view.name.text


class VOIWidget(QtWidgets.QFrame):
    def __init__(self, file):
        super().__init__()
        path = os.path.join(sys.path[0], file)
        uic.loadUi(path, self)

        self.name = LineEdit(self.name_lineEdit)
        self.center = LineEdit(self.center_lineEdit)

        validator = QRegularExpressionValidator(QRegularExpression("\\w+"))
        self.name.enable_validation(validator)
        self.name.validate()

        validator = DoubleVector3Validator()
        self.center.enable_validation(validator)
        self.center.validate()

        self.remove_button = PushButton(self.remove_pushButton)
        self.remove_button.emit_on_click(self.close)

    def get_center(self):
        center = self.center.text.replace(" ", "").split(";")
        return [float(x) for x in center]

    def validate(self):
        return self.name.validate() and self.center.validate()

    def highlight_border(self, highlight=False):
        if highlight:
            self.setStyleSheet("#VOI { border: 1px solid red }")
        else:
            self.setStyleSheet("#VOI { border: 1px solid black }")


class SphericalVOIWidget(VOIWidget):
    def __init__(self):
        super().__init__("view//spherical_voi.ui")

        self.radius = LineEdit(self.radius_lineEdit)

        validator = DoubleValidatorLowerLimit()
        validator.setBottom(0, False)
        self.radius.enable_validation(validator)
        self.radius.validate()

    def validate(self):
        return super().validate() and self.radius.validate()


class CuboidalVOIWidget(VOIWidget):
    def __init__(self):
        super().__init__("view//cuboidal_voi.ui")

        self.width = LineEdit(self.width_lineEdit)
        self.height = LineEdit(self.height_lineEdit)
        self.depth = LineEdit(self.depth_lineEdit)

        validator = DoubleValidatorLowerLimit()
        validator.setBottom(0, False)
        self.width.enable_validation(validator)
        self.width.validate()
        self.height.enable_validation(validator)
        self.height.validate()
        self.depth.enable_validation(validator)
        self.depth.validate()

    def validate(self):
        return super().validate() and self.width.validate() and self.height.validate() and self.depth.validate()


class DoubleVector3Validator(QValidator):
    def __init__(self):
        super().__init__()

    def validate(self, string, pos):
        if not string:
            return QValidator.Intermediate, string, pos

        center = string.replace(" ", "").split(";")
        if len(center) != 3:
            return QValidator.Intermediate, string, pos

        regex = QRegularExpression("[-]?\\d+([,.]?\\d*)?")
        states = [QRegularExpressionValidator(regex).validate(x, pos) for x in center]
        for state in states:
            if state[0] != QValidator.Acceptable:
                return QValidator.Intermediate, string, pos

        return QValidator.Acceptable, string, pos


class DoubleValidatorLowerLimit(QValidator):
    def __init__(self):
        super().__init__()
        self._bottom = None

    def setBottom(self, value, inclusive=True):
        self._bottom = value
        self._inclusive = inclusive

    def validate(self, string, pos):
        if not string:
            return QValidator.Intermediate, string, pos

        if self._bottom and self._bottom >= 0:
            regex = QRegularExpression("\\d+([,.]?\\d*)?")
        else:
            regex = QRegularExpression("[-]?\\d+([,.]?\\d*)?")
        state = QRegularExpressionValidator(regex).validate(string, pos)

        if not self._bottom:
            return state

        string_copy = string.replace(",", ".")
        if string_copy.endswith("."):
            string_copy = string_copy[:-1]

        if state[0] == QValidator.Acceptable and \
                ((self._inclusive and float(string_copy) < self._bottom) or
                 (not self._inclusive and float(string_copy) <= self._bottom)):
            return QValidator.Intermediate, string, pos

        return state
