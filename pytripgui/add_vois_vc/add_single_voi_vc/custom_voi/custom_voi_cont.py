import math

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import logging
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

# TODO replace text on buttons wiht icons, shape creation (circles), add confirmation dialogs and info popups,
#  add the upper and lower slice visible in the background, popup when mousing over a point showing its coords,
#  add units, clean up code and add more comments, reset info label after each action, add info to the previous dialog
#  when there's not even a single slice, center the drawing area;
#  maybe: moving around points/contours, rotating contours/slices, colouring contours, importing of slices in some form


class CustomVOIController:
    def __init__(self, model, view, voi_limits, center):
        self.model = model
        self.view = view
        self.voi_dimensions = voi_limits
        self.center = center

        self._prepare_slices()
        self._prepare_drawing_area()

        self.is_new_contour = False

        self.last_closest_point = None

        self._undo_redo_stack = UndoRedoStack(self.view.undo_button, self.view.redo_button)

        self._setup_callbacks()
        self._set_validators()
        self.is_accepted = False

    def _setup_callbacks(self) -> None:
        self.view.accept_buttons.accepted.disconnect()
        self.view.accept_buttons.accepted.connect(self._save_and_exit)

        self.view.new_contour_button.emit_on_click(lambda: self._new_contour())

        self.view.up_slice_button.emit_on_click(lambda: self._up_slice_changed())
        self.view.top_slice_button.emit_on_click(lambda: self._top_slice_changed())
        self.view.down_slice_button.emit_on_click(lambda: self._down_slice_changed())
        self.view.bottom_slice_button.emit_on_click(lambda: self._bottom_slice_changed())
        self.view.slice_index.emit_on_text_change(self._slice_index_changed)

        self.view.clear_slice_button.emit_on_click(lambda: self._clear_slice())
        self.view.clear_all_button.emit_on_click(lambda: self._clear_all())

        self.view.extend_up_button.emit_on_click(lambda: self._extend_up())
        self.view.extend_down_button.emit_on_click(lambda: self._extend_down())

        self.view.add_point_button.emit_on_click(lambda: self._input_point())

        self.view.undo_button.emit_on_click(lambda: self._undo())
        self.view.redo_button.emit_on_click(lambda: self._redo())

        self.canvas.mpl_connect("motion_notify_event", self._on_move)
        self.canvas.mpl_connect("button_press_event", self._on_click)

    def _prepare_slices(self) -> None:
        self.current_slice_index = 0
        # TODO probably not working fully correctly
        self.voi_slice_number = int(self.voi_dimensions[2] // self.model.slice_distance)
        if self.center[2] % self.model.slice_thickness:
            self.voi_slice_number -= 1

        # TODO probably make a separate structure
        self.slices = [[[]] for _ in range(self.voi_slice_number)]

        self.view.slice_min.text = 0
        self.view.slice_max.text = self.voi_slice_number - 1

    def _prepare_drawing_area(self) -> None:
        self.draw_area_size = self.voi_dimensions[0]

        self.figure = plt.figure()

        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.canvas.setMaximumSize(500, 500)

        self.ax = self.figure.add_subplot()
        self.ax.axis("square")
        self.ax.yaxis.set_ticks_position('both')
        self.ax.xaxis.set_ticks_position('both')
        self.ax.set_xlim(self.center[0] - self.draw_area_size / 2, self.center[0] + self.draw_area_size / 2)
        self.ax.set_ylim(self.center[0] - self.draw_area_size / 2, self.center[0] + self.draw_area_size / 2)
        self.figure.tight_layout()

        self.view.draw_layout.insertWidget(0, self.canvas)

        self.point_size = 5

    def _set_validators(self) -> None:
        validator = QIntValidator(0, self.voi_slice_number - 1)
        self.view.slice_index.enable_validation(validator)

        validator = QIntValidator()
        validator.setBottom(0)
        self.view.extend_slice.enable_validation(validator)

    def _save_and_exit(self) -> None:
        if self._validate_slices():
            self.is_accepted = True
            self.view.accept()

    def _validate_slices(self) -> bool:
        is_processing_voi = False
        is_processing_voi_done = False
        for slice_content in self.slices:
            if slice_content[0]:
                if is_processing_voi_done:
                    self.view.info.text = "There can't be an empty slice between two non-empty ones."
                    return False
                else:
                    is_processing_voi = True
            else:
                if is_processing_voi:
                    is_processing_voi_done = True

        if not is_processing_voi:
            self.view.info.text = "VOI can't be empty."
            return False
        return True

    def _new_contour(self) -> None:
        # if the last contour is non-empty, otherwise there's no point in creating a new one
        if self.slices[self.current_slice_index][-1]:
            self.is_new_contour = True

    def _up_slice_changed(self) -> None:
        if self.current_slice_index < self.voi_slice_number - 1:
            self._change_slice(self.current_slice_index + 1)

    def _top_slice_changed(self) -> None:
        if self.current_slice_index != self.voi_slice_number - 1:
            self._change_slice(self.voi_slice_number - 1)

    def _down_slice_changed(self) -> None:
        if self.current_slice_index > 0:
            self._change_slice(self.current_slice_index - 1)

    def _bottom_slice_changed(self) -> None:
        if self.current_slice_index != 0:
            self._change_slice(0)

    def _slice_index_changed(self, index) -> None:
        # TODO if text not empty
        if index:
            self.current_slice_index = int(index)
            self._draw_slice()

    def _change_slice(self, new_slice) -> None:
        self.current_slice_index = new_slice
        self.view.slice_index.text = self.current_slice_index
        self._draw_slice()

    def _clear_slice(self) -> None:
        action = ActionClearSlice(self.current_slice_index, self.slices[self.current_slice_index])
        self._undo_redo_stack.append(action)

        self.slices[self.current_slice_index] = [[]]
        self._draw_slice()

    # TODO add confirmation dialog
    def _clear_all(self) -> None:
        action = ActionClearAll(self.slices)
        self._undo_redo_stack.append(action)

        self.slices = [[[]] for _ in range(self.voi_slice_number)]
        self._draw_slice()

    def _extend_up(self) -> None:
        if self.view.extend_slice.text:
            extend_by = int(self.view.extend_slice.text)
            if extend_by > self.voi_slice_number - 1 - self.current_slice_index:
                extend_by = self.voi_slice_number - 1 - self.current_slice_index

            action = ActionExtend(self.current_slice_index, extend_by,
                                  self.slices[self.current_slice_index + 1: self.current_slice_index + extend_by + 1])
            self._undo_redo_stack.append(action)

            self._extend(int(self.view.extend_slice.text))

    def _extend_down(self) -> None:
        if self.view.extend_slice.text:
            extend_by = -int(self.view.extend_slice.text)
            if abs(extend_by) > self.current_slice_index:
                extend_by = -self.current_slice_index

            action = ActionExtend(self.current_slice_index, extend_by,
                                  self.slices[self.current_slice_index + extend_by: self.current_slice_index])
            self._undo_redo_stack.append(action)

            self._extend(-int(self.view.extend_slice.text))

    # TODO add confirmation dialog in case of overwriting non-empty slices
    def _extend(self, extend_by) -> None:
        if extend_by > 0:
            slice_start = self.current_slice_index + 1
            slice_finish = self.current_slice_index + extend_by + 1
        else:
            slice_start = self.current_slice_index + extend_by
            slice_finish = self.current_slice_index

        for slice_index in range(slice_start, slice_finish):
            self.slices[slice_index] = self.slices[self.current_slice_index].copy()

        self.view.extend_slice.text = 0

    def _undo(self) -> None:
        self._undo_redo_stack.undo(self)

    def _redo(self) -> None:
        self._undo_redo_stack.redo(self)

    def _on_move(self, event) -> None:
        if event.xdata is not None:
            point = [event.xdata, event.ydata]
            closest_point = self._get_closest_point(point)

            # highlight the possibility of closing a contour and make it easier to click onto
            if closest_point and closest_point == self.slices[self.current_slice_index][-1][0] and \
                    len(self.slices[self.current_slice_index][-1]) >= 3 and \
                    math.hypot(closest_point[0] - point[0], closest_point[1] - point[1]) <= self.draw_area_size * 0.02:
                self._draw_point(closest_point, "green")
                self.last_closest_point = closest_point
            else:
                if self.last_closest_point:
                    self._draw_point(self.last_closest_point, "blue")
                    self.last_closest_point = None

            self.canvas.draw()

    def _on_click(self, event) -> None:
        if self.last_closest_point:
            point = self.last_closest_point
        else:
            point = [event.xdata, event.ydata]

        action_is_new_contour = self.is_new_contour
        if self.is_new_contour:
            self._add_contour()
            self.is_new_contour = False

        self._add_point(point)
        action = ActionAddPoint(self.current_slice_index, point, action_is_new_contour)
        self._undo_redo_stack.append(action)

    def _input_point(self) -> None:
        # TODO add validation
        point = [float(self.view.point_x.text), float(self.view.point_y.text)]
        action_is_new_contour = self.is_new_contour
        if self.is_new_contour:
            self._add_contour()
            self.is_new_contour = False
        self._add_point(point)
        action = ActionAddPoint(self.current_slice_index, point, action_is_new_contour)
        self._undo_redo_stack.append(action)

    def _add_point(self, point):
        # if the contour is not empty, i.e. we're drawing a line segment
        if self.slices[self.current_slice_index][-1]:
            last_point = self.slices[self.current_slice_index][-1][-1]
            # TODO maybe allow intersections and just add a point at the intersection
            if self._are_any_intersecting(last_point, point):
                # TODO show message about problem
                return
            self._draw_line(last_point, point)
            self._draw_point(last_point, "blue")
            # if closing the contour, prepare a new one
            if point == self.slices[self.current_slice_index][-1][0]:
                self.is_new_contour = True
            else:
                self._draw_point(point, "red")
        else:
            self._draw_point(point, "red")

        # add to current slice, latest contour
        self.slices[self.current_slice_index][-1].append(point)

        self.canvas.draw()

    def _remove_last_point(self):
        # reset contour creation
        self.is_new_contour = False
        # from the latest contour
        self.slices[self.current_slice_index][-1].pop()
        self._draw_slice()

    def _get_closest_point(self, a) -> list:
        smallest_distance = float("inf")
        closest_point = None
        for contour in self.slices[self.current_slice_index]:
            for b in contour:
                distance = math.hypot(a[0] - b[0], a[1] - b[1])
                if distance < smallest_distance:
                    closest_point = b
                    smallest_distance = distance
        return closest_point

    def _add_contour(self) -> None:
        self.slices[self.current_slice_index].append([])
        # TODO not the best idea
        self._draw_slice()

    def _remove_last_contour(self):
        self.slices[self.current_slice_index].pop()
        # TODO not the best idea
        self._draw_slice()

    def _replace_slice(self, slice_index, slice_contents) -> None:
        self.slices[slice_index] = slice_contents
        if slice_index == self.current_slice_index:
            self._draw_slice()

    def _draw_slice(self) -> None:
        self.ax.clear()
        self.ax.set_xlim(self.center[0] - self.draw_area_size / 2, self.center[0] + self.draw_area_size / 2)
        self.ax.set_ylim(self.center[0] - self.draw_area_size / 2, self.center[0] + self.draw_area_size / 2)

        for contour in self.slices[self.current_slice_index]:
            if len(contour):
                point_a = contour[0]
                for point_b in contour[1:]:
                    self._draw_line(point_a, point_b)
                    self._draw_point(point_a, "blue")
                    point_a = point_b
                self._draw_point(point_a, "blue")

        if self.slices[self.current_slice_index][-1] and \
                (self.slices[self.current_slice_index][-1][-1] != self.slices[self.current_slice_index][-1][0] or
                 len(self.slices[self.current_slice_index][-1]) == 1):
            self._draw_point(self.slices[self.current_slice_index][-1][-1], "red")

        self.canvas.draw()

    def _draw_point(self, point, color) -> None:
        self.ax.plot(point[0], point[1], marker="o", markersize=self.point_size, color=color)

    def _draw_line(self, point_a, point_b) -> None:
        self.ax.plot([point_a[0], point_b[0]], [point_a[1], point_b[1]], color="black")

    def _are_any_intersecting(self, a1, a2) -> bool:
        for contour in self.slices[self.current_slice_index]:
            # ignoring last point
            if len(contour) >= 3:
                b1 = contour[0]
                for b2 in contour[1:-1]:
                    # TODO overhaul
                    # allow sharing of points between line segments
                    if a1 not in [b1, b2] and a2 not in [b1, b2] and are_intersecting(a1, a2, b1, b2):
                        return True
                    b1 = b2
        return False

    def get_slices(self) -> list:
        return self.slices


def ccw(a, b, c) -> bool:
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


def are_intersecting(a1, a2, b1, b2) -> bool:
    return ccw(a1, b1, b2) != ccw(a2, b1, b2) and ccw(a1, a2, b1) != ccw(a1, a2, b2)


class Action:
    def __init__(self, slice_indexes=0):
        if not isinstance(slice_indexes, list):
            slice_indexes = [slice_indexes]
        self.slice_indexes = slice_indexes

    @property
    def slice_index(self) -> int:
        return self.slice_indexes[0]

    def undo(self, executor) -> None:
        raise NotImplementedError("Undo not implemented.")

    def redo(self, executor) -> None:
        raise NotImplementedError("Redo not implemented.")


class ActionClearSlice(Action):
    def __init__(self, slice_index, slice_content):
        super().__init__(slice_index)
        self.slice_content = slice_content

    def undo(self, executor) -> None:
        getattr(executor, "_replace_slice")(self.slice_index, self.slice_content)

    def redo(self, executor) -> None:
        getattr(executor, "_clear_slice")()


class ActionClearAll(Action):
    def __init__(self, slice_contents):
        super().__init__()
        self.slice_contents = slice_contents

    def undo(self, executor) -> None:
        for slice_index, slice_contents in enumerate(self.slice_contents):
            getattr(executor, "_replace_slice")(slice_index, slice_contents)

    def redo(self, executor) -> None:
        getattr(executor, "_clear_all")()


class ActionAddPoint(Action):
    def __init__(self, slice_index, point, is_new_contour):
        super().__init__(slice_index)
        self.point = point
        self.is_new_contour = is_new_contour

    def undo(self, executor) -> None:
        getattr(executor, "_remove_last_point")()
        if self.is_new_contour:
            getattr(executor, "_remove_last_contour")()

    def redo(self, executor) -> None:
        if self.is_new_contour:
            getattr(executor, "_add_contour")()
        getattr(executor, "_add_point")(self.point)


class ActionExtend(Action):
    def __init__(self, slice_index, extend_by, slice_contents):
        super().__init__(slice_index)
        self.extend_by = extend_by
        self.slice_contents = slice_contents

    def undo(self, executor) -> None:
        if self.extend_by > 0:
            affectted_slice_indexes = range(self.slice_index + 1, self.slice_index + self.extend_by + 1)
        else:
            affectted_slice_indexes = range(self.slice_index + self.extend_by, self.slice_index)

        for slice_contents_index, affected_slice_index in enumerate(affectted_slice_indexes):
            getattr(executor, "_replace_slice")(affected_slice_index, self.slice_contents[slice_contents_index])

    def redo(self, executor) -> None:
        getattr(executor, "_extend")(self.extend_by)


class UndoRedoStack:
    def __init__(self, undo_button, redo_button):
        self._undo_stack = []
        self._redo_stack = []
        self._undo_button = undo_button
        self._redo_button = redo_button
        self._undo_button.set_enabled(False)
        self._redo_button.set_enabled(False)

    def undo(self, executor) -> None:
        if self._undo_stack:
            action = self._undo_stack.pop()
            getattr(executor, "_change_slice")(action.slice_index)
            action.undo(executor)
            self._redo_stack.append(action)

            self._redo_button.set_enabled(True)
            if not self._undo_stack:
                self._undo_button.set_enabled(False)

    def redo(self, executor) -> None:
        if self._redo_stack:
            action = self._redo_stack.pop()
            getattr(executor, "_change_slice")(action.slice_index)
            action.redo(executor)
            self._undo_stack.append(action)

            self._undo_button.set_enabled(True)
            if not self._redo_stack:
                self._redo_button.set_enabled(False)

    def append(self, action) -> None:
        self._undo_stack.append(action)
        # limit the size of the stack
        if len(self._undo_stack) > 100:
            self._undo_stack.pop(0)
        self._redo_stack = []
        self._undo_button.set_enabled(True)
