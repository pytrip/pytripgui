import logging
from typing import Collection

from PyQt5.QtWidgets import QApplication
from pytrip import Voi

from pytripgui.contouring_vc.contouring_view import ContouringView

logger = logging.getLogger(__name__)


class ContouringController:
    def __init__(self, vois: Collection[Voi], parent=None):
        self._view = ContouringView(parent=parent)
        self._vois = vois
        self._view.connect_yes(lambda: self._contour_vois())

    def _contour_vois(self):
        self._view.update_accepted()
        QApplication.processEvents()
        total_vois = len(self._vois)
        for current, voi in enumerate(self._vois):
            self._view.update_progress(voi.name, current, total_vois)
            QApplication.processEvents()
            voi.calculate_slices_with_contours_in_sagittal_and_coronal()
        self._view.update_finished()

    def show(self):
        self._view.show()

    def _finish_(self):
        self._view.update_finished()
