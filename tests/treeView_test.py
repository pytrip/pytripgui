import sys
import logging
from anytree import RenderTree
from PyQt5.QtWidgets import QApplication, QDockWidget
from PyQt5.QtCore import Qt

from pytripgui.view.qt_gui import UiMainWindow
from pytripgui.tree_vc.TreeView import TreeView
from pytripgui.tree_vc.TreeController import TreeController
from pytripgui.tree_vc.TreeModel import PatientTreeModel
from pytripgui.tree_vc.TreeItems import PatientList
from pytripgui.tree_vc.TreeItems import PatientItem
from pytripgui.tree_vc.TreeItems import PlanItem
from pytripgui.tree_vc.TreeItems import FieldItem
from pytripgui.tree_vc.TreeItems import KernelItem

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


app = QApplication(sys.argv)


mainWindow = UiMainWindow()

kernel1 = KernelItem()
kernel1.data.basename = "C Kernel"

kernel2 = KernelItem()
kernel2.data.basename = "H Kernel"

field1 = FieldItem()
field1.data.basename = "Field1"
field1.add_cloned_child(kernel1)

field2 = FieldItem()
field2.data.basename = "Field2"
field2.add_cloned_child(kernel2)

plan1 = PlanItem()
plan1.add_cloned_child(field1)
plan1.add_cloned_child(field2)
plan1.data.basename = "Plan1"

plan2 = PlanItem()
plan2.add_cloned_child(field1)
plan2.data.basename = "Plan2"

plan3 = PlanItem()
plan3.add_cloned_child(field2)
plan3.data.basename = "Plan3"

plan4 = PlanItem()
plan4.add_cloned_child(field1)
plan4.data.basename = "Plan4"

pat1 = PatientItem()
pat1.add_child(plan1)
pat1.add_child(plan2)
pat1.add_child(plan3)
pat1.add_child(plan4)

patient_list = PatientList()
# patient_list.add_child(pat1)

print(RenderTree(patient_list))

treeView = TreeView()

widget = QDockWidget()
widget.setWidget(treeView)
mainWindow.addDockWidget(Qt.LeftDockWidgetArea, widget)

model = PatientTreeModel(patient_list)
treeView.setModel(model)


mainWindow.show()
# widget.show()

treeControler = TreeController(model, treeView)

app.exec_()
