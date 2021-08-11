# TODO class that tells plotter how to place all necessary elements on the canvas
from matplotlib.gridspec import GridSpec


class PlacementManager:
    columns = 16
    rows = 9

    def __init__(self, figure):
        self.grid_spec = GridSpec(ncols=self.columns, nrows=self.rows, figure=figure)
        self.plot_elements = {
            'coord_info': False,
            'ctx_plot': False,
            'ctx_bar': False,
            'dose_plot': False,
            'dose_bar': False,
            'let_plot': False,
            'let_bar': False
        }

    # setters

    def add_coord_info(self):
        self.plot_elements['coord_info'] = True

    def remove_coord_info(self):
        self.plot_elements['coord_info'] = False

    def add_ctx_plot(self):
        self.plot_elements['ctx_plot'] = True

    def remove_ctx_plot(self):
        self.plot_elements['ctx_plot'] = False

    def add_ctx_bar(self):
        self.plot_elements['ctx_bar'] = True

    def remove_ctx_bar(self):
        self.plot_elements['ctx_bar'] = False

    def add_dose_plot(self):
        self.plot_elements['dose_plot'] = True

    def remove_dose_plot(self):
        self.plot_elements['dose_plot'] = False

    def add_dose_bar(self):
        self.plot_elements['dose_bar'] = True

    def remove_dose_bar(self):
        self.plot_elements['dose_bar'] = False

    def add_let_plot(self):
        self.plot_elements['let_plot'] = True

    def remove_let_plot(self):
        self.plot_elements['let_plot'] = False

    def add_let_bar(self):
        self.plot_elements['let_bar'] = True

    def remove_let_bar(self):
        self.plot_elements['let_bar'] = False

    # TODO methods that return proper positions of elements of the plot based on which of those elements are present
