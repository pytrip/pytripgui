from matplotlib.gridspec import GridSpec, SubplotSpec


class PlacementManager:
    columns: int = 16
    rows: int = 9

    def __init__(self, figure):
        self._grid_spec: GridSpec = GridSpec(ncols=self.columns, nrows=self.rows, figure=figure)

        self._ctx_bar: bool = False
        self._dose_bar: bool = False
        self._let_bar: bool = False

        self._positions: dict = {
            'coord_info': self._grid_spec[:2, 13:],
            'main_plot': self._grid_spec[:, 2:14],
            'ctx_bar': None,
            'dose_bar': None,
            'let_bar': None
        }

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

    def _only_ctx(self) -> bool:
        return self._ctx_bar \
               and not self._dose_bar \
               and not self._let_bar

    def _only_ctx_places(self) -> None:
        self._positions['ctx_bar'] = self._grid_spec[:, 1]
        self._positions['dose_bar'] = None
        self._positions['let_bar'] = None

    def _ctx_and_dose(self) -> bool:
        return self._ctx_bar \
               and self._dose_bar \
               and not self._let_bar

    def _ctx_and_dose_places(self) -> None:
        self._positions['ctx_bar'] = self._grid_spec[:, 1]
        self._positions['dose_bar'] = self._grid_spec[:, 0]
        self._positions['let_bar'] = None

    def _ctx_and_let(self) -> bool:
        return self._ctx_bar \
               and not self._dose_bar \
               and self._let_bar

    def _ctx_and_let_places(self) -> None:
        self._positions['ctx_bar'] = self._grid_spec[:, 1]
        self._positions['dose_bar'] = None
        self._positions['let_bar'] = self._grid_spec[:, 0]

    def _update_places(self) -> None:
        if self._only_ctx():
            self._only_ctx_places()
        elif self._ctx_and_dose():
            self._ctx_and_dose_places()
        elif self._ctx_and_let():
            self._ctx_and_let_places()

    def get_coord_info_place(self) -> SubplotSpec:
        return self._positions['coord_info']

    def get_main_plot_place(self) -> SubplotSpec:
        return self._positions['main_plot']

    def get_ctx_bar_place(self) -> SubplotSpec:
        return self._positions['ctx_bar']

    def get_dose_bar_place(self) -> SubplotSpec:
        return self._positions['dose_bar']

    def get_let_bar_place(self) -> SubplotSpec:
        return self._positions['let_bar']
