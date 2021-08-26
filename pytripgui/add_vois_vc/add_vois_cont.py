import os
import sys
from enum import Enum

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from pytrip.vdx import create_sphere, create_cube

import logging

from pytripgui.view.qt_view_adapter import LineEdit, PushButton

logger = logging.getLogger(__name__)


class AddVOIsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_accepted = False
        self._setup_callbacks()

        self.parameters = dict.fromkeys([
            "width", "height", "depth", "slice_distance", "slice_number", "pixel_number_x", "pixel_number_y",
            "pixel_size"
        ])

        self._set_view_from_model()

    def _setup_callbacks(self):
        self.view.accept_buttons.accepted.disconnect()
        self.view.accept_buttons.accepted.connect(self._save_and_exit)

        self.view.add_spherical_voi_button.emit_on_click(lambda: self._add_voi_widget(SphericalVOIWidget))
        self.view.add_cuboidal_voi_button.emit_on_click(lambda: self._add_voi_widget(CuboidalVOIWidget))

    def _save_and_exit(self):
        if self._validate_all():
            self._set_model_from_view()
            self.is_accepted = True
            self.view.accept()

    def _validate_all(self):
        return self._validate_vois() and self._validate_vois_contained()

    def _validate_vois(self):
        result = True
        voi_widgets = self.view.voi_scroll_area.widget().layout()
        for index in range(voi_widgets.count() - 1):
            voi_widget = voi_widgets.itemAt(index).widget()
            if not voi_widget.validate():
                result = False
        return result

    def _validate_vois_contained(self):
        final_result = True

        ctx = self.model.ctx

        voi_widgets = self.view.voi_scroll_area.widget().layout()
        for index in range(voi_widgets.count() - 1):
            voi_widget = voi_widgets.itemAt(index).widget()

            if isinstance(voi_widget, SphericalVOIWidget):
                voi = create_sphere(cube=ctx, name=voi_widget.name, center=voi_widget.center, radius=voi_widget.radius)
            else:
                voi = create_cube(
                    cube=ctx,
                    name=voi_widget.name,
                    center=voi_widget.center,
                    width=voi_widget.width,
                    height=voi_widget.height,
                    depth=voi_widget.depth,
                )

            if voi.is_fully_contained():
                voi_widget.highlight_border(False)
            else:
                voi_widget.highlight_border(True)
                final_result = False

        return final_result

    def _add_voi_widget(self, widget_type):
        widget = widget_type()
        index = self.view.voi_scroll_area.widget().layout().count() - 1
        self.view.voi_scroll_area.widget().layout().insertWidget(index, widget)

    def _set_view_from_model(self):
        p = self.parameters
        ctx = self.model.ctx

        self.view.name.text = ctx.patient_name

        p["width"] = ctx.dimx
        p["height"] = ctx.dimy
        p["depth"] = ctx.dimz
        p["slice_distance"] = ctx.slice_distance
        p["slice_number"] = ctx.slice_number
        p["pixel_size"] = ctx.pixel_size
        p["pixel_number_x"] = ctx.dimx / ctx.pixel_size
        p["pixel_number_y"] = ctx.dimy / ctx.pixel_size

        fields_tabs = self.view.dimensions_fields
        for fields_tab in fields_tabs:
            for field in fields_tab:
                fields_tab[field].text = self.parameters[field]

    def _set_model_from_view(self):
        vdx = self.model.vdx

        voi_widgets = self.view.voi_scroll_area.widget().layout()
        for index in range(voi_widgets.count() - 1):
            voi_widget = voi_widgets.itemAt(index).widget()

            if isinstance(voi_widget, SphericalVOIWidget):
                voi = create_sphere(
                    cube=self.model.ctx,
                    name=voi_widget.name,
                    center=voi_widget.center,
                    radius=voi_widget.radius,
                )
            else:
                voi = create_cube(
                    cube=self.model.ctx,
                    name=voi_widget.name,
                    center=voi_widget.center,
                    width=voi_widget.width,
                    height=voi_widget.height,
                    depth=voi_widget.depth,
                )
            vdx.add_voi(voi)


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

        validator = RegularExpressionValidator(Regex.STRING.value)
        self._name.enable_validation(validator)
        self._name.validate()

        validator = RegularExpressionValidator(Regex.FLOAT.value)
        enable_validation_list(validator, self._center)
        validate_list(self._center)

        self._remove_button = PushButton(self.remove_pushButton)
        self._remove_button.emit_on_click(self._remove_self)

    @property
    def name(self):
        return self._name.text

    @property
    def center(self):
        return [float(i.text) for i in self._center]

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

        validator = RegularExpressionValidator(Regex.FLOAT_UNSIGNED.value)
        self._radius.enable_validation(validator)
        self._radius.validate()

    @property
    def radius(self):
        return float(self._radius.text)

    def validate(self):
        return super().validate() and \
               self._radius.validate()


class CuboidalVOIWidget(VOIWidget):
    def __init__(self):
        super().__init__("view//cuboidal_voi.ui")

        self._width = LineEdit(self.width_lineEdit)
        self._height = LineEdit(self.height_lineEdit)
        self._depth = LineEdit(self.depth_lineEdit)
        self._dims = [self._width, self._height, self._depth]

        validator = RegularExpressionValidator(Regex.FLOAT_UNSIGNED.value)
        enable_validation_list(validator, self._dims)
        validate_list(self._dims)

    @property
    def width(self):
        return float(self._width.text)

    @property
    def height(self):
        return float(self._height.text)

    @property
    def depth(self):
        return float(self._depth.text)

    @property
    def dims(self):
        return [float(i.text) for i in self._dims]

    def validate(self):
        return super().validate() and \
               validate_list(self._dims)


class RegularExpressionValidator(QRegularExpressionValidator):
    def __init__(self, regex=None):
        super().__init__(regex)
        self._tooltip_message = None

    def set_tooltip_message(self, value):
        self._tooltip_message = value

    def get_tooltip_message(self):
        return self._tooltip_message


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
