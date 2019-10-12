import logging

from pytripgui.plan_executor.executor import PlanExecutor

logger = logging.getLogger(__name__)


class MainModel(object):
    def __init__(self, app=None):

        from pytrip import __version__ as _pytrip_version
        from pytripgui import __version__ as _pytripgui_version

        self._pytrip_version = _pytrip_version
        self._pytripgui_version = _pytripgui_version

        self._update_funce = []

        self.executor = PlanExecutor()
        self.kernels = []  # placeholder for KernelModels

        self.patients = []
        self.current_patient = None
        self.patient_tree_cont = None

        self.one_plot_model = None
        self.pne_plot_cont = None

        self.settings = SettingsModel(self)

    def subscribe_update_func(self, func):
        """
        Subscribe a view method for updating
        """
        if func not in self._update_funcs:
            self._update_funcs.append(func)

    def unsubscribe_update_func(self, func):
        """
        Unsubscribe a view method for updating
        """
        if func in self._update_funcs:
            self._update_funcs.remove(func)

    def announce_update(self):
        """
        Update registered view methods
        """
        for func in self._update_funcs:
            func()


class SettingsModel(object):
    """
    This class contains a list model parameters which need to be retained when closing PyTRiPGUI.
    The attribute names must be identical to those in Model.
    Model attribute names with leading _ are saved, but not loaded.
    Model attribute names with leading __ are not saved and not loaded.
    """

    def __init__(self, model):
        """
        This object is pickled upon save and unpickled upon load.
        It is connected to Model, in a way that
        - upon SettingsController.load(), SettingsModel attributes starting with "_"  are not written to         Model.
        - upon SettingsController.save(),         Model attributes starting with "__" are not written to SettingsModel.

        This way,
            a) _version is written to disk, but imported into Model when loading
            b) __internal_attribute__ are not passed between Model and SettingsModel
        """
        # self.trip_config = model.trip_config
        self.executor = model.executor

        self.kernels = model.kernels

        self._pytrip_version = model._pytrip_version  # saved, but not loaded
        self._pytripgui_version = model._pytripgui_version  # saved, but not loaded
