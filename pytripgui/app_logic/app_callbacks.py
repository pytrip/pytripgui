from pytripgui.plan_vc.plan_view import PlanQtView
from pytripgui.plan_vc.plan_cont import PlanController
from pytripgui.field_vc.field_view import FieldQtView
from pytripgui.field_vc.field_cont import FieldController
from pytripgui.app_logic.viewcanvas import ViewCanvases

from pytripgui.tree_vc.TreeItems import PatientItem, PlanItem, FieldItem
from pytripgui.tree_vc.TreeItems import SimulationResultItem

from pytripgui.messages import InfoMessages
from pytripgui.app_logic.charts import Charts

from pytripgui.app_logic.gui_executor import GuiExecutor

from pytripgui.view.qt_gui import UiAddPatient

from pytripgui.controller.settings_cont import SettingsController

import os
import logging
logger = logging.getLogger(__name__)


class AppCallback:
    def __init__(self, app_model, parent_gui):
        self.app_model = app_model
        self.parent_gui = parent_gui
        self.chart = Charts(self.parent_gui)

        self.settings = SettingsController(self.app_model)

    def on_open_voxelplan(self):
        patient = PatientItem()
        if self.open_voxelplan_callback(patient):
            self.app_model.patient_tree.add_new_item(None, patient)

    def on_open_dicom(self):
        patient = PatientItem()
        if self.open_dicom_callback(patient):
            self.app_model.patient_tree.add_new_item(None, patient)

    def on_execute_selected_plan(self):
        item = self.app_model.patient_tree.selected_item()
        if isinstance(item, FieldItem):
            plan = item.parent
        else:
            plan = item

        if not isinstance(plan, PlanItem):
            raise TypeError("You should select Field or Plan")

        patient = self.app_model.patient_tree.selected_item_patient()

        executor = GuiExecutor(self.app_model.trip_config, patient, plan,
                               self._execute_finish_callback,
                               self.parent_gui.ui)

        executor.start()
        executor.show()

    def _execute_finish_callback(self, item):
        self.app_model.patient_tree.add_new_item(None, item)

    def on_add_new_plan(self):
        selected_patient = self.app_model.patient_tree.selected_item_patient()
        if not selected_patient:
            self.parent_gui.show_info(*InfoMessages["addNewPatient"])
            return
        self.new_item_callback(selected_patient)

    def on_kernels_configurator(self):
        """
        Kernel dialog opened from window->settings->kernel
        """
        from pytripgui.kernel_vc import KernelController

        model = self.app_model.kernels
        view = self.parent_gui.get_kernel_config_view()

        controller = KernelController(model, view)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            self.settings.save()

    def on_trip98_config(self):
        """
        Config menu opened from window->Settings->TRiP98 Config
        """
        logger.debug("TRiP config menu()")

        from pytripgui.config_vc import ConfigController

        view = self.parent_gui.get_trip_config_view()

        controller = ConfigController(self.app_model.trip_config, view)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            self.settings.save()

    def on_add_patient(self):
        dialog = UiAddPatient(self.parent_gui.ui)
        dialog.on_create_empty = self.add_empty_patient
        dialog.on_open_voxelplan = self.on_open_voxelplan
        dialog.on_open_dicom = self.on_open_dicom
        dialog.show()

    def add_empty_patient(self):
        patient = PatientItem()
        self.app_model.patient_tree.add_new_item(None, patient)

    def on_create_field(self):
        field = FieldItem()
        save_field = self.edit_field(field)
        if save_field:
            selected_item = self.app_model.patient_tree.selected_item()
            if isinstance(selected_item, PlanItem):
                selected_plan = selected_item
            elif isinstance(selected_item, FieldItem):
                selected_plan = selected_item.parent
            self.app_model.patient_tree.add_new_item(selected_plan, field)

    def new_item_callback(self, parent):
        if parent is None:
            self.add_empty_patient()
        elif isinstance(parent, PatientItem):
            plan = self.edit_plan(PlanItem(), parent)
            self.app_model.patient_tree.add_new_item(parent, plan)
        elif isinstance(parent, PlanItem):
            field = self.edit_field(FieldItem())
            self.app_model.patient_tree.add_new_item(parent, field)

    def edit_item_callback(self, item, patient):
        if isinstance(item, PatientItem):
            return
        elif isinstance(item, PlanItem):
            self.edit_plan(item, patient)
        elif isinstance(item, FieldItem):
            self.edit_field(item)

    def edit_plan(self, item, patient):
        logger.debug("edit_plan()".format())

        if not patient.data.vdx:
            self.parent_gui.show_info(*InfoMessages["loadCtxVdx"])
            return False

        item.data.basename = patient.data.name

        view = PlanQtView(self.parent_gui.ui)

        controller = PlanController(item.data, view, self.app_model.kernels,
                                    patient.data.vdx.vois)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            return item
        return None

    def edit_field(self, item):
        logger.debug("edit_field()".format())

        view = FieldQtView(self.parent_gui.ui)

        item.data.basename = "field"
        controller = FieldController(item.data, view, self.app_model.kernels)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            return item
        return None

    def open_voxelplan_callback(self, patient_item):
        path = self.parent_gui.browse_file_path("Open Voxelpan",
                                                "Voxelplan (*.hed)")
        filename, extension = os.path.splitext(path)

        if filename == "":
            return False

        patient = patient_item.data
        patient.open_ctx(filename + ".ctx")  # Todo catch exceptions
        patient.open_vdx(filename + ".vdx")  # Todo catch exceptions

        if not self.app_model.viewcanvases:
            self.app_model.viewcanvases = ViewCanvases()
            self.parent_gui.add_widget(self.app_model.viewcanvases.widget())

        self.app_model.viewcanvases.set_patient(patient)
        return True

    def open_dicom_callback(self, patient_item):
        dir_name = self.parent_gui.browse_folder_path("Open DICOM folder")

        if not dir_name:
            return False

        patient = patient_item.data
        patient.open_dicom(dir_name)  # Todo catch exceptions

        if not self.app_model.viewcanvases:
            self.app_model.viewcanvases = ViewCanvases()
            self.parent_gui.add_widget(self.app_model.viewcanvases.widget())

        self.app_model.viewcanvases.set_patient(patient)
        return True

    def one_click_callback(self, top_item, item):
        self.parent_gui.action_create_field_set_enable(False)
        self.parent_gui.action_create_plan_set_enable(False)
        self.parent_gui.action_execute_plan_set_enable(False)

        if isinstance(top_item, SimulationResultItem):
            self.app_model.viewcanvases.set_simulation_results(top_item.data)
            self.chart.set_simulation_result(top_item.data)
        elif isinstance(top_item, PatientItem):
            self.parent_gui.action_create_plan_set_enable(True)
            if self.app_model.viewcanvases:
                self.app_model.viewcanvases.set_patient(top_item.data)

        if isinstance(item, PlanItem):
            self.parent_gui.action_create_field_set_enable(True)
            if self.is_executable(item):
                self.parent_gui.action_execute_plan_set_enable(True)

        elif isinstance(item, FieldItem):
            self.parent_gui.action_create_field_set_enable(True)
            if self.is_executable(item):
                self.parent_gui.action_execute_plan_set_enable(True)

    @staticmethod
    def is_executable(item):
        if isinstance(item, PlanItem):
            if item.has_children():
                return True
        elif isinstance(item, FieldItem):
            return True

        return False
