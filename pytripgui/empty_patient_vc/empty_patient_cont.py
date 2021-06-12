import math
import os
import sys
from enum import Enum

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QIntValidator, QValidator, QRegularExpressionValidator
from pytrip.cube import Cube
from pytrip.ctx import CtxCube
from pytrip.vdx import VdxCube, create_sphere, create_cube, is_cuboidal_voi_contained, is_spherical_voi_contained

import logging

from pytripgui.view.qt_view_adapter import LineEdit, PushButton

logger = logging.getLogger(__name__)


class EmptyPatientController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_accepted = False
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
        if self._validate_all():
            self._calculate_fields(self.view.dimensions_tabs.current_index)
            self._set_model_from_view()
            self.is_accepted = True
            self.view.accept()

    def _convert_tab_contents(self):
        fields = self.view.dimensions_fields
        tabs = self.view.dimensions_tabs
        prev_index = tabs.previous_index
        curr_index = tabs.current_index

        if self._validate_tab(prev_index):
            self._calculate_fields(prev_index)
            for field in fields[curr_index]:
                fields[curr_index][field].text = self.parameters[field]
        else:
            self._clear_tab(prev_index)

        tabs.update_previous_index()

    def _clear_tab(self, index):
        for field in self.view.dimensions_fields[index].values():
            field.clear()

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
            p["pixel_number_y"] = int(float(prev["height"].text) / float(prev["pixel_size"].text))
            p["pixel_size"] = float(prev["pixel_size"].text)
        elif index == 1:
            p["width"] = float(prev["width"].text)
            p["height"] = float(prev["height"].text)
            p["depth"] = float(prev["depth"].text)
            p["slice_distance"] = round(float(prev["depth"].text) / int(prev["slice_number"].text), 3)
            p["slice_number"] = int(prev["slice_number"].text)
            p["pixel_number_x"] = int(prev["pixel_number_x"].text)
            p["pixel_number_y"] = int(prev["pixel_number_y"].text)
            p["pixel_size"] = round(float(prev["width"].text) / int(prev["pixel_number_x"].text), 3)
        else:
            p["width"] = int(prev["pixel_number_x"].text) * float(prev["pixel_size"].text)
            p["height"] = int(prev["pixel_number_y"].text) * float(prev["pixel_size"].text)
            p["depth"] = int(prev["slice_number"].text) * float(prev["slice_distance"].text)
            p["slice_distance"] = float(prev["slice_distance"].text)
            p["slice_number"] = int(prev["slice_number"].text)
            p["pixel_number_x"] = int(prev["pixel_number_x"].text)
            p["pixel_number_y"] = int(prev["pixel_number_y"].text)
            p["pixel_size"] = float(prev["pixel_size"].text)

    def _set_validators(self):
        dim = self.view.dimensions_fields

        validator = QIntValidator()
        self.view.hu_value.enable_validation(validator)

        validator = QIntValidator()
        validator.setBottom(1)
        enable_validation_list(validator,
            [
                dim[1]["slice_number"],
                dim[2]["slice_number"],
                dim[2]["pixel_number_x"],
                dim[2]["pixel_number_y"]
            ]
        )

        validator = QRegularExpressionValidator(Regex.FLOAT.value)
        self.view.slice_offset.enable_validation(validator)

        validator = QRegularExpressionValidator(Regex.FLOAT_POSITIVE.value)
        enable_validation_list(validator,
            [
                dim[0]["slice_distance"],
                dim[0]["pixel_size"],
                dim[1]["depth"],
                dim[2]["slice_distance"],
                dim[2]["pixel_size"]
            ]
        )

        validator = MultipleOfRegularExpressionValidator(Regex.FLOAT_POSITIVE.value)
        validator.set_multiple_of(dim[0]["pixel_size"])
        enable_validation_list(validator,
            [
                dim[0]["width"],
                dim[0]["height"],
            ]
        )
        dim[0]["pixel_size"].emit_on_text_change(
            lambda: validate_list([
                dim[0]["width"],
                dim[0]["height"]
            ])
        )

        validator = MultipleOfRegularExpressionValidator(Regex.FLOAT_POSITIVE.value)
        validator.set_multiple_of(dim[0]["slice_distance"])
        enable_validation_list(validator,
            [
                dim[0]["depth"]
            ]
        )
        dim[0]["slice_distance"].emit_on_text_change(
            lambda: validate_list([
                dim[0]["depth"]
            ])
        )

        validator = PixelSizeValidator(Regex.FLOAT_POSITIVE.value)
        validator.set_additional_validation(self._validate_pixel_size)
        enable_validation_list(validator,
            [
                dim[1]["width"],
                dim[1]["height"]
            ]
        )

        validator = PixelSizeValidator(Regex.INT_POSITIVE.value)
        validator.set_additional_validation(self._validate_pixel_size)
        enable_validation_list(validator,
            [
                dim[1]["pixel_number_x"],
                dim[1]["pixel_number_y"]
            ]
        )

    def _validate_all(self):
        if self._validate_general_parameters() and self._validate_tab(self.view.dimensions_tabs.current_index):
            self._calculate_fields(self.view.dimensions_tabs.current_index)
            return self._validate_vois() and self._validate_vois_cube()
        return False

    def _validate_general_parameters(self):
        return self.view.hu_value.validate() and \
               self.view.slice_offset.validate()

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

    def _validate_pixel_size(self):
        dim = self.view.dimensions_fields[1]
        fields = [dim["width"], dim["pixel_number_x"], dim["height"], dim["pixel_number_y"]]
        if any(not field.text for field in fields):
            return False

        width = string2float(dim["width"].text)
        pixel_number_x = int(dim["pixel_number_x"].text)
        height = string2float(dim["height"].text)
        pixel_number_y = int(dim["pixel_number_y"].text)
        if math.isclose(width / pixel_number_x, height / pixel_number_y, abs_tol=1e-3):
            for field in fields:
                field.highlight_border(False)
            return True
        else:
            for field in fields:
                field.highlight_border(True)
            return False

    def _validate_vois(self):
        result = True
        vois = self.view.voi_scroll_area.widget().layout()
        for index in range(vois.count() - 1):
            voi = vois.itemAt(index).widget()
            if not voi.validate():
                result = False
        return result

    def _validate_vois_cube(self):
        final_result = True
        vois = self.view.voi_scroll_area.widget().layout()
        for index in range(vois.count() - 1):
            voi = vois.itemAt(index).widget()
            cube_dims = [
                self.parameters["width"],
                self.parameters["height"],
                self.parameters["depth"]
            ]

            if isinstance(voi, SphericalVOIWidget):
                result = is_spherical_voi_contained(cube_dims, voi.center, voi.radius)
            else:
                result = is_cuboidal_voi_contained(cube_dims, voi.center, voi.dims)

            if not result:
                voi.highlight_border(True)
                final_result = False
            else:
                voi.highlight_border(False)

        return final_result

    def _add_voi_widget(self, widget_type):
        widget = widget_type()
        index = self.view.voi_scroll_area.widget().layout().count() - 1
        self.view.voi_scroll_area.widget().layout().insertWidget(index, widget)

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
        for index in range(vois.count() - 1):
            voi = vois.itemAt(index).widget()

            if isinstance(voi, SphericalVOIWidget):
                voi = create_sphere(
                    cube=self.model.ctx,
                    name=voi.name,
                    center=voi.center,
                    radius=voi.radius
                )
            else:
                voi = create_cube(
                    cube=self.model.ctx,
                    name=voi.name,
                    center=voi.center,
                    width=voi.width,
                    height=voi.height,
                    depth=voi.depth,
                )
            vdxCube.add_voi(voi)

        self.model.vdx = vdxCube
        self.model.name = self.view.name.text


