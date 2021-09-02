from matplotlib.axes import Axes
from matplotlib.figure import Figure

from pytripgui.canvas_vc.objects.ctx import Ctx
from pytripgui.canvas_vc.objects.dos import Dos
from pytripgui.canvas_vc.objects.let import Let
from pytripgui.canvas_vc.plotter.bars import BarProjection
from pytripgui.canvas_vc.plotter.coordinate_info import CoordinateInfo
from pytripgui.canvas_vc.plotter.images import CtxImage, DoseImage, LetImage
from pytripgui.canvas_vc.plotter.managers import PlacementManager, BlitManager
from pytripgui.canvas_vc.plotter.managers.voi_manager import VoiManager
'''
This class was created to remove extra responsibilities from mpl_plotter.
It hides how things are plotted, if they are present and how they are removed.
Thanks to that, mpl_plotter does not know how most things are done
and delegates almost everything connected to plotting to this class.
'''


class PlottingManager:
    """
    Holds high level logic for plotting/removing images and bars.
    """
    def __init__(self, figure: Figure, blit_manager: BlitManager):
        """
        Parameters:
        ----------
        figure : Figure -- object on which everything will be plotted

        blit_manager : BlitManager -- object that is responsible for fast figure updating
        """
        self.figure = figure
        self.placement_manager = PlacementManager(self.figure)
        self.blit_manager = blit_manager
        # main plot
        self.axes: Axes = self._initialize_axes()
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
        self.figure.patch.set_facecolor('black')

        # plotting VOIs
        self._voi_manager: VoiManager = VoiManager(self.axes, self.blit_manager)

    def _initialize_axes(self) -> Axes:
        axes = self.figure.add_subplot(self.placement_manager.get_main_plot_place())
        axes.grid(False)
        axes.set_xticks([])
        axes.set_yticks([])
        return axes

    def remove_dos(self) -> None:
        """
        Removes dose image and dose bar if present.

        Changes WILL NOT be visible until BlitManager updates them.
        """
        if self.dose.is_present():
            self.blit_manager.remove_artist(self.dose.get())
            self.dose.remove()
        if self.dose_bar:
            self.placement_manager.remove_dose_bar()
            self.dose_bar.remove()
            self.dose_bar = None

    def plot_dos(self, data: Dos) -> None:
        """
        Plots dose image and dose bar if not present, adds image to BlitManager.
        In opposite case, updates dose image data.

        Changes WILL NOT be visible until BlitManager updates them.
        """
        if not self.dose.is_present() and data.max_dose > data.min_dose:
            self.dose.plot(data)
            self.blit_manager.add_artist(self.dose.get())
            if not self.dose_bar:
                self.placement_manager.add_dose_bar()
                self._plot_dos_bar(data)
        else:
            self.dose.update(data)

    def _plot_dos_bar(self, data: Dos) -> None:
        self.dose_bar = self.figure.add_subplot(self.placement_manager.get_dose_bar_place(),
                                                projection=BarProjection.DOS.value)
        self.dose_bar.plot_bar(self.dose.get(), scale=data.dos_scale)

    def remove_let(self) -> None:
        """
        Removes LET image and LET bar if present.

        Changes WILL NOT be visible until BlitManager updates them.
        """
        if self.let.is_present():
            self.blit_manager.remove_artist(self.let.get())
            self.let.remove()
        if self.let_bar:
            self.placement_manager.remove_let_bar()
            self.let_bar.clear_bar()
            self.let_bar = None

    def plot_let(self, data: Let) -> None:
        """
        Plots LET image and LET bar if not present, adds image to BlitManager.
        In opposite case, updates LET image data.

        Changes WILL NOT be visible until BlitManager updates them.
        """
        if not self.let.is_present():
            self.let.plot(data)
            self.blit_manager.add_artist(self.let.get())
            if not self.let_bar:
                self.placement_manager.add_let_bar()
                self._plot_let_bar()
        else:
            self.let.update(data)

    def _plot_let_bar(self) -> None:
        self.let_bar = self.figure.add_subplot(self.placement_manager.get_let_bar_place(),
                                               projection=BarProjection.LET.value)
        self.let_bar.plot_bar(self.let.get())

    def remove_ctx(self) -> None:
        """
        Removes CTX image and CTX bar if present.

        Changes WILL NOT be visible until BlitManager updates them.
        """
        if self.ctx.is_present():
            self.blit_manager.remove_artist(self.ctx.get())
            self.ctx.remove()
        if self.ctx_bar:
            self.placement_manager.remove_ctx_bar()
            self.ctx_bar.clear_bar()
            self.ctx_bar = None

    def plot_ctx(self, data: Ctx) -> None:
        """
        Plots CTX image and CTX bar if not present, adds image to BlitManager.
        In opposite case, updates CTX image data.

        Plots information about slices positions if not present, adds plot to BlitManager.
        In opposite case, updates plot data.

        Changes WILL NOT be visible until BlitManager updates them.
        """
        self._plot_coordinate_info(data)
        if not self.ctx.is_present():
            self.ctx.plot(data)
            self.blit_manager.add_artist(self.ctx.get())
            if not self.ctx_bar:
                self.placement_manager.add_ctx_bar()
                self._plot_ctx_bar()
        else:
            self.ctx.update(data)

    def _plot_ctx_bar(self) -> None:
        self.ctx_bar = self.figure.add_subplot(self.placement_manager.get_ctx_bar_place(),
                                               projection=BarProjection.CTX.value)
        self.ctx_bar.plot_bar(self.ctx.get())

    def _plot_coordinate_info(self, data: Ctx) -> None:
        if self.info_axes is None:
            self.info_axes = self.figure.add_subplot(self.placement_manager.get_coord_info_place(),
                                                     projection=CoordinateInfo.name)
            self.blit_manager.add_artist(self.info_axes)
        else:
            self.info_axes.update_info(data)

    def plot_voi(self, vdx):
        self._voi_manager.plot_voi(vdx)

    def remove_voi(self):
        self._voi_manager.remove_voi()
