from pytripgui.treewidget_vc.treewidget_cont import TreeWidgetController

from pytripgui.model.patient import Patient

import os

import logging
logger = logging.getLogger(__name__)


class MainWindowController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self._initialize_model()

    def open_files(self, args):
        pass
        # raise Exception("Unimplemented")  # TODO

    def _initialize_model(self):
        # main window
        self.view.open_voxelplan_callback = self.open_voxelplan

        # patients tree module
        patient_tree_view = self.view.get_patient_tree_view()
        self.model.patient_tree_cont = TreeWidgetController(self.model.patients, patient_tree_view)
        self.model.patient_tree_cont.update_selected_item_callback = self.selected_item_callback
        self.model.patient_tree_cont.context_menu.new_patient_callback = self.add_new_patient
        self.model.patient_tree_cont.context_menu.open_voxelplan_callback = self.open_voxelplan

    def selected_item_callback(self, patient, item):
        self.model.current_patient = patient

    def add_new_patient(self):
        new_patient = Patient(self.model.kernels)
        self.model.patients.append(new_patient)
        return new_patient

    def open_voxelplan(self):
        path = self.view.browse_file_path("Open Voxelpan", "Voxelplan (*.hed)")
        filename, extension = os.path.splitext(path)

        if filename == "":
            return

        if self.model.current_patient:
            patient = self.model.current_patient
        else:
            patient = self.add_new_patient()
            self.model.patient_tree_cont.synchronize()

        patient.open_ctx(filename + ".ctx")  # Todo catch exceptions
        patient.open_vdx(filename + ".vdx")  # Todo catch exceptions
        self.model.patient_tree_cont.synchronize()
