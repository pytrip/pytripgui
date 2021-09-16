from typing import Optional

from pytripgui.canvas_vc.gui_state import PatientGuiState
from pytripgui.plan_vc.plan_view import PlanQtView
from pytripgui.plan_vc.plan_cont import PlanController
from pytripgui.field_vc.field_view import FieldQtView
from pytripgui.field_vc.field_cont import FieldController
from pytripgui.empty_patient_vc.empty_patient_view import EmptyPatientQtView
from pytripgui.empty_patient_vc.empty_patient_cont import EmptyPatientController
from pytripgui.app_logic.viewcanvas import ViewCanvases

from pytripgui.tree_vc.tree_items import PatientItem, PlanItem, FieldItem, TreeItem
from pytripgui.tree_vc.tree_items import SimulationResultItem

from pytripgui.messages import InfoMessages
from pytripgui.app_logic.charts import Charts

from pytripgui.app_logic.gui_executor import GuiExecutor

from pytripgui.view.qt_gui import UiAddPatient
from pytripgui.view.execute_config_view import ExecuteConfigView

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

    def add_empty_patient(self) -> None:
        patient = PatientItem()
        if self.open_empty_patient_callback(patient):
            self.app_model.patient_tree.add_new_item(parent_item=None, item=patient)

    def on_open_voxelplan(self) -> None:
        patient = PatientItem()
        if self.open_voxelplan_callback(patient):
            self.app_model.patient_tree.add_new_item(parent_item=None, item=patient)

    def on_open_dicom(self) -> None:
        patient = PatientItem()
        if self.open_dicom_callback(patient):
            self.app_model.patient_tree.add_new_item(parent_item=None, item=patient)

    def on_execute_selected_plan(self) -> None:
        item = self.app_model.patient_tree.selected_item()
        if isinstance(item, FieldItem):
            plan = item.parent
        else:
            plan = item

        if not isinstance(plan, PlanItem):
            raise TypeError("You should select Field or Plan")

        patient = self.app_model.patient_tree.selected_item_patient()

        trip_config = ExecuteConfigView(model=self.app_model.trip_configs, ui=self.parent_gui.ui)
        trip_config.show()
        if not trip_config.config:
            return

        executor = GuiExecutor(trip_config=trip_config.config, patient=patient, plan=plan,
                               result_callback=self._execute_finish_callback, parent_view=self.parent_gui.ui)

        executor.start()
        executor.show()

    def _execute_finish_callback(self, item: TreeItem) -> None:
        self.app_model.patient_tree.add_new_item(parent_item=None, item=item)

    def on_add_new_plan(self) -> None:
        selected_patient = self.app_model.patient_tree.selected_item_patient()
        if not selected_patient:
            self.parent_gui.show_info(*InfoMessages["addNewPatient"])
            return

        self.new_item_callback(selected_patient)

    def on_kernels_configurator(self) -> None:
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

    def on_trip98_config(self) -> None:
        """
        Config menu opened from window->Settings->TRiP98 Config
        """
        logger.debug("TRiP config menu()")

        from pytripgui.config_vc import ConfigController
        view = self.parent_gui.get_trip_config_view()

        config = self.app_model.trip_configs
        controller = ConfigController(config, view)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            self.app_model.trip_configs = controller.model
            self.settings.save()

    def on_add_patient(self) -> None:
        dialog = UiAddPatient(self.parent_gui.ui)
        dialog.on_create_empty = self.add_empty_patient
        dialog.on_open_voxelplan = self.on_open_voxelplan
        dialog.on_open_dicom = self.on_open_dicom
        dialog.show()

    def on_create_field(self) -> None:
        field = FieldItem()
        save_field = self.edit_field(field)
        if save_field:
            selected_item = self.app_model.patient_tree.selected_item()
            if isinstance(selected_item, PlanItem):
                selected_plan = selected_item
            elif isinstance(selected_item, FieldItem):
                selected_plan = selected_item.parent
            self.app_model.patient_tree.add_new_item(parent_item=selected_plan, item=field)

    def new_item_callback(self, parent: Optional[TreeItem]) -> None:
        """
        Adds a new tree item. Its type is inferred from the type of the parent item
        using the hierarchy of PatientItem > PlanItem > FieldItem.

        Parameters:
        parent (Optional[TreeItem]): A parent item the new item will belong to, or None if a new patient is to be added.

        Returns:
        Nothing
        """
        if parent is None:
            self.add_empty_patient()
        elif isinstance(parent, PatientItem):
            plan = self.edit_plan(PlanItem(), parent)
            self.app_model.patient_tree.add_new_item(parent_item=parent, item=plan)
        elif isinstance(parent, PlanItem):
            field = self.edit_field(FieldItem())
            self.app_model.patient_tree.add_new_item(parent_item=parent, item=field)

    def edit_item_callback(self, item: TreeItem, patient: PatientItem) -> None:
        """
        Handles an edit action on any TreeItem with its specific behavior by triggering a dedicated callback.

        Returns:
        Nothing
        """
        if isinstance(item, PatientItem):
            return
        if isinstance(item, PlanItem):
            self.edit_plan(item, patient)
        elif isinstance(item, FieldItem):
            self.edit_field(item)

    def edit_plan(self, item: PlanItem, patient: PatientItem) -> Optional[PlanItem]:
        """
        Open a plan configuration window, allowing a user to interactively change a plan's parameters.

        Parameters:
        item (PlanItem): the plan item that will be edited.
        patient (PatientItem): the patient this plan is related to.

        Returns:
        PlanItem: the plan item with newly edited parameters
            or
        Nothing: when changes were cancelled or failed
        """
        logger.debug("edit_plan()".format())

        if not patient.data.vdx:
            self.parent_gui.show_info(*InfoMessages["loadCtxVdx"])
            return None

        if not item.data.basename:
            item.data.basename = patient.data.name

        view = PlanQtView(self.parent_gui.ui)

        controller = PlanController(item.data, view, self.app_model.kernels, patient.data.vdx.vois)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            return item
        return None

    def edit_field(self, item: FieldItem) -> Optional[FieldItem]:
        """
        Open a field configuration window, allowing a user to interactively change a field's parameters.

        Parameters:
        item (FieldItem): the field item that will be edited.

        Returns:
        FieldItem: the field item with newly edited parameters
            or
        Nothing: when changes were cancelled or failed
        """
        logger.debug("edit_field()".format())

        view = FieldQtView(self.parent_gui.ui)

        item.data.basename = "field"
        controller = FieldController(item.data, view, self.app_model.kernels)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            return item
        return None

    def open_empty_patient_callback(self, patient_item: PatientItem) -> bool:
        """
        Open an empty patient creation window, allowing the user to interactively set patient parameters.

        Parameters:
        patient_item (PatientItem): Patient item that will contain the newly created patient.

        Returns:
        bool: Whether empty patient creation was successful.
        """
        patient = patient_item.data

        view = EmptyPatientQtView(self.parent_gui.ui)
        controller = EmptyPatientController(patient, view)
        view.show()

        if not controller.is_accepted:
            return False

        patient = controller.model

        if not self.app_model.viewcanvases:
            self.app_model.viewcanvases = ViewCanvases()
            self.parent_gui.add_widget(self.app_model.viewcanvases.widget())

        # someone needs to test this, but I think it's unnecessary,
        #   because after that callback another event is emitted, which sets patient one more time
        # self.app_model.viewcanvases.set_patient(patient)
        return True

    def open_voxelplan_callback(self, patient_item: PatientItem) -> bool:
        """
        Open a file name selection window, then load patient data from Voxelplan files
        with the selected path and basename.

        Parameters:
        patient_item (PatientItem): The patient item to load Vocelplan data into.

        Returns:
        bool: Whether loading Voxelplan data was successful.
        """
        path = self.parent_gui.browse_file_path("Open Voxelpan", "Voxelplan (*.hed)")
        filename, _ = os.path.splitext(path)

        if not filename:
            return False

        patient = patient_item.data
        patient.open_ctx(filename + ".ctx")  # Todo catch exceptions
        try:
            patient.open_vdx(filename + ".vdx")  # Todo catch more exceptions
        except FileNotFoundError:
            logger.warning("Loaded patient has no VOI data")
            # TODO add empty vdx init if needed
            patient.vdx = None

        if not self.app_model.viewcanvases:
            self.app_model.viewcanvases = ViewCanvases()
            self.parent_gui.add_widget(self.app_model.viewcanvases.widget())

        # someone needs to test this, but I think it's unnecessary,
        #   because after that callback another event is emitted, which sets patient one more time
        # self.app_model.viewcanvases.set_patient(patient)
        return True

    def open_dicom_callback(self, patient_item: PatientItem) -> bool:
        """
        Open a folder selection window, then load patient data from DICOM files in the selected folder.

        Parameters:
        patient_item (PatientItem): The patient item to load DICOM data into.

        Returns:
        bool: Whether loading DICOM data was successful.
        """
        logger.debug("Open DICOM start")
        dir_name = self.parent_gui.browse_folder_path("Open DICOM folder")

        if not dir_name:
            return False

        logger.debug("Open DICOM by patient start")

        patient = patient_item.data
        patient.open_dicom(dir_name)  # Todo catch exceptions

        if not self.app_model.viewcanvases:
            self.app_model.viewcanvases = ViewCanvases()
            self.parent_gui.add_widget(self.app_model.viewcanvases.widget())

        # someone needs to test this, but I think it's unnecessary,
        #   because after that callback another event is emitted, which sets patient one more time
        # self.app_model.viewcanvases.set_patient(patient)
        return True

    def export_patient_voxelplan_callback(self, patient_item: PatientItem) -> bool:
        """
        Export patient cube to Voxelplan format (.hed, .ctx, .vdx) with the selected name.

        Parameters:
        patient_item (PatientItem): Patient tree item containing the patient's data

        Returns:
        bool: Whether export was successful
        """
        logger.debug("Voxelplan export start.")
        full_path = self.parent_gui.save_file_path("Export patient to Voxelplan", "Voxelplan (*.hed)")

        if not full_path:
            return False

        path_base, _extension = os.path.splitext(full_path)
        path, basename = os.path.split(path_base)
        logger.info("Voxelplan export to: " + path + " with plan basename: " + basename)

        patient_item.data.ctx.write(os.path.join(path, basename + patient_item.data.ctx.data_file_extension))
        if patient_item.data.vdx:
            patient_item.data.vdx.write(os.path.join(path, basename + patient_item.data.vdx.data_file_extension))
        else:
            logger.warning("Exported patient has no VOI.")

        logger.debug("Voxelplan export finished.")
        return True

    def export_patient_dicom_callback(self, patient_item: PatientItem) -> bool:
        """
        Export patient cube to DICOM format in the selected folder.

        Parameters:
        patient_item (PatientItem): Patient tree item containing the patient's data

        Returns:
        bool: Whether export was successful
        """
        logger.debug("DICOM export start.")
        full_path = self.parent_gui.browse_folder_path("Export patient to DICOM")

        if not full_path:
            return False

        logger.info("DICOM export to: " + full_path)

        patient_item.data.ctx.write_dicom(full_path)
        if patient_item.data.vdx:
            patient_item.data.vdx.write_dicom(full_path)
        else:
            logger.warning("Exported patient has no VOI.")

        logger.debug("DICOM export finished.")
        return True

    def one_click_callback(self) -> None:
        """
        Handles a click action on any TreeItem with its specific behavior.
        This includes displaying the correct data in the canvas and enabling the correct UI buttons.

        Returns:
        Nothing
        """
        self.parent_gui.action_create_field_set_enable(False)
        self.parent_gui.action_create_plan_set_enable(False)
        self.parent_gui.action_execute_plan_set_enable(False)

        item = self.app_model.patient_tree.selected_item()
        top_item = self.app_model.patient_tree.selected_item_patient()

        if isinstance(top_item, SimulationResultItem):
            self.app_model.viewcanvases.set_simulation_results(simulation_results=top_item.data,
                                                               simulation_item=item.data, state=top_item.state)
            if top_item.state is None:
                top_item.state = self.app_model.viewcanvases.get_gui_state()
            self.chart.set_simulation_result(simulation_result=top_item.data)
        elif isinstance(item, PatientItem):
            self.parent_gui.action_create_plan_set_enable(True)
            self._show_patient(top_item, top_item)
        elif isinstance(item, PlanItem):
            self.parent_gui.action_create_plan_set_enable(True)
            self.parent_gui.action_create_field_set_enable(True)
            self._show_patient(top_item, item)
        elif isinstance(item, FieldItem):
            self.parent_gui.action_create_plan_set_enable(True)
            self.parent_gui.action_create_field_set_enable(True)
            self._show_patient(top_item, item)
        if self.is_executable(item):
            self.parent_gui.action_execute_plan_set_enable(True)

    def _show_patient(self, data_item: PatientItem, state_item: PatientGuiState) -> None:
        """
        Displays the data of a patient in the canvas according to the GUI state provided.

        Parameters:
        data_item (PatientItem): The patient tree item to display.
        state_item (PatientGuiState): The GUI state data of the selected patient.

        Returns:
        Nothing.
        """
        if self.app_model.viewcanvases:
            self.app_model.viewcanvases.set_patient(patient=data_item.data, state=state_item.state)

            # set state of plot when plotting first time
            if state_item.state is None:
                state_item.state = self.app_model.viewcanvases.get_gui_state()

            # hide VOI list
            if not data_item.data.vdx or not data_item.data.vdx.vois:
                logger.debug("no VOI data present, hiding VOI list control")
                self.app_model.viewcanvases.viewcanvas_view.voi_list_empty(True)
            else:
                self.app_model.viewcanvases.viewcanvas_view.voi_list_empty(False)

    def patient_tree_show(self) -> None:
        """
        Updates the visibility of the patient tree according to the "View -> Patient Tree" setting.

        Returns:
        Nothing
        """
        self.app_model.patient_tree.set_visible(self.parent_gui.action_open_tree_checked)

    @staticmethod
    def is_executable(item: TreeItem) -> bool:
        """
        Assert whether an item on the patient tree can be executed.
        Execution is possible on plans which have

        Parameters:
        item (TreeItem): The patient tree item in question.

        Returns:
        bool: Whether the item can be executed.
        """
        if isinstance(item, PlanItem):
            # a plan which has children - fields
            if item.has_children():
                return True
        elif isinstance(item, FieldItem):
            # a field item belonging to a plan
            return True
        # not a plan or a plan without fields
        return False
