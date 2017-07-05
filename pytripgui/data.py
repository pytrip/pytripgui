"""
    This file is part of pytripgui.

    pytripgui is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pytripgui is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pytripgui.  If not, see <http://www.gnu.org/licenses/>
"""
"""
All plan data are stored here.
"""

class TRiPData:
    """
    TODO: find better name for this class (PyTripGuiData ?)

    Structure:

    Each Patient will have its own TRiPData object
    Each Data object holds
    - a list of plans
    - a list of VOIs for this particular patient


    Plans will be extended to hold VOIs as well.
    So each plan will also hold:
    - a list of VOIs (from a given VdxCube)
    - a list of DosCubes (don't call them "dose", this is ambigous)
    - a list of LETCubes

    """

    def __init__(self):
        """
        """
        self.patient_name = ""
        self.plans = []
        self.active_plan = None
        self.vois = []
        
        for voi in self.vois:
            voi.selected = True  # attribute whether it is visible in plot or not
