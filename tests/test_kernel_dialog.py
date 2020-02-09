import logging
from pytestqt.qt_compat import qt_api

from pytripgui.kernel_vc import KernelController
from pytripgui.kernel_vc import KernelQtView
from pytrip.tripexecuter import KernelModel
from pytrip.tripexecuter import Projectile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

kernels = []
# Kernel 1
ker = KernelModel()
ker.projectile = Projectile("C")
kernels.append(ker)
# Kernel 2
ker = KernelModel()
ker.projectile = Projectile("H")
kernels.append(ker)


def test_basics(qtbot):
    assert qt_api.QApplication.instance() is not None

    view = KernelQtView()
    controller = KernelController(kernels, view)
    controller.set_view_from_model()

    qtbot.addWidget(view)
    view.ui.show()
    assert view.ui.isVisible()

    # selecting kernel to edit
    current_kernel_index = 1
    view.ui.beamKernel_comboBox.setCurrentIndex(current_kernel_index)
    assert view.projectile_symbol == kernels[current_kernel_index].projectile.iupac

    # setting new name
    new_kernel_name = "Proton"
    view.kernel_name = new_kernel_name

    # clicking "OK"
    view.ui.accept_buttonBox.accepted.emit()
    assert not view.ui.isVisible()
    assert controller.user_clicked_save

    # checking if new name was saved
    assert kernels[current_kernel_index].name == new_kernel_name
