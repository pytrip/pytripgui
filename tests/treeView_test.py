import sys
import logging
from PyQt5.QtWidgets import QApplication, QDockWidget
from PyQt5.QtCore import Qt

from pytripgui.view.qt_gui import UiMainWindow
from pytripgui.tree_vc.TreeView import TreeView
from pytripgui.tree_vc.TreeController import TreeController
from pytripgui.tree_vc.TreeModel import PatientTreeModel
from pytripgui.tree_vc.TreeItems import PatientList
from pytripgui.tree_vc.TreeItems import PatientItem


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


app = QApplication(sys.argv)
widget = QDockWidget()

mainWindow = UiMainWindow()


patient_list = PatientList()
patient_list.add_child(PatientItem())

treeView = TreeView()
widget.setWidget(treeView)
# widget.setSizePolicy(sizePolicy)

model = PatientTreeModel(patient_list)
treeView.setModel(model)

# mainWindow.addDockWidget(Qt.LeftDockWidgetArea, widget)
# mainWindow.show()
widget.show()

treeControler = TreeController(model, treeView)

app.exec_()
