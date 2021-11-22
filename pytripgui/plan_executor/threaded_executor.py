from threading import Thread
from queue import Queue
from pytripgui.plan_executor.executor import PlanExecutor
from pytripgui.plan_executor.html_executor_logger import HtmlExecutorLogger


class ThreadedExecutor(Thread):
    def __init__(self, plan, patient, trip_config):
        super().__init__()

        self.logger = HtmlExecutorLogger()
        self.item_queue = Queue()

        self.patient = patient
        self.plan = plan
        self.trip_config = trip_config

    def run(self):
        self.on_execute_selected_plan_threaded()

    def on_execute_selected_plan_threaded(self):
        sim_results = self._execute_plan(self.plan, self.patient)
        if sim_results:
            self.item_queue.put(sim_results)

    def _execute_plan(self, plan, patient):
        plan_executor = PlanExecutor(self.trip_config, self.logger)
        item = plan_executor.execute(patient.data, plan.data)
        return item
