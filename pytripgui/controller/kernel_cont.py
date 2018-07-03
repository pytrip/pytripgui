import logging

from PyQt5 import QtWidgets
# from PyQt5.QtCore import Qt

# from pytrip.tripexecuter import KernelModel

from pytripgui.view.gen.kernel import Ui_KernelDialog

logger = logging.getLogger(__name__)


class KernelController(object):
    """
    """

    def __init__(self, model):
        """
        """
        self.model = model

    @staticmethod
    def edit_kernel(model):
        """
        Show an instance of a kernel.
        """
        logger.debug("edit_kernel()")

        # open the plan configuration dialog
        # https://stackoverflow.com/questions/42505429/pyqt5-gui-structure-advice-needed
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_KernelDialog()
        # plan_ui = dialog_ui # TODO why not being used ?

        dialog_ui.setupUi(dialog)
        # KernelController._populate_kernel_ui(dialog_ui, model, plan)
        # KernelController._setup_kernel_callbacks(dialog_ui, model, plan)
        dialog.exec_()
        dialog.show()

    @staticmethod
    def delete_kernel(model):
        """
        Deletes a kernel from the model.
        """
        logger.debug("edit_kernel()")

    @staticmethod
    def _populate_kernel_ui(ui, model, kernel):
        """
        Fill all widgets with current model data.
        """
        logger.debug("_populate_kernel_ui()")
