import threading
from typing import Optional, Union, Collection

import pytrip.tripexecuter
from PyQt5.QtWidgets import QApplication
from pytrip import DosCube, dicomhelper, Voi

from pytripgui.canvas_vc.gui_state import PatientGuiState
from pytripgui.contouring_vc.contouring_controller import ContouringController
from pytripgui.loading_file_vc.loading_file_controller import LoadingFileController
from pytripgui.plan_executor.simulation_results import SimulationResults
from pytripgui.add_vois_vc import AddVOIsController
from pytripgui.add_vois_vc.add_vois_view import AddVOIsQtView
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
    def __init__(self, app_controller):
        self.app_model = app_controller.model
        self.parent_gui = app_controller.view
        self.app_controller = app_controller

        self.chart = Charts(self.parent_gui)
        self.settings = SettingsController(self.app_model)

    def add_empty_patient(self) -> None:
        """
        Creates a new PatientItem and calls the open_empty_patient_callback on it to create an empty patient.
        If opening is sucessful, adds this patient to the patient tree.

        Returns:
        None
        """
        patient = PatientItem()
        if self.open_empty_patient_callback(patient):
            self.app_model.patient_tree.add_new_item(parent_item=None, item=patient)

    def on_open_voxelplan(self) -> None:
        """
        Displays a file selection dialog window, allowing the user to select a .hed file to load,
        then attempts to create a patient with Voxelplan data loaded from that file.

        Returns:
        None
        """

        path = self.parent_gui.browse_file_path("Open Voxelpan", "Voxelplan (*.hed)")
        logger.debug("Open Voxelplan: {}".format(path))
        progress_dialog: LoadingFileController = LoadingFileController(load_function=self.app_controller.open_voxelplan,
                                                                       function_args=(path,), parent=self.parent_gui.ui,
                                                                       window_title="Open Voxelplan",
                                                                       progress_message="Reading files, please wait...")
        progress_dialog.start()
        progress_dialog.connect_finished(self.show_contouring_dialog)

    def on_open_dicom(self) -> None:
        """
        Displays a directory selection dialog window, allowing the user to select a folder,
        then attempts to create a patient with DICOM data loaded from that folder.

        Returns:
        None
        """
        dir_path = self.parent_gui.browse_folder_path("Open DICOM folder")
        logger.debug("Open DICOM: {}".format(dir_path))
        # self.app_controller.open_dicom(dir_path)
        progress_dialog = LoadingFileController(load_function=self.app_controller.open_dicom, function_args=(dir_path,),
                                                parent=self.parent_gui.ui, window_title="Open DICOM",
                                                progress_message="Reading files, please wait...")
        progress_dialog.start()
        progress_dialog.connect_finished(self.show_contouring_dialog)

    def show_contouring_dialog(self):
        patient: PatientItem = self.app_model.patient_tree.selected_item_patient()
        vois: Collection[Voi] = patient.data.vdx.vois
        contouring_dialog: ContouringController = ContouringController(vois=vois, parent=self.parent_gui.ui)
        contouring_dialog.show()

    def on_execute_selected_plan(self) -> None:
        """
        Displays a popup window to select a TRiP configuration to use during plan execution,
        then executes the selected PlanItem selected on the tree, or the plan to which the selected Fielditem belongs.
        If the TRiP configuration selection is aborted, so is the execution.

        Raises:
        TypeError: if the selected item is neither a plan nor a field

        Returns:
        None
        """
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

    def _execute_finish_callback(self, item: TreeItem, patient: PatientItem = None) -> None:
        """
        Add a new item to the patient tree, containing the plan execution results.

        Returns:
        None
        """
        self.app_model.patient_tree.add_new_item(parent_item=patient, item=item)

    def on_add_new_plan(self) -> None:
        """
        Add a new plan item to the patient tree, belonging to the currently selected patient.
        If no patient is selected, display an error popup.

        Returns:
        None
        """
        selected_patient = self.app_model.patient_tree.selected_item_patient()
        if not selected_patient:
            self.parent_gui.show_info(*InfoMessages["addNewPatient"])
            return

        self.new_item_callback(selected_patient)

    def on_kernels_configurator(self) -> None:
        """
        Open the beam kernel configuration dialog window and if user chose to, save the resulting configuration.

        Returns:
        None
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
        Open the TRiP98 configuration dialog window and if user chose to, save the resulting configuration.

        Returns:
        None
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
        """
        Open a dialog window allowing the user to select the type of patient they want to add.

        Returns:
        None
        """
        dialog = UiAddPatient(self.parent_gui.ui)
        dialog.on_create_empty = self.add_empty_patient
        dialog.on_open_voxelplan = self.on_open_voxelplan
        dialog.on_open_dicom = self.on_open_dicom
        dialog.show()

    def on_add_vois(self):
        selected_patient = self.app_model.patient_tree.selected_item_patient()
        if not selected_patient:
            self.parent_gui.show_info(*InfoMessages["addNewPatient"])
            return

        view = AddVOIsQtView(self.parent_gui.ui)
        controller = AddVOIsController(selected_patient.data, view)

        view.show()

        if controller.is_accepted:
            if selected_patient.data.vdx and selected_patient.data.vdx.vois:
                self.app_model.viewcanvases.update_voi_list(selected_patient.data, selected_patient.state)
                self.app_model.viewcanvases.viewcanvas_view.voi_list_empty(False)

    def on_create_field(self) -> None:
        """
        Create a new field item, then call the edit_field callback to let the user interactively set its parameters.
        If this is successful, add this new field item to the patient tree, under the currently selected plan,
        or the plan that the currently selected field item belongs to.

        Returns:
        None
        """
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
        None
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
        Handles an edit action on any TreeItem with its specific behavior by invoking a dedicated callback.

        Returns:
        None
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
        None: when changes were cancelled or failed
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
        None: when changes were cancelled or failed
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
            self.app_model.viewcanvases = ViewCanvases(self.parent_gui.ui)
            self.parent_gui.add_widget(self.app_model.viewcanvases.widget())

        # someone needs to test this, but I think it's unnecessary,
        #   because after that callback another event is emitted, which sets patient one more time
        # self.app_model.viewcanvases.set_patient(patient)
        return True

    def export_patient_voxelplan_callback(self, patient_item: PatientItem) -> bool:
        """
        Open a file name selection window, then export the patient cube to Voxelplan format (.hed, .ctx, .vdx)
        with the selected name.

        Parameters:
        patient_item (PatientItem): Patient tree item containing the patient's data

        Returns:
        bool: Whether export was successful
        """
        logger.debug("Voxelplan export start.")
        full_path = self.parent_gui.save_file_path("Export patient to Voxelplan", "Voxelplan (*.hed)")

        if not full_path:
            # file browsing was cancelled or failed, so no destination was selected for the files
            # returning False to signify a failed export
            return False

        path_base, _extension = os.path.splitext(full_path)
        path, basename = os.path.split(path_base)

        progress_dialog = LoadingFileController(load_function=self._export_patient_voxelplan,
                                                function_args=(path, basename, patient_item),
                                                parent=self.parent_gui.ui, window_title="Export to Voxelplan",
                                                progress_message="Saving files, please wait...",
                                                finish_message="Export complete.")
        progress_dialog.start()
        return True

    @staticmethod
    def _export_patient_voxelplan(path, basename, patient_item):
        logger.info("Voxelplan export to: " + path + " with plan basename: " + basename)

        patient_item.data.ctx.write(os.path.join(path, basename + patient_item.data.ctx.data_file_extension))
        if patient_item.data.vdx:
            patient_item.data.vdx.write(os.path.join(path, basename + patient_item.data.vdx.data_file_extension))
        else:
            logger.warning("Exported patient has no VOI.")

        logger.debug("Voxelplan export finished.")

    def export_patient_dicom_callback(self, patient_item: PatientItem) -> bool:
        """
        Open a folder selection window, then export patient cube to DICOM format in the selected folder.

        Parameters:
        patient_item (PatientItem): Patient tree item containing the patient's data

        Returns:
        bool: Whether export was successful
        """
        logger.debug("DICOM export start.")
        full_path = self.parent_gui.browse_folder_path("Export patient to DICOM")

        if not full_path:
            # file browsing was cancelled or failed, so no destination was selected for the files
            # returning False to signify a failed export
            return False

        progress_dialog = LoadingFileController(load_function=self._export_patient_dicom,
                                                function_args=(full_path, patient_item),
                                                parent=self.parent_gui.ui, window_title="Export to DICOM",
                                                progress_message="Saving files, please wait...",
                                                finish_message="Export complete.")
        progress_dialog.start()
        return True

    @staticmethod
    def _export_patient_dicom(full_path, patient_item):

        logger.info("DICOM export to: " + full_path)

        patient_item.data.ctx.write_dicom(full_path)
        if patient_item.data.vdx:
            patient_item.data.vdx.write_dicom(full_path)
        else:
            logger.warning("Exported patient has no VOI.")

        logger.debug("DICOM export finished.")

    def export_dose_voxelplan_callback(self, simulation_result: SimulationResultItem):
        """
        Open a file name selection window, then export dose cube to Voxelplan format with the selected name.

        Parameters:
        simulation_result (SimulationResultItem): Tree item containing the dose cube's data

        Returns:
        bool: Whether export was successful
        """
        logger.debug("Export DoseCube to Voxelplan")
        dose_cube = simulation_result.data
        full_path = self.parent_gui.save_file_path("Export Dose to Voxelplan", "Voxelplan (*.hed)")

        if not full_path:
            # file browsing was cancelled or failed, so no destination was selected for the files
            # returning False to signify a failed export
            return False

        path_base, extension = os.path.splitext(full_path)
        path, basename = os.path.split(path_base)
        logger.info("Voxelplan export to: " + path + " with basename: " + basename)

        progress_dialog = LoadingFileController(load_function=dose_cube.write,
                                                function_args=(path_base,),
                                                parent=self.parent_gui.ui, window_title="Export to Voxelplan",
                                                progress_message="Saving files, please wait...",
                                                finish_message="Export complete.")
        progress_dialog.start()

        logger.debug("Voxelplan export finished.")
        return True

    def export_dose_dicom_callback(self, simulation_result: SimulationResultItem):
        """
        Open a folder selection window, then export dose cube to DICOM format in the selected folder.

        Parameters:
        simulation_result (SimulationResultItem): Tree item containing the dose cube's data

        Returns:
        bool: Whether export was successful
        """
        logger.debug("Export DoseCube to DICOM")
        dose_cube = simulation_result.data

        full_path = self.parent_gui.browse_folder_path("Export Dose to DICOM")

        if not full_path:
            # file browsing was cancelled or failed, so no destination was selected for the files
            # returning False to signify a failed export
            return False

        logger.info("DICOM export to: " + full_path)

        progress_dialog = LoadingFileController(load_function=dose_cube.write_dicom,
                                                function_args=(full_path,),
                                                parent=self.parent_gui.ui, window_title="Export to DICOM",
                                                progress_message="Saving files, please wait...",
                                                finish_message="Export complete.")
        progress_dialog.start()

        logger.debug("DICOM export finished.")
        return True

    def import_dose_voxelplan_callback(self) -> bool:
        logger.debug("Import DoseCube from Voxelplan")

        selected_patient: PatientItem = self.app_model.patient_tree.selected_item_patient()
        if not selected_patient:
            # no patient related to the current selection
            self.parent_gui.show_info(*InfoMessages["addNewPatient"])
            return False

        full_path = self.parent_gui.browse_file_path("Import Dose from Voxelplan", "Voxelplan dose (*.dos)")

        if not full_path:
            # file browsing was cancelled or failed, so no file path was selected
            # returning False to signify a failed import
            return False

        logger.info("Voxelplan import from: " + full_path)

        progress_dialog = LoadingFileController(load_function=self._import_dose_voxelplan,
                                                function_args=(full_path, selected_patient),
                                                parent=self.parent_gui.ui, window_title="Import from Voxelplan",
                                                progress_message="Loading files, please wait...",
                                                finish_message="Import complete.")
        progress_dialog.start()

        logger.debug("Voxelplan import finished.")
        return True

    def _import_dose_voxelplan(self, full_path, selected_patient):
        path_base, _extension = os.path.splitext(full_path)
        dir_path, plan_basename = os.path.split(path_base)

        result_item: SimulationResultItem = SimulationResultItem()
        plan = self._setup_imported_plan(plan_basename, dir_path)

        # we're not using the default import method from SimulationResults,
        # so that we're not limited to .phys.dos or .bio.dos,
        # but rather the user's file of choice
        result_item.data = SimulationResults(patient=selected_patient.data, plan=plan.data, name=plan.data.basename)
        result_item.data.import_dos(full_path)

        # add dose item as child of Simulation
        dose_item: SimulationResultItem = SimulationResultItem()
        dose_item.data = result_item.data.get_doses()[-1]
        result_item.add_child(dose_item)

        # parent_item=selected_patient to set simulation result as a child of the patient
        # parent_item=None to set simulation result as a independent item
        self.app_model.patient_tree.add_new_item(parent_item=selected_patient, item=result_item)

    def import_dose_dicom_callback(self) -> bool:
        logger.debug("Import DoseCube from DICOM")

        selected_patient: PatientItem = self.app_model.patient_tree.selected_item_patient()
        if not selected_patient:
            # no patient related to the current selection
            self.parent_gui.show_info(*InfoMessages["addNewPatient"])
            return False

        dicom_dir = self.parent_gui.browse_folder_path("Import Dose from DICOM")

        if not dicom_dir:
            # file browsing was cancelled or failed, so no directory path was selected
            # returning False to signify a failed import
            return False

        logger.info("DICOM import from: " + dicom_dir)

        progress_dialog = LoadingFileController(load_function=self._import_dose_dicom,
                                                function_args=(dicom_dir, selected_patient),
                                                parent=self.parent_gui.ui, window_title="Import from DICOM",
                                                progress_message="Loading files, please wait...",
                                                finish_message="Import complete.")
        progress_dialog.start()

        logger.debug("DICOM import finished.")
        return True

    def _import_dose_dicom(self, dicom_dir, selected_patient):
        _dir_path, plan_basename = os.path.split(dicom_dir)

        result_item = SimulationResultItem()
        plan = self._setup_imported_plan(plan_basename, dicom_dir)

        # we're not using the default import method from SimulationResults,
        # because it relies on data in the Voxelplan format (*.dos)
        result_item.data = SimulationResults(patient=selected_patient.data, plan=plan.data, name=plan.data.basename)

        dos = DosCube(selected_patient.data.ctx)
        dcm = dicomhelper.read_dicom_dir(dicom_dir)
        dos.read_dicom(dcm)
        result_item.data.plan.dosecubes.append(dos)

        # add dose item as child of Simulation
        dose_item = SimulationResultItem()
        dose_item.data = dos
        result_item.add_child(dose_item)

        # parent_item=selected_patient to set simulation result as a child of the patient
        self.app_model.patient_tree.add_new_item(parent_item=selected_patient, item=result_item)

    def export_plan_exec_callback(self, item: Union[PlanItem, FieldItem]) -> bool:
        """
        Open a file name selection window, then export the plan to an .exec file with the selected name.

        Parameters:
        item (Union[PlanItem, FieldItem]): Tree item containing the plan's data or one of its fields

        Returns:
        bool: Whether export was successful
        """
        logger.debug("Export plan .exec file.")
        if isinstance(item, PlanItem):
            plan_item = item
        else:
            # field's parent is a plan
            plan_item = item.parent

        plan: pytrip.tripexecuter.Plan = plan_item.data

        full_path = self.parent_gui.save_file_path("Export plan", "Plan file (*.exec)")

        if not full_path:
            # file browsing was cancelled or failed, so no destination was selected for the files
            # returning False to signify a failed export
            return False

        logger.info("Plan export to: " + full_path)

        progress_dialog = LoadingFileController(load_function=plan.save_exec,
                                                function_args=(full_path,),
                                                parent=self.parent_gui.ui, window_title="Exporting plan",
                                                progress_message="Saving files, please wait...",
                                                finish_message="Export complete.")
        progress_dialog.start()
        logger.debug("Plan export finished.")
        return True

    @staticmethod
    def _setup_imported_plan(basename: str, working_dir: str):
        plan = PlanItem()

        # turn off the import flags to create a SimulationResults object
        # without importing data with a default configuration:
        plan.data.want_phys_dose = False
        plan.data.want_bio_dose = False
        plan.data.want_dlet = False
        plan.data.want_rst = False
        plan.data.want_tlet = False

        plan.basename = basename
        plan.data.basename = basename
        plan.data.basename = basename
        plan.data.working_dir = working_dir

        return plan

    def one_click_callback(self):
        """
        Handles a click action on any TreeItem with its specific behavior.
        This includes displaying the correct data in the canvas and enabling the correct UI buttons.

        Returns:
        None
        """

        self.parent_gui.action_add_vois_set_enable(False)
        self.parent_gui.action_create_field_set_enable(False)
        self.parent_gui.action_create_plan_set_enable(False)
        self.parent_gui.action_execute_plan_set_enable(False)
        self.parent_gui.import_dose_cube_set_enabled(False)

        item = self.app_model.patient_tree.selected_item()
        patient_item = self.app_model.patient_tree.selected_item_patient()
        logger.debug("Item clicked: " + str(item))
        logger.debug("Parent of item clicked: " + str(item.parent))

        if isinstance(item, SimulationResultItem):
            # SimulationResultItem is a class shared by TreeItems containing Simulations and those containing Cubes
            # we need to find out which was clicked, so we inspect their data field
            if isinstance(item.data, SimulationResults):
                # selected item is the top item of simulation results
                parent_item = item
                item = item.children[0]
            else:
                # selected item is a simulation result item (e.g. DoseCube)
                parent_item = item.parent

            if parent_item.state is None:
                parent_item.state = self.app_model.viewcanvases.get_gui_state()

            self.app_model.viewcanvases.set_simulation_results(simulation_results=parent_item.data,
                                                               simulation_item=item.data, state=parent_item.state)

            self.chart.set_simulation_result(simulation_result=parent_item.data)
        elif isinstance(item, PatientItem):
            self.parent_gui.action_add_vois_set_enable(True)
            self.parent_gui.action_create_plan_set_enable(True)
            self._show_patient(patient_item, patient_item)
            self.parent_gui.import_dose_cube_set_enabled(True)
        elif isinstance(item, PlanItem):
            self.parent_gui.action_create_plan_set_enable(True)
            self.parent_gui.action_create_field_set_enable(True)
            self._show_patient(patient_item, item)
            self.parent_gui.import_dose_cube_set_enabled(True)
        elif isinstance(item, FieldItem):
            self.parent_gui.action_create_plan_set_enable(True)
            self.parent_gui.action_create_field_set_enable(True)
            self._show_patient(patient_item, item)
            self.parent_gui.import_dose_cube_set_enabled(True)

        if item.is_executable():
            self.parent_gui.action_execute_plan_set_enable(True)

    def _show_patient(self, data_item: PatientItem, state_item: PatientGuiState) -> None:
        """
        Displays the data of a patient in the canvas according to the GUI state provided.

        Parameters:
        data_item (PatientItem): The patient tree item to display.
        state_item (PatientGuiState): The GUI state data of the selected patient.

        Returns:
        None.
        """
        if not self.app_model.viewcanvases:
            self.app_model.viewcanvases = ViewCanvases(self.parent_gui)
            self.parent_gui.add_widget(self.app_model.viewcanvases.widget())

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
        None
        """
        self.app_model.patient_tree.set_visible(self.parent_gui.action_open_tree_checked)
