import sys
import logging
from PyQt5.QtWidgets import QApplication

from pytripgui.view.qt_gui import UiMainWindow
from pytripgui.treewidget_vc.treewidget_view import TreeWidgetView
from pytripgui.treewidget_vc.treewidget_cont import TreeWidgetController
from pytripgui.plan_executor.patient_model import PatientModel
from pytripgui.treewidget_vc.patient_tree_model import PatientTreeModel
from pytrip.tripexecuter.plan import Plan

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


app = QApplication(sys.argv)
widget = UiMainWindow()
widget.show()


patient_list = list()
patient_list.append(PatientModel())
patient_list.append(PatientModel())
patient_list.append(PatientModel())
patient_list[0].name = "Patient nr 0"
patient_list[0].plans.append(Plan(basename="Hello"))

patient_list[1].name = "Another one"
patient_list[2].name = "Third Patient"

treeView = TreeWidgetView(widget.patient_treeView)
model = PatientTreeModel(patient_list)
widget.patient_treeView.setModel(model)

treeControler = TreeWidgetController(patient_list, treeView)

app.exec_()
