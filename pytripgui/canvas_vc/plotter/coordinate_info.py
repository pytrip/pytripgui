from collections import deque
from typing import Dict, Optional

import numpy as np
from matplotlib.projections import register_projection
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.axis3d import Axis

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
        self._x, self._y = np.meshgrid(r, r)
        self._one = np.ones(4).reshape(2, 2)
        # wireframe and surface parameters
        self._inactive_plane_alpha: float = 0.5
        self._wireframe_color: str = 'grey'
        # set surfaces' colors
        self._colors: Dict[str, str] = {'Transversal': 'limegreen', 'Sagittal': 'orangered', 'Coronal': 'royalblue'}
        # set default last plane
        self._last_plane: str = 'DEFAULT_PLANE'
        # flag that tells if plot should be initialized or updated
        self._data_set: bool = False
        # set default surfaces
        self._surfaces: Dict[str, Optional[Poly3DCollection]] = {'Transversal': None, 'Sagittal': None, 'Coronal': None}
        # set rotation values for each plane
        self._rotations: Dict[str, int] = {'Transversal': 0, 'Sagittal': 1, 'Coronal': -1}
        # set axis to be changed for each plane
        self._xyz_axis: Dict[str, Axis] = {'Transversal': self.zaxis, 'Sagittal': self.xaxis, 'Coronal': self.yaxis}

        self._plot_initial_state()

    def _plot_initial_state(self):
        # set plot labels
        self.set_xlabel('x')
        self.set_ylabel('y')
        self.set_zlabel('z')
        # color labels
        for plane, axis in self._xyz_axis.items():
            axis.label.set_color(self._colors[plane])
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
        self.plot_wireframe(self._x, self._y, self._one, alpha=self._inactive_plane_alpha, color=self._wireframe_color)
        self.plot_wireframe(self._x, self._y, -self._one, alpha=self._inactive_plane_alpha, color=self._wireframe_color)
        self.plot_wireframe(self._x, -self._one, self._y, alpha=self._inactive_plane_alpha, color=self._wireframe_color)
        self.plot_wireframe(self._x, self._one, self._y, alpha=self._inactive_plane_alpha, color=self._wireframe_color)
        self.plot_wireframe(self._one, self._x, self._y, alpha=self._inactive_plane_alpha, color=self._wireframe_color)
        self.plot_wireframe(-self._one, self._x, self._y, alpha=self._inactive_plane_alpha, color=self._wireframe_color)
        # plot arrows for axis indicators
        # indicators should be in order in which xyz_axis ale colors are ordered
        indicators = [('^', [1]), ('>', [1]), ('>', [0])]
        indicators_params = zip(self._xyz_axis.values(), indicators, self._colors.values())
        for axis, (marker, position), color in indicators_params:
            axis.line.set_marker(marker)
            axis.line.set_markevery(position)
            axis.line.set_markerfacecolor(color)
            axis.line.set_color(color)
            axis.line.set_clip_on(False)

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
                self._plot_plane(plane, current_slices, last_slices, False)

            self._data_set = True

        else:
            # if last and current plane are not the same remove and plot surface that represents last plane
            if self._last_plane != current_plane:
                self._surfaces[self._last_plane].remove()
                self._plot_plane(self._last_plane, current_slices, last_slices, False)

            # remove and plot surface that represents current plane
            self._surfaces[current_plane].remove()
            self._plot_plane(current_plane, current_slices, last_slices, True)

        self._last_plane = current_plane

    def _plot_plane(self, plane: str, current_slices: Dict[str, int], last_slices: Dict[str, int],
                    is_current_plane: bool) -> None:
        # rescale from [0...last slice] to [-1...1]
        ones = np.multiply(self._one, 2 * current_slices[plane] / last_slices[plane]) - 1

        # get proper vector by rotating base one
        xyz = deque([self._x, self._y, ones])
        xyz.rotate(self._rotations[plane])
        x, y, z = xyz

        # get axis assigned to current plane
        axis: Axis = self._xyz_axis[plane]

        # get color assigned to current plane
        color: str = self._colors[plane]

        # plot full color if this is current plane
        alpha: float = 1.0
        if not is_current_plane:
            # plot partially transparent if it is not current plane
            alpha = self._inactive_plane_alpha

        # change axis alpha
        axis.line.set_alpha(alpha)
        # change axis label alpha
        axis.label.set_alpha(alpha)

        # plot proper plane
        self._surfaces[plane] = self.plot_surface(x, y, z, alpha=alpha, color=color)


register_projection(CoordinateInfo)
