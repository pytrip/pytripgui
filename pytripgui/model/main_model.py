import logging

from pytripgui.model.plot_model import PlotModel
# from pytripgui.model.tree_model import TreeModel

logger = logging.getLogger(__name__)


class MainModel(object):
    def __init__(self, app):
        self._update_funce = []

        self.ctx = None  # Only one CTX is allowed
        self.vdx = None  # Only one VDX is allowed
        self.plans = []
        self.dos = []   # TODO: change to self.doss (plural s)
        self.let = []   # TODO: change to self.lets (plural s)

        # paths
        self.dicom_path = "."
        self.voxelplan_path = "."
        self.tripexec_path = "."
        self.wdir = "."

        # attach submodels
        self.plot = PlotModel()
        # self.tree = TreeModel()
        self.kernels = []  # placeholder for KernelModels

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
    This class contains links to the model parameters which need to be retained when closing PyTRiPGUI
    """

    def __init__(self, model):
        """
        Establishes links to the model.
        """
        self.dicom_path = model.dicom_path
        self.voxelplan_path = model.voxelplan_path
        self.tripexec_path = model.tripexec_path
        self.wdir = model.wdir

        self.kernels = model.kernels

        from pytrip import __version__ as _pytrip_version
        from pytripgui import __version__ as _pytripgui_version

        self._pytrip_version = _pytrip_version
        self._pytripgui_version = _pytripgui_version
