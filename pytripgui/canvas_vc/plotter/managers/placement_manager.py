from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec, SubplotSpec
"""
This class was made to remove extra responsibilities from mpl_plotter.
It gathers information about elements that are added to the figure and determines where they should be put
 based on some boolean mask.
Thanks to it, it is possible to display elements of figure differently based on what elements are to be displayed.

If you want to add new element, follow these few steps:
    1. Add flag that represents presence or absence of your new element
    2. Add new entry to _positions dictionary for your element
    3. Add getter for that new entry
    4. Add methods that set that flag to true and false
    5. Add method that holds condition with your element's flag
    6. Add method that changes entries in _positions dictionary in the way that your elements fits in figure
"""


class PlacementManager:
    """
    Class that holds information what is present on figure and positions of those elements.
    Updates positions every time something is added to figure to ensure that everything has space to be shown properly.
    """
    def __init__(self, figure: Figure):
        """
        Parameters:
        ----------
        figure: Figure -- figure on which grid to position elements will be made
        """
        self.columns: int = 16
        self.rows: int = 9
        self._grid_spec: GridSpec = GridSpec(ncols=self.columns, nrows=self.rows, figure=figure)

        self._ctx_bar: bool = False
        self._dose_bar: bool = False
        self._let_bar: bool = False

        self._positions: dict = {
            'coord_info': self._grid_spec[:2, 13:],
            'plotter': self._grid_spec[:, 2:14],
            'ctx_bar': None,
            'dose_bar': None,
            'let_bar': None
        }

    """
    Block of methods that set each flag to false or true
    """

    def add_ctx_bar(self) -> None:
        self._ctx_bar = True
        self._update_places()

    def remove_ctx_bar(self) -> None:
        self._ctx_bar = False
        self._update_places()

    def add_dose_bar(self) -> None:
        self._dose_bar = True
        self._update_places()

    def remove_dose_bar(self) -> None:
        self._dose_bar = False
        self._update_places()

    def add_let_bar(self) -> None:
        self._let_bar = True
        self._update_places()

    def remove_let_bar(self) -> None:
        self._let_bar = False
        self._update_places()

    """
    Block of methods that hold conditions and methods that change _positions based on those conditions
    """

    def _only_ctx(self) -> bool:
        return self._ctx_bar and not self._dose_bar and not self._let_bar

    def _only_ctx_places(self) -> None:
        self._positions['ctx_bar'] = self._grid_spec[:, 1]
        self._positions['dose_bar'] = None
        self._positions['let_bar'] = None

    def _ctx_and_dose(self) -> bool:
        return self._ctx_bar and self._dose_bar and not self._let_bar

    def _ctx_and_dose_places(self) -> None:
        self._positions['ctx_bar'] = self._grid_spec[:, 1]
        self._positions['dose_bar'] = self._grid_spec[:, 0]
        self._positions['let_bar'] = None

    def _ctx_and_let(self) -> bool:
        return self._ctx_bar and not self._dose_bar and self._let_bar

    def _ctx_and_let_places(self) -> None:
        self._positions['ctx_bar'] = self._grid_spec[:, 1]
        self._positions['dose_bar'] = None
        self._positions['let_bar'] = self._grid_spec[:, 0]

    """
    Method that checks which condition is satisfied and updates positions
    """

    def _update_places(self) -> None:
        if self._only_ctx():
            self._only_ctx_places()
        elif self._ctx_and_dose():
            self._ctx_and_dose_places()
        elif self._ctx_and_let():
            self._ctx_and_let_places()

    """
    Block of getter for each element
    """

    def get_coord_info_place(self) -> SubplotSpec:
        return self._positions['coord_info']

    def get_main_plot_place(self) -> SubplotSpec:
        return self._positions['plotter']

    def get_ctx_bar_place(self) -> SubplotSpec:
        return self._positions['ctx_bar']

    def get_dose_bar_place(self) -> SubplotSpec:
        return self._positions['dose_bar']

    def get_let_bar_place(self) -> SubplotSpec:
        return self._positions['let_bar']
