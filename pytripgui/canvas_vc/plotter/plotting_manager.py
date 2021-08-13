from pytripgui.canvas_vc.plotter.bars import BarProjection
from pytripgui.canvas_vc.plotter import CoordinateInfo
from pytripgui.canvas_vc.plotter.images import CtxImage, DoseImage, LetImage
from pytripgui.canvas_vc.plotter.placement_manager import PlacementManager


class PlottingManager:
    def __init__(self, figure, blit_manager):
        self.figure = figure
        self.placement_manager = PlacementManager(self.figure)
        self.blit_manager = blit_manager
        # main plot
        self.axes = self._initialize_axes()
        # plot with information about slices position
        self.info_axes = None
        # CTX
        self.ctx = CtxImage(self.axes)
        self.ctx_bar = None
        # DOS
        self.dose = DoseImage(self.axes)
        self.dose_bar = None
        # LET
        self.let = LetImage(self.axes)
        self.let_bar = None

        # painting background color
        self.figure.patch.set_facecolor('red')

    def _initialize_axes(self):
        axes = self.figure.add_subplot(self.placement_manager.get_main_plot_place())
        axes.grid(False)
        axes.set_xticks([])
        axes.set_yticks([])
        return axes

    def remove_dos(self):
        if self.dose.is_present():
            self.blit_manager.remove_artist(self.dose.get())
            self.dose.remove()
        if self.dose_bar:
            self.placement_manager.remove_dose_bar()
            self.dose_bar.remove()
            self.dose_bar = None

    def plot_dos(self, dos):
        if not self.dose.is_present() and dos.max_dose > dos.min_dose:
            self.dose.plot(dos)
            self.blit_manager.add_artist(self.dose.get())
            if not self.dose_bar:
                self.placement_manager.add_dose_bar()
                self._plot_dos_bar(dos)
        else:
            self.dose.update(dos)

    def _plot_dos_bar(self, dos):
        self.dose_bar = self.figure.add_subplot(self.placement_manager.get_dose_bar_place(),
                                                projection=BarProjection.DOS.value)
        self.dose_bar.plot_bar(self.dose.get(), scale=dos.dos_scale)

    def remove_let(self):
        if self.let.is_present():
            self.blit_manager.remove_artist(self.let.get())
            self.let.remove()
        if self.let_bar:
            self.placement_manager.remove_let_bar()
            self.let_bar.clear_bar()
            self.let_bar = None

    def plot_let(self, data):
        if not self.let.is_present():
            self.let.plot(data)
            self.blit_manager.add_artist(self.let.get())
            if not self.let_bar:
                self.placement_manager.add_let_bar()
                self._plot_let_bar()
        else:
            self.let.update(data)

    def _plot_let_bar(self):
        self.let_bar = self.figure.add_subplot(self.placement_manager.get_let_bar_place(),
                                               projection=BarProjection.LET.value)
        self.let_bar.plot_bar(self.let.get())

    def remove_ctx(self):
        if self.ctx.is_present():
            self.blit_manager.remove_artist(self.ctx.get())
            self.ctx.remove()
        if self.ctx_bar:
            self.placement_manager.remove_ctx_bar()
            self.ctx_bar.clear_bar()
            self.ctx_bar = None

    def plot_ctx(self, data):
        self._plot_coordinate_info(data)
        if not self.ctx.is_present():
            self.ctx.plot(data)
            self.blit_manager.add_artist(self.ctx.get())
            if not self.ctx_bar:
                self.placement_manager.add_ctx_bar()
                self._plot_ctx_bar()
        else:
            self.ctx.update(data)

    def _plot_ctx_bar(self):
        self.ctx_bar = self.figure.add_subplot(self.placement_manager.get_ctx_bar_place(),
                                               projection=BarProjection.CTX.value)
        self.ctx_bar.plot_bar(self.ctx.get())

    def _plot_coordinate_info(self, data):
        if self.info_axes is None:
            self.info_axes = self.figure.add_subplot(self.placement_manager.get_coord_info_place(),
                                                     projection=CoordinateInfo.name)
            self.blit_manager.add_artist(self.info_axes)

        self.info_axes.update_info(data)
