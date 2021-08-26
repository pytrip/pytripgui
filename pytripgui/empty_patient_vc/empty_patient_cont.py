import math
from enum import Enum

from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QValidator, QRegularExpressionValidator
from pytrip.ctx import CtxCube
from pytrip.vdx import VdxCube


class EmptyPatientController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_accepted = False
        self._setup_callbacks()

        self._set_validators()
        self._validate_tabs()

        self.parameters = dict.fromkeys([
            "width", "height", "depth", "slice_distance", "slice_number", "pixel_number_x", "pixel_number_y",
            "pixel_size"
        ])

    def _setup_callbacks(self):
        self.view.accept_buttons.accepted.disconnect()
        self.view.accept_buttons.accepted.connect(self._save_and_exit)

        self.view.dimensions_tabs.emit_on_tab_change(self._convert_tab_contents)

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

        validator = QRegularExpressionValidator(Regex.INT.value)
        self.view.hu_value.enable_validation(validator)

        validator = QRegularExpressionValidator(Regex.INT_POSITIVE.value)
        enable_validation_list(
            validator,
            [dim[1]["slice_number"], dim[2]["slice_number"], dim[2]["pixel_number_x"], dim[2]["pixel_number_y"]])

        validator = QRegularExpressionValidator(Regex.FLOAT.value)
        self.view.slice_offset.enable_validation(validator)

        validator = QRegularExpressionValidator(Regex.FLOAT_POSITIVE.value)
        enable_validation_list(validator, [
            dim[0]["slice_distance"], dim[0]["pixel_size"], dim[1]["depth"], dim[2]["slice_distance"],
            dim[2]["pixel_size"]
        ])

        validator = MultipleOfRegularExpressionValidator(Regex.FLOAT_POSITIVE.value)
        validator.set_multiple_of(dim[0]["pixel_size"])
        enable_validation_list(validator, [dim[0]["width"], dim[0]["height"]])
        dim[0]["pixel_size"].emit_on_text_change(lambda: validate_list([dim[0]["width"], dim[0]["height"]]))

        validator = MultipleOfRegularExpressionValidator(Regex.FLOAT_POSITIVE.value)
        validator.set_multiple_of(dim[0]["slice_distance"])
        enable_validation_list(validator, [dim[0]["depth"]])
        dim[0]["slice_distance"].emit_on_text_change(lambda: validate_list([dim[0]["depth"]]))

        validator = PixelSizeValidator(Regex.FLOAT_POSITIVE.value)
        validator.set_additional_validation(self._validate_pixel_size)
        enable_validation_list(validator, [dim[1]["width"], dim[1]["height"]])

        validator = PixelSizeValidator(Regex.INT_POSITIVE.value)
        validator.set_additional_validation(self._validate_pixel_size)
        enable_validation_list(validator, [dim[1]["pixel_number_x"], dim[1]["pixel_number_y"]])

    def _validate_all(self):
        return self._validate_general_parameters() and self._validate_tab(self.view.dimensions_tabs.current_index)

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

    def _validate_pixel_size(self):
        dim = self.view.dimensions_fields[1]
        fields = [dim["width"], dim["pixel_number_x"], dim["height"], dim["pixel_number_y"]]
        # check if any of the fields are empty
        if any(not field.text for field in fields):
            return False

        width = float(dim["width"].text)
        height = float(dim["height"].text)
        pixel_number_x = int(dim["pixel_number_x"].text)
        pixel_number_y = int(dim["pixel_number_y"].text)
        if math.isclose(width / pixel_number_x, height / pixel_number_y, abs_tol=1e-3):
            for field in fields:
                field.highlight_border(False)
            return True
        for field in fields:
            field.highlight_border(True)
        return False

    def _set_model_from_view(self):
        ctx = CtxCube()

        ctx.create_empty_cube(dimx=self.parameters["pixel_number_x"],
                              dimy=self.parameters["pixel_number_y"],
                              dimz=self.parameters["slice_number"],
                              slice_offset=float(self.view.slice_offset.text),
                              slice_distance=self.parameters["slice_distance"],
                              pixel_size=self.parameters["pixel_size"],
                              value=int(self.view.hu_value.text))
        self.model.ctx = ctx
        self.model.ctx.basename = self.view.name.text

        vdxCube = VdxCube(self.model.ctx)
        vdxCube.basename = self.view.name.text
        self.model.vdx = vdxCube
        self.model.name = self.view.name.text


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

        string = string.replace(",", ".")
        if string.endswith("."):
            string = string[:-1]
        string_num = float(string)
        multiple_of = float(self._multiple_of_line_edit.text)

        if multiple_of and \
                ((multiple_of < 1 and math.isclose(abs(round(string_num / multiple_of, 0) - string_num / multiple_of),
                                                   0, abs_tol=1e-9)) or
                 math.isclose(string_num % multiple_of, 0, abs_tol=1e-3)):
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
    STRING = QRegularExpression(r"\w+")
    INT = QRegularExpression(r"-?\d+")
    INT_POSITIVE = QRegularExpression(r"\d*[1-9]\d*")
    FLOAT = QRegularExpression(r"-?((\d+([,\.]\d{0,3})?)|(\d*[,\.]\d{1,3}))")
    FLOAT_POSITIVE = QRegularExpression(r"(\d*[1-9]\d*([,\.]\d{0,3})?)|(\d*[,\.](?=\d{1,3}$)(\d*[1-9]\d*))")
    FLOAT_UNSIGNED = QRegularExpression(r"0+|((\d*[1-9]\d*([,\.]\d{0,3})?)|(\d*[,\.](?=\d{1,3}$)(\d*[1-9]\d*)))")


def enable_validation_list(validator, items):
    for item in items:
        item.enable_validation(validator)


def validate_list(items):
    result = True
    for item in items:
        if not item.validate():
            result = False
    return result
