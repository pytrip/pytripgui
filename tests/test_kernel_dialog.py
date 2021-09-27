import logging

import pytest
from pytrip.tripexecuter import KernelModel
from pytrip.tripexecuter import Projectile

from pytripgui.kernel_vc import KernelController
from pytripgui.kernel_vc import KernelQtView

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def kernels():
    kernels = []
    # Kernel 1
    ker = KernelModel()
    ker.projectile = Projectile("C")
    kernels.append(ker)
    # Kernel 2
    ker = KernelModel()
    ker.projectile = Projectile("H")
    kernels.append(ker)
    yield kernels


def test_basics(qtbot, kernels):
    view = KernelQtView()
    controller = KernelController(kernels, view)
    controller.set_view_from_model()

    qtbot.addWidget(view.ui)
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
