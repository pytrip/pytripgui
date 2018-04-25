import logging

from PyQt5 import QtWidgets

from pytripgui.view.gen.plan import Ui_PlanDialog

logger = logging.getLogger(__name__)


class PlanController(object):
    """
    """

    def __init__(self, model):
        """
        """
        self.model = model

    @staticmethod
    def new_plan(model):
        """
        Creates a new instance of a plan, and adds it to model.
        """
        logger.debug("new_plan()")

        # setup a new tripexecuter.plan object
        import pytrip.tripexecuter as pte
        plan = pte.Plan(basename=model.ctx.basename)

        # attach this plan to the list of plans in models.
        model.plans.append(plan)

        # open a dialog for the user to edit it
        PlanController.edit_plan(model, plan)

        return plan  # for further use

    @staticmethod
    def edit_plan(model, plan):
        """
        """
        # open the plan configuration dialog
        # https://stackoverflow.com/questions/42505429/pyqt5-gui-structure-advice-needed
        popup = QtWidgets.QDialog()
        popupui = Ui_PlanDialog()
        popupui.setupUi(popup)
        PlanController._populate_plan_ui(popupui, model, plan)
        PlanController._callbacks_plan_ui(popupui, model, plan)
        logger.debug("edit_plan() Popup show")  # Something is broken here, does not show?
        popup.show()

    @staticmethod
    def delete_plan(model, plan):
        """
        """
        logger.debug("delete_plan()")
        pass

    @staticmethod
    def _populate_plan_ui(ui, model, plan):
        """
        Fill all widgets with current model data.
        """

        voinames = [voi.name for voi in model.vdx.vois]

        # TARGET
        ui.comboBox.clear()
        ui.comboBox.addItems(voinames)

        # OAR
        list = ui.listView
        from PyQt5.QtGui import QStandardItemModel
        from PyQt5.QtGui import QStandardItem
        # https://www.pythoncentral.io/pyside-pyqt-tutorial-qlistview-and-qstandarditemmodel/
        listmodel = QStandardItemModel(list)
        for voiname in voinames:
            item = QStandardItem(voiname)
            item.setCheckable(True)
            listmodel.appendRow(item)
        list.setModel(listmodel)

        # INCUBE
        # TISSUE
        # RESIDUAL TISSUE

    @staticmethod
    def _callbacks_plan_ui(ui, model, plan):
        """
        Connect all widgets to model.
        No OK button needs to be pressed, when a value is changed, model is updated immediately.
        """
        pass
