class LineEdit:
    def __init__(self, line_edit):
        self._ui = line_edit

    @property
    def text(self):
        return self._ui.text()

    @text.setter
    def text(self, text):
        self._ui.setText(text)


class ComboBox:
    def __init__(self, combo_box):
        self._ui = combo_box

    def fill(self, combo_list, lambda_names):
        self._ui.clear()
        for item in combo_list:
            self._ui.addItem(lambda_names(item), item)

    def emit_on_item_change(self, callback):
        self._ui.currentIndexChanged.connect(callback)
