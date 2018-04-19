import logging

from model.plot_model import PlotModel
from model.tree_model import TreeModel

logger = logging.getLogger(__name__)


class MainModel(object):

    def __init__(self, app):
        self._update_funce = []
        self.foobar = 10
        self.ctx = None
        self.vdx = None
        self.plans = None
        self.dos = []
        self.let = []

        # attach submodels
        self.plot = PlotModel()
        self.tree = TreeModel()

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
