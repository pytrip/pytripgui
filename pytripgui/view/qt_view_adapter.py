from typing import Callable

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QValidator, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem


class LineEdit:
    def __init__(self, line_edit):
        self._ui = line_edit

    @property
    def text(self):
        return self._ui.text()

    @text.setter
    def text(self, text):
        self._ui.setText(str(text))

    def clear(self):
        self._ui.clear()

    def set_enabled(self, enabled):
        self._ui.setEnabled(enabled)

    def emit_on_text_change(self, callback):
        """
        When user have changed text in UI, callback will be called with new text:
        callback(new_text)
        """
        self._ui.textChanged.connect(callback)

    def set_validator(self, validator):
        self._ui.setValidator(validator)

    def enable_validation(self, validator, custom_validation=None):
        self._ui.setValidator(validator)
        if custom_validation:
            self._ui.textChanged.connect(custom_validation)
        else:
            self._ui.textChanged.connect(self.validate)

    def disable_validation(self):
        self._ui.textChanged.disconnect()

    def validate(self):
        if self._ui.validator():
            state = self._ui.validator().validate(self._ui.text(), 0)[0]
            if state == QValidator.Acceptable:
                self.reset_border()
                return True
            self.highlight_border()
        return False

    def highlight_border(self):
        self._ui.setStyleSheet("border: 1px solid red")

    def reset_border(self):
        self._ui.setStyleSheet("")


class LineEditMath(LineEdit):
    @property
    def text(self):
        return self._ui.text().replace(",", ".")

    @text.setter
    def text(self, text):
        self._ui.setText(str(text))


class PushButton:
    def __init__(self, push_button):
        self._ui = push_button

    def emit_on_click(self, callback):
        self._ui.clicked.connect(callback)


class ComboBox:
    def __init__(self, combo_box):
        self._ui = combo_box
        self.last_index = 0

        self._on_item_change_user_callback = None
        self._ui.currentIndexChanged.connect(self._on_item_change_callback)

    def fill(self, combo_list, lambda_names):
        self.last_index = 0
        self._ui.clear()
        for item in combo_list:
            self._ui.addItem(lambda_names(item), item)

    def append_element(self, data, name):
        self._ui.addItem(name, data)
        self.current_index = self.count - 1

    def emit_on_item_change(self, callback):
        self._on_item_change_user_callback = callback

    def _on_item_change_callback(self):
        if self._on_item_change_user_callback:
            self._on_item_change_user_callback()
        self.last_index = self.current_index

    def set_current_item_text(self, text):
        self._ui.setItemText(self.current_index, text)

    def remove_current_item(self):
        self.last_index = -1
        self._ui.removeItem(self.current_index)

    @property
    def current_index(self):
        return self._ui.currentIndex()

    @property
    def current_text(self):
        return self._ui.currentText()

    @property
    def count(self):
        return self._ui.count()

    @current_index.setter
    def current_index(self, index):
        self._ui.setCurrentIndex(index)

    @property
    def data(self):
        data = []
        for i in range(self.count):
            data.append(self._ui.itemData(i))
        return data

    @property
    def current_data(self):
        return self._ui.currentData()

    @property
    def last_data(self):
        return self._ui.itemData(self.last_index)


class UserInfoBox:
    def __init__(self, parent_ui):
        self._parent_ui = parent_ui

    def show_error(self, name, content):
        QMessageBox.critical(self._parent_ui, name, content)

    def show_info(self, name, content):
        QMessageBox.information(self._parent_ui, name, content)


class ListWidget:
    def __init__(self, list_widget, checkable=False):
        self._ui = list_widget
        self._items = []
        self._checkable = checkable

        self.on_list_item_clicked_callback = lambda: None
        self._ui.itemClicked.connect(self._on_item_clicked)

    def fill(self, items, get_name: Callable, get_color: Callable = None):
        self._ui.clear()
        self._items.clear()
        for item in items:
            name = get_name(item)
            q_item = QListWidgetItem(name)
            if get_color:
                size = 13
                image = np.full(shape=(size, size, 3), fill_value=get_color(item), dtype=np.uint8)
                image = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)
                pixmap = QPixmap(image)
                q_item.setIcon(QIcon(pixmap))
            q_item.setData(Qt.UserRole, item)
            if self._checkable:
                q_item.setCheckState(Qt.Unchecked)
            # From 'default item flags' remove flag allowing user to directly change item's checkbox status.
            # The status is exclusively controlled by _on_item_clicked callback,
            #   so if user clicks within list item boundaries (not only checkbox), the status will be changed.
            q_item.setFlags(q_item.flags() & ~Qt.ItemIsUserCheckable)
            # Leaving ItemIsUserCheckable flag enabled, causes problems when user clicks on checkbox
            #   - two callbacks are launched:
            #     - first - controlled by the flag - checks/unchecks checkbox directly,
            #     - second - defined by us (_on_item_clicked) also checks/unchecks checkbox.
            #   In that case user DOES NOT see the change of checkbox status, because
            #       checkbox is checked by first callback and unchecked by second one (or the other way around)
            #       and list of checked items effectively stays unchanged,
            #       while causing side effects (eg. invocation of on_list_item_clicked_callback).
            self._items.append(q_item)
            self._ui.addItem(q_item)

    def ticked_items(self):
        selected = []
        if not self._checkable:
            return selected

        for i in range(self._ui.count()):
            widget = self._ui.item(i)
            if widget.checkState() == Qt.Checked:
                selected.append(widget.data(Qt.UserRole))
        return selected

    def tick_checkboxes(self, items, get_name: Callable):
        item_names = [get_name(item) for item in items]
        for item in self._items:
            if get_name(item.data(Qt.UserRole)) in item_names:
                item.setCheckState(Qt.Checked)

    def _on_item_clicked(self, item):
        # change check state of item that was clicked
        item.setCheckState(Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked)
        # invoke callback
        self.on_list_item_clicked_callback()


class TableWidget:
    def __init__(self, table_widget):
        self._ui = table_widget

    def add_row(self):
        self._ui.insertRow(self.row_count())

    def row_count(self):
        return self._ui.rowCount()

    def col_count(self):
        return self._ui.colCount()

    def item(self, row, col):
        return self._ui.item(row, col)

    def selected_row_index(self):
        if self._ui.selectionModel().hasSelection():
            return self._ui.selectionModel().selectedIndexes()[0].row()
        return -1

    def remove_row(self, index):
        if 0 <= index < self._ui.rowCount():
            self._ui.removeRow(index)

    def is_row_full(self, row):
        for column in range(self._ui.columnCount()):
            if not self._ui.item(row, column):
                return False
        return True


class TabWidget:
    def __init__(self, tab_widget):
        self._ui = tab_widget
        self._previous_index = self._ui.currentIndex()

    @property
    def current_index(self):
        return self._ui.currentIndex()

    @property
    def previous_index(self):
        return self._previous_index

    def update_previous_index(self):
        self._previous_index = self._ui.currentIndex()

    def emit_on_tab_change(self, callback):
        self._ui.currentChanged.connect(callback)


class Label:
    def __init__(self, label):
        self._ui = label

    @property
    def text(self):
        return self._ui.text()

    @text.setter
    def text(self, text):
        self._ui.setText(str(text))
