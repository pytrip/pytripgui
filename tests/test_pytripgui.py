import logging
import os.path

import pytest
from PyQt5 import QtCore, QtWidgets
import pyautogui

from pytrip.ctx import CtxCube
from pytrip.vdx import create_sphere, VdxCube

from pytripgui.app_logic.viewcanvas import ViewCanvases
from pytripgui.main_window_qt_vc import MainWindowQtView, MainWindowController
from pytripgui.model.main_model import MainModel
from pytripgui.view.qt_gui import UiPlanDialog, UiFieldDialog

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def window():
    model = MainModel()
    view = MainWindowQtView()
    controller = MainWindowController(model, view)
    yield model, view, controller


@pytest.fixture(scope="session")
def voxelplan_header_path(tmpdir_factory):
    ctx = CtxCube()
    ctx.create_empty_cube(value=0, dimx=100, dimy=100, dimz=25, pixel_size=1, slice_distance=2, slice_offset=0)
    file_obj = tmpdir_factory.mktemp("data").join("patient")
    patient_base_path = str(file_obj)
    ctx.write(patient_base_path)
    vdx = VdxCube(cube=ctx)
    voi = create_sphere(cube=ctx, name="target", center=[50, 50, 25], radius=10)
    vdx.add_voi(voi)
    vdx.write(patient_base_path + '.vdx')
    yield patient_base_path + '.hed'


def test_basics(qtbot, window):
    _, view, _ = window
    qtbot.addWidget(view.ui)
    view.ui.show()

    assert view.ui.isVisible()
    assert view.ui.windowTitle() == 'PyTRiPGUI'


@pytest.mark.xfail(sys.version_info < (3,7), reason="issue on matplotlib with python 3.6 or older")
def test_open_voxelplan(qtbot, window, voxelplan_header_path):
    model, view, _ = window
    qtbot.addWidget(view.ui)

    patient_dir, header_basename = os.path.split(voxelplan_header_path)

    def handle_file_dialog():
        dialog = view.ui.findChild(QtWidgets.QFileDialog)
        dialog.setDirectory(QtCore.QDir(patient_dir))

        pyautogui.typewrite(header_basename)
        pyautogui.press("enter")

        #  solution when option QFileDialog.DontUseNativeDialog is on
        #  it doesn't require pyautogui
        # dialog.findChild(QtWidgets.QLineEdit, 'fileNameEdit').setText(file)
        # open_button = dialog.findChildren(QtWidgets.QPushButton)[0]
        # qtbot.mouseClick(open_button, QtCore.Qt.LeftButton)

    QtCore.QTimer.singleShot(1000, handle_file_dialog)
    view.ui.actionOpen_Voxelplan.trigger()

    assert isinstance(model.viewcanvases, ViewCanvases)
    assert model.patient_tree.patient_tree_model.rowCount() == 1
    assert len(model.patient_tree.selected_item_patient().data.vdx.vois) == 1


@pytest.mark.xfail(sys.version_info < (3,7), reason="issue on matplotlib with python 3.6 or older")
def test_create_plan_and_field(qtbot, window, voxelplan_header_path):
    _, view, controller = window
    qtbot.addWidget(view.ui)

    controller.open_voxelplan(voxelplan_header_path)

    def handle_plan_dialog():
        dialog = view.ui.findChild(UiPlanDialog)
        assert dialog.isVisible()
        dialog.findChild(QtWidgets.QTabWidget, 'tabWidget').setCurrentIndex(1)
        radios = dialog.targetROI_listWidget.findChildren(QtWidgets.QRadioButton)
        radios[0].setChecked(True)
        ok_button = dialog.accept_buttonBox.findChildren(QtWidgets.QPushButton)[0]
        qtbot.mouseClick(ok_button, QtCore.Qt.LeftButton)

    assert view.ui.actionNew_Plan.isEnabled() is True
    assert view.ui.actionCreate_field.isEnabled() is False
    QtCore.QTimer.singleShot(1000, handle_plan_dialog)
    view.ui.actionNew_Plan.trigger()

    def handle_field_dialog():
        dialog = view.ui.findChild(UiFieldDialog)
        assert dialog.isVisible()
        qtbot.mouseClick(dialog.gantry_pushButton_p90, QtCore.Qt.LeftButton)
        assert dialog.gantry_doubleSpinBox.value() == 90.0
        ok_button = dialog.accept_ButtonBox.findChildren(QtWidgets.QPushButton)[0]
        qtbot.mouseClick(ok_button, QtCore.Qt.LeftButton)

    assert view.ui.actionCreate_field.isEnabled() is True
    QtCore.QTimer.singleShot(1000, handle_field_dialog)
    view.ui.actionCreate_field.trigger()
