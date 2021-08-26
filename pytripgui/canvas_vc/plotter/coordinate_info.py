from typing import Dict, List, Optional, Callable

import numpy as np
from matplotlib.projections import register_projection
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from pytripgui.canvas_vc.objects.ctx import Ctx


class CoordinateInfo(Axes3D):
    """
    Special class that inherits from Axes3D from matplotlib.

    Holds logic for plotting wireframe cube, which represents patient, with three surfaces.
    Those surfaces' positions represent number of slice that user sees in all three perspectives.

    It is registered as projection in matplotlib.

    Examples of usage:
        1) using string:
            figure.add_subplot(111, projection='CoordinateInfo')
        2) using class parameter:
            figure.add_subplot(123, projection=CoordinateInfo.name)
    """
    # name to register that as projection in matplotlib
    name: str = 'CoordinateInfo'

    def __init__(self, fig, rect, **kwargs):
        super().__init__(fig, rect, **kwargs)

        # variables to ease wireframe plotting
        r = [-1, 1]
        self._x, self.y = np.meshgrid(r, r)
        self._one = np.ones(4).reshape(2, 2)

        # wireframe and surface parameters
        self._alpha: float = 0.4
        self._wireframe_color: str = 'grey'
        self._transversal_color: str = 'lime'
        self._sagittal_color: str = 'red'
        self._coronal_color: str = 'cyan'

        self._plot_initial_state()

        # set default last plane
        self._last_plane: str = 'DEFAULT_PLANE'
        # flag that tells if plot should be initialized or updated
        self._data_set: bool = False
        # set default surfaces
        self._surfaces: Dict[str, Optional[Poly3DCollection]] = {'Transversal': None, 'Sagittal': None, 'Coronal': None}
        # set actions to be done depending on surface type
        self._actions: Dict[str, Callable] = {
            'Transversal': self._plot_transversal,
            'Sagittal': self._plot_sagittal,
            'Coronal': self._plot_coronal
        }

    def _plot_initial_state(self):
        # set plot labels
        self.set_xlabel('x')
        self.xaxis.label.set_color(self._sagittal_color)
        self.set_ylabel('y')
        self.yaxis.label.set_color(self._coronal_color)
        self.set_zlabel('z')
        self.zaxis.label.set_color(self._transversal_color)
        # remove grid and axes ticks
        self.grid(False)
        self.set_xticks([])
        self.set_yticks([])
        self.set_zticks([])
        # set background color
        self.set_facecolor('black')
        # turn off panes visibility
        self.xaxis.pane.set_visible(False)
        self.yaxis.pane.set_visible(False)
        self.zaxis.pane.set_visible(False)
        # set proper distance from plot
        self.dist = 18
        # plot cubic frame
        self.plot_wireframe(self._x, self.y, self._one, alpha=self._alpha, color=self._wireframe_color)
        self.plot_wireframe(self._x, self.y, -self._one, alpha=self._alpha, color=self._wireframe_color)
        self.plot_wireframe(self._x, -self._one, self.y, alpha=self._alpha, color=self._wireframe_color)
        self.plot_wireframe(self._x, self._one, self.y, alpha=self._alpha, color=self._wireframe_color)
        self.plot_wireframe(self._one, self._x, self.y, alpha=self._alpha, color=self._wireframe_color)
        self.plot_wireframe(-self._one, self._x, self.y, alpha=self._alpha, color=self._wireframe_color)
        # plot arrows for axis indicators
        indicator_params = [(self.xaxis.line, '>', [1], self._sagittal_color),
                            (self.yaxis.line, '>', [0], self._coronal_color),
                            (self.zaxis.line, '^', [1], self._transversal_color)]
        for line, marker, position, color in indicator_params:
            line.set_marker(marker)
            line.set_markevery(position)
            line.set_markerfacecolor(color)
            line.set_color(color)
            line.set_clip_on(False)

    def update_info(self, data: Ctx) -> None:
        """
        Updates positions of surfaces.

        First invocation plots all surfaces.
        Next invocations update position of one surface or two surfaces, if perspective has changed.

        Parameters:
        ----------
        data : Ctx - object that has projection_selector

        """
        current_plane: str = data.projection_selector.plane
        current_slices: Dict[str, int] = data.projection_selector.get_current_slices()
        last_slices: Dict[str, int] = data.projection_selector.get_last_slices()

        # initialize whole plot if necessary
        if not self._data_set:
            for plane in self._surfaces:
                self._plot_plane(plane, current_slices, last_slices, current_plane)

            self._data_set = True

        else:
            # if last and current plane are not the same remove and plot surface that represents last plane
            if self._last_plane != current_plane:
                self._surfaces[self._last_plane].remove()
                self._plot_plane(self._last_plane, current_slices, last_slices, current_plane)

            # remove and plot surface that represents current plane
            self._surfaces[current_plane].remove()
            self._plot_plane(current_plane, current_slices, last_slices, current_plane)

        self._last_plane = current_plane

    def _plot_plane(self, plane: str, current_slices: Dict[str, int], last_slices: Dict[str, int],
                    current_plane: str) -> None:
        # rescale from [0...last slice] to [-1...1]
        ones = np.multiply(self._one, 2 * current_slices[plane] / last_slices[plane]) - 1
        # plot proper plane
        self._surfaces[plane] = self._actions[plane](ones, current_plane == plane)

    def _plot_transversal(self, ones: List[List[int]], is_current_plane: bool) -> Poly3DCollection:
        # plot full color if this is current plane
        if is_current_plane:
            # set alpha back to normal
            self.zaxis.line.set_alpha(1)
            self.zaxis.label.set_alpha(1)
            return self.plot_surface(self._x, self.y, ones, color=self._transversal_color)

        # change axis alpha
        self.zaxis.line.set_alpha(self._alpha)
        # change axis label alpha
        self.zaxis.label.set_alpha(self._alpha)
        # plot partially transparent if it is not current plane
        return self.plot_surface(self._x, self.y, ones, alpha=self._alpha, color=self._transversal_color)

    def _plot_sagittal(self, ones: List[List[int]], is_current_plane: bool) -> Poly3DCollection:
        if is_current_plane:
            self.xaxis.line.set_alpha(1)
            self.xaxis.label.set_alpha(1)
            return self.plot_surface(ones, self._x, self.y, color=self._sagittal_color)

        self.xaxis.line.set_alpha(self._alpha)
        self.xaxis.label.set_alpha(self._alpha)
        return self.plot_surface(ones, self._x, self.y, alpha=self._alpha, color=self._sagittal_color)

    def _plot_coronal(self, ones: List[List[int]], is_current_plane: bool) -> Poly3DCollection:
        if is_current_plane:
            self.yaxis.line.set_alpha(1)
            self.yaxis.label.set_alpha(1)
            return self.plot_surface(self._x, ones, self.y, color=self._coronal_color)

        self.yaxis.line.set_alpha(self._alpha)
        self.yaxis.label.set_alpha(self._alpha)
        return self.plot_surface(self._x, ones, self.y, alpha=self._alpha, color=self._coronal_color)


register_projection(CoordinateInfo)
