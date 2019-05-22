import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from pytripgui.view.gen.field import Ui_FieldDialog

logger = logging.getLogger(__name__)


class FieldControl(object):
    """
    This class is used to gather info from user about fields and pass it to pytrip
    """

    @staticmethod
    def new_field(plan):
        """
        Creates new field and add it to tree
        """
        logger.debug("new_field()")

        # setup a new tripexecuter.field object
        import pytrip.tripexecuter as pte
        field = pte.Field(basename=plan.basename)

        # open a dialog for the user to edit it
        FieldControl.edit_field(field)
        # attach this field to the list of plans in models.
        plan.fields.append(field)

    @staticmethod
    def edit_field(field):
        """
        This method should show window, where user can modify field attributes.
        """
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_FieldDialog()

        dialog_ui.setupUi(dialog)
        FieldControl._populate_plan_ui(dialog_ui, field)
        FieldControl._setup_callbacks(dialog_ui, field)

        dialog.exec_()
        dialog.show()

    @staticmethod
    def _populate_plan_ui(ui, field):
        """
        TODO: this comment
        """
        if field.use_raster_file:
            ui.checkBox.setCheckState(Qt.Checked)
        else:
            ui.checkBox.setCheckState(Qt.Unchecked)
        # TODO: populate rest of the field

    @staticmethod
    def _setup_callbacks(ui, field):
        """
        TODO: this comment
        """
        ui.checkBox.stateChanged.connect(lambda: FieldControl._callbacks(ui, field, "use_raster_file"))

    @staticmethod
    def _callbacks(ui, field, attr_name):
        """
        TODO: this comment
        """
        if "use_raster_file" == attr_name:
            field.use_raster_file = ui.checkBox.checkState()
