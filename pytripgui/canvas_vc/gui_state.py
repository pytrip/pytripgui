from typing import Optional, List

from pytripgui.canvas_vc.projection_selector import ProjectionSelector


class PatientGuiState:
    """
    This class holds information about viewing patient
        - on which slice user stopped scrolling on each plane
        - which VOIs user picked to be shown
        etc.
    """
    def __init__(self):
        self.projection_selector: Optional[ProjectionSelector] = None
        self.ticked_voi_list: List = []
