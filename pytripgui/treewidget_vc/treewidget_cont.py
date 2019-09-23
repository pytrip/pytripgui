import logging
logger = logging.getLogger(__name__)


class TreeWidgetController:
    def __init__(self, model, view):
        self._patients = model
        self._view = view

        self.synchronize()
        self.synchronize()
        self._view.set_item_clicked_callback(self._item_clicked_callback)

    def synchronize(self):
        self._view.clear()
        for patient in self._patients:
            self._view.add_new_patient(patient)
            if patient.ctx:
                self._view.add_ctx_to_patient(patient, patient.ctx)
            if patient.vdx:
                self._view.add_vdx_to_patient(patient, patient.vdx)
            if patient.plans:
                self._view.add_plans_to_patient(patient, patient.plans)
            #
            # self._model.patient_tree = patient_tree

    def _item_clicked_callback(self, item, patient):
        print(item)
