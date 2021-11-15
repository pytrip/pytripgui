from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QRegularExpressionValidator
from pathlib import Path

from pytripgui.utils.regex import Regex
from pytripgui.view.qt_view_adapter import LineEdit


class VOIWidget(QtWidgets.QFrame):
    def __init__(self, widget_file):
        super().__init__()
        widget_path = Path(Path(__file__).parent, "widgets", widget_file).resolve()
        uic.loadUi(widget_path, self)

        self._name = LineEdit(self.name_lineEdit)
        self._center = [
            LineEdit(self.centerX_lineEdit),
            LineEdit(self.centerY_lineEdit),
            LineEdit(self.centerZ_lineEdit)
        ]

        validator = QRegularExpressionValidator(Regex.STRING.value)
        self._name.enable_validation(validator)

        validator = QRegularExpressionValidator(Regex.FLOAT.value)
        enable_validation_list(validator, self._center)

    @property
    def name(self):
        return self._name.text

    @property
    def center(self):
        return [float(field.text) for field in self._center]

    def validate(self) -> bool:
        return self._name.validate() and validate_list(self._center)

    def disable_fields(self) -> None:
        self._name.set_enabled(False)
        for field in self._center:
            field.set_enabled(False)


class SphericalVOIWidget(VOIWidget):
    def __init__(self):
        super().__init__("spherical_voi.ui")

        self._radius = LineEdit(self.radius_lineEdit)

        validator = QRegularExpressionValidator(Regex.FLOAT_UNSIGNED.value)
        self._radius.enable_validation(validator)

    @property
    def radius(self):
        return float(self._radius.text)

    def validate(self) -> bool:
        return super().validate() and self._radius.validate()

    def disable_fields(self) -> None:
        super().disable_fields()
        self._radius.set_enabled(False)


class CuboidalVOIWidget(VOIWidget):
    def __init__(self):
        super().__init__("cuboidal_voi.ui")

        self._width = LineEdit(self.width_lineEdit)
        self._height = LineEdit(self.height_lineEdit)
        self._depth = LineEdit(self.depth_lineEdit)
        self._dims = [self._width, self._height, self._depth]

        validator = QRegularExpressionValidator(Regex.FLOAT_UNSIGNED.value)
        enable_validation_list(validator, self._dims)

    @property
    def width(self) -> float:
        return float(self._width.text)

    @property
    def height(self) -> float:
        return float(self._height.text)

    @property
    def depth(self) -> float:
        return float(self._depth.text)

    @property
    def dims(self) -> list:
        return [float(i.text) for i in self._dims]

    def validate(self) -> bool:
        return super().validate() and validate_list(self._dims)

    def disable_fields(self) -> None:
        super().disable_fields()
        for field in self._dims:
            field.set_enabled(False)


class CylindricalVOIWidget(VOIWidget):
    def __init__(self):
        super().__init__("cylindrical_voi.ui")

        self._radius = LineEdit(self.radius_lineEdit)
        self._depth = LineEdit(self.depth_lineEdit)

        validator = QRegularExpressionValidator(Regex.FLOAT_UNSIGNED.value)
        self._radius.enable_validation(validator)
        self._depth.enable_validation(validator)

    @property
    def radius(self):
        return float(self._radius.text)

    @property
    def depth(self):
        return float(self._depth.text)

    def validate(self) -> bool:
        return super().validate() and self._radius.validate() and self._depth.validate()

    def disable_fields(self) -> None:
        super().disable_fields()
        self._radius.set_enabled(False)
        self._depth.set_enabled(False)


def enable_validation_list(validator: QRegularExpressionValidator, items: list) -> None:
    for item in items:
        item.enable_validation(validator)


def validate_list(items: list) -> bool:
    result = True
    for item in items:
        if not item.validate():
            result = False
    return result
