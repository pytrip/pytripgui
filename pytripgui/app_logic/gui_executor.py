from pytripgui.executor_vc.executor_view import ExecutorQtView

from pytripgui.plan_executor.threaded_executor import ThreadedExecutor
from pytripgui.tree_vc.tree_items import SimulationResultItem
from pytripgui.messages import InfoMessages

from PyQt5.QtCore import QTimer


class GuiExecutor:
    GUI_UPDATE_RATE_MS = 10  # GUI update rate during trip98 execution [ms]

    def __init__(self, trip_config, patient, plan, result_callback, partnt_view):
        if not plan.data.fields:
            partnt_view.show_info(*InfoMessages["addOneField"])
            return

        self.result_callback = result_callback
        self.done = False  # True when object can be removed from memory

        self._gui_update_timer = QTimer()
        self._thread = ThreadedExecutor(plan, patient, trip_config)

        self._ui = ExecutorQtView(partnt_view)

    def show(self):
        self._ui.show()

    def update_gui(self):
        if self._thread.is_alive():
            # if thread is still alive, execute this function in GUI_UPDATE_RATE_MS
            self._gui_update_timer.singleShot(GuiExecutor.GUI_UPDATE_RATE_MS, self.update_gui)
        else:
            self._call_result_callback()
            self._ui.enable_ok_button()
            self.done = True

        while not self._thread.std_out_queue.empty():
            text = self._thread.std_out_queue.get(False)
            self._ui.append_log(text)

    def start(self):
        self._thread.start()
        # update gui in GUI_UPDATE_RATE_MS
        self._gui_update_timer.singleShot(GuiExecutor.GUI_UPDATE_RATE_MS, self.update_gui)

    def _call_result_callback(self):
        if self._thread.item_queue.empty():
            return

        item = SimulationResultItem()
        item.data = self._thread.item_queue.get(False)

        if item.data.dose:
            dose_item = SimulationResultItem()
            dose_item.data = item.data.dose
            item.add_child(dose_item)

        if item.data.let:
            let_item = SimulationResultItem()
            let_item.data = item.data.let
            item.add_child(let_item)

        self.result_callback(item)
