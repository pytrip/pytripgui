import logging

import pytest

from pytripgui.kernel_vc import KernelController
from pytripgui.kernel_vc import KernelQtView
from pytrip.tripexecuter import KernelModel
from pytrip.tripexecuter import Projectile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestKernelDialog:
    kernels = []
    # Kernel 1
    ker = KernelModel()
    ker.projectile = Projectile("C")
    kernels.append(ker)
    # Kernel 2
    ker = KernelModel()
    ker.projectile = Projectile("H")
    kernels.append(ker)

    @staticmethod
    @pytest.mark.skip(reason="needs to be fixed, non-Widget passed to addWidget method")
    def test_basics(qtbot):

        view = KernelQtView()
        controller = KernelController(TestKernelDialog.kernels, view)
        controller.set_view_from_model()

        qtbot.addWidget(view)
        view.ui.show()
        assert view.ui.isVisible()

        # selecting kernel to edit
        current_kernel_index = 1
        view.ui.beamKernel_comboBox.setCurrentIndex(current_kernel_index)
        assert view.projectile_symbol == TestKernelDialog.kernels[current_kernel_index].projectile.iupac

        # setting new name
        new_kernel_name = "Proton"
        view.kernel_name = new_kernel_name

        # clicking "OK"
        view.ui.accept_buttonBox.accepted.emit()
        assert not view.ui.isVisible()
        assert controller.user_clicked_save

        # checking if new name was saved
        assert TestKernelDialog.kernels[current_kernel_index].name == new_kernel_name