class VOIWidget(QtWidgets.QFrame):
    def __init__(self, file):
        super().__init__()
        path = os.path.join(sys.path[0], file)
        uic.loadUi(path, self)

        self._name = LineEdit(self.name_lineEdit)
        self._center = [
            LineEdit(self.centerX_lineEdit),
            LineEdit(self.centerY_lineEdit),
            LineEdit(self.centerZ_lineEdit)
        ]

        validator = QRegularExpressionValidator(Regex.STRING.value)
        self._name.enable_validation(validator)
        self._name.validate()

        validator = QRegularExpressionValidator(Regex.FLOAT_POSITIVE.value)
        enable_validation_list(validator, self._center)
        validate_list(self._center)

        self._remove_button = PushButton(self.remove_pushButton)
        self._remove_button.emit_on_click(
            lambda: self._remove_self()
        )

    @property
    def name(self):
        return self._name.text

    @property
    def center(self):
        return [string2float(i.text) for i in self._center]

    def validate(self):
        return self._name.validate() and \
               validate_list(self._center)

    def highlight_border(self, highlight=False):
        if highlight:
            self.setStyleSheet("#VOI { border: 1px solid red }")
        else:
            self.setStyleSheet("#VOI { border: 1px solid black }")

    def _remove_self(self):
        self.parent().layout().removeWidget(self)
        self.close()


