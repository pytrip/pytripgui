import logging
logger = logging.getLogger(__name__)


class TreeWidgetController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

        self.synchronize()

    def synchronize(self):
        for patient in self._model:

            patient_tree = self._view.init_widget(patient.tree_model)
            # self._view.add_ctx_to_patient(patient_tree, patient.ctx)
            #
            # self._model.patient_tree = patient_tree
