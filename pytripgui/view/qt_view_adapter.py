from PyQt5.QtWidgets import QMessageBox


class LineEdit:
    def __init__(self, line_edit):
        self._ui = line_edit

    @property
    def text(self):
        return self._ui.text()

    @text.setter
    def text(self, text):
        self._ui.setText(text)

    def emit_on_text_change(self, callback):
        """
        WHen user have changed text in UI, callback will be called with new text:
        callback(new_text)
        """
        self._ui.textChanged.connect(callback)


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

    def _on_item_change_callback(self, current_item):
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
    def count(self):
        return self._ui.count()

    @current_index.setter
    def current_index(self, index):
        self._ui.setCurrentIndex(index)

    @property
    def data(self):
        data = list()
        for i in range(self.count):
            data.append(self._ui.itemData(i))
        return data

    @property
    def current_data(self):
        return self._ui.currentData()

    @property
    def last_data(self):
        return self._ui.itemData(self.last_index)

    @property
    def count(self):
        return self._ui.count()


class UserInfoBox:
    def __init__(self, parent_ui):
        self._parent_ui = parent_ui

    def show_error(self, name, content):
        QMessageBox.critical(self._parent_ui, name, content)

    def show_info(self, name, content):
        QMessageBox.information(self._parent_ui, name, content)