class SphericalVOIWidget(VOIWidget):
    def __init__(self):
        super().__init__("view//spherical_voi.ui")

        self._radius = LineEdit(self.radius_lineEdit)

        validator = QRegularExpressionValidator(Regex.FLOAT_POSITIVE.value)
        self._radius.enable_validation(validator)
        self._radius.validate()

    @property
    def radius(self):
        return string2float(self._radius.text)

    def validate(self):
        return super().validate() and \
               self._radius.validate()


class CuboidalVOIWidget(VOIWidget):
    def __init__(self):
        super().__init__("view//cuboidal_voi.ui")

        self._width = LineEdit(self.width_lineEdit)
        self._height = LineEdit(self.height_lineEdit)
        self._depth = LineEdit(self.depth_lineEdit)
        self._dims = [
            self._width,
            self._height,
            self._depth
        ]

        validator = QRegularExpressionValidator(Regex.FLOAT_POSITIVE.value)
        enable_validation_list(validator, self._dims)
        validate_list(self._dims)

    @property
    def width(self):
        return string2float(self._width.text)

    @property
    def height(self):
        return string2float(self._height.text)

    @property
    def depth(self):
        return string2float(self._depth.text)

    @property
    def dims(self):
        return [string2float(i.text) for i in self._dims]

    def validate(self):
        return super().validate() and \
               validate_list(self._dims)


class MultipleOfRegularExpressionValidator(QRegularExpressionValidator):
    def __init__(self, regex=None):
        super().__init__(regex)
        self._multiple_of_line_edit = None

    def set_multiple_of(self, value):
        self._multiple_of_line_edit = value

    def validate(self, string, pos):
        result = super().validate(string, pos)
        if result[0] != QValidator.Acceptable:
            return result

        if self._multiple_of_line_edit is None:
            return QValidator.Intermediate, string, pos

        if not self._multiple_of_line_edit.text:
            return QValidator.Acceptable, string, pos

        string_num = string2float(string)
        multiple_of = string2float(self._multiple_of_line_edit.text)

        if math.isclose(string_num % multiple_of, 0, abs_tol=1e-3):
            return QValidator.Acceptable, string, pos
        return QValidator.Intermediate, string, pos


class PixelSizeValidator(QRegularExpressionValidator):
    def __init__(self, regex=None):
        super().__init__(regex)
        self._pixel_size_validation = None

    def set_additional_validation(self, validation):
        self._pixel_size_validation = validation

    def validate(self, string, pos):
        result = super().validate(string, pos)
        if result[0] != QValidator.Acceptable:
            return result

        if self._pixel_size_validation is not None and self._pixel_size_validation():
            return QValidator.Acceptable, string, pos
        return QValidator.Intermediate, string, pos


class Regex(Enum):
    STRING = QRegularExpression("\\w+")
    INT_POSITIVE = QRegularExpression("\\d*[1-9]\\d*")
    FLOAT = QRegularExpression("-?((\\d+([,\\.]\\d{0,3})?)|(\\d*[,\\.]\\d{1,3}))")
    FLOAT_POSITIVE = QRegularExpression("((\\d*[1-9]\\d*([,\\.]\\d{0,3})?)|(\\d*[,\\.](?=\\d{1,3}$)(\\d*[1-9]\\d*)))")


def string2float(string):
    string_copy = string.replace(",", ".")
    if string_copy.endswith("."):
        string_copy = string_copy[:-1]
    return float(string_copy)


def enable_validation_list(validator, fields):
    for field in fields:
        field.enable_validation(validator)


def validate_list(items):
    result = True
    for item in items:
        if not item.validate():
            result = False
    return result
