import logging
from typing import Collection

from pytrip import Voi

from pytripgui.contouring_vc.contouring_view import ContouringView

logger = logging.getLogger(__name__)


class ContouringController:
    def __init__(self, vois: Collection[Voi], parent=None, window_title=None,
                 progress_message=None, warning_message=None, finish_message=None):
        self._view = ContouringView(parent=parent, window_title=window_title, progress_message=progress_message,
                                    warning_message=warning_message, finish_message=finish_message)
        self.vois = vois
        # TODO other code
        self._view.connect_yes(self.contour_vois)

    def contour_vois(self):
        for voi in self.vois:
            # TODO: call contouring method
            pass
