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


class ComboBox:
    def __init__(self, combo_box):
        self._ui = combo_box
        self.last_index = 0
        self.current_index = 0

        self._on_item_change_user_callback = None
        self._ui.currentIndexChanged.connect(self._on_item_change_callback)

    def fill(self, combo_list, lambda_names):
        self._ui.clear()
        for item in combo_list:
            self._ui.addItem(lambda_names(item), item)

    def emit_on_item_change(self, callback):
        self._on_item_change_user_callback = callback

    def _on_item_change_callback(self, current_item):
        self.last_index = self.current_index
        self.current_index = current_item

        if self._on_item_change_user_callback:
            self._on_item_change_user_callback()

    def set_current_item_text(self, text):
        self._ui.setItemText(self.current_index, text)
