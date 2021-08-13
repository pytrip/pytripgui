import numpy as np
from matplotlib.projections import register_projection
from mpl_toolkits.mplot3d import Axes3D


class CoordinateInfo(Axes3D):
    # name to register that as projection in matplotlib
    name: str = 'CoordinateInfo'

    def __init__(self, fig, rect, **kwargs):
        super().__init__(fig, rect, **kwargs)
        # variables to ease wireframe plotting
        r = [-1, 1]
        self.x, self.y = np.meshgrid(r, r)
        self.one = np.ones(4).reshape(2, 2)
        # wireframe and surface parameters
        self.alpha = 0.2
        self.wireframe_color = 'black'
        self.transversal_color = 'g'
        self.sagittal_color = 'r'
        self.coronal_color = 'b'
        # set plot labels
        self.set_xlabel('x')
        self.set_ylabel('y')
        self.set_zlabel('z')
        # remove grid and axes ticks
        self.grid(False)
        self.set_xticks([])
        self.set_yticks([])
        self.set_zticks([])
        # plot cubic frame
        self.plot_wireframe(self.x, self.y, self.one, alpha=self.alpha, color=self.wireframe_color)
        self.plot_wireframe(self.x, self.y, -self.one, alpha=self.alpha, color=self.wireframe_color)
        self.plot_wireframe(self.x, -self.one, self.y, alpha=self.alpha, color=self.wireframe_color)
        self.plot_wireframe(self.x, self.one, self.y, alpha=self.alpha, color=self.wireframe_color)
        self.plot_wireframe(self.one, self.x, self.y, alpha=self.alpha, color=self.wireframe_color)
        self.plot_wireframe(-self.one, self.x, self.y, alpha=self.alpha, color=self.wireframe_color)
        # set proper distance from plot
        self.dist = 18
        # set default last plane
        self._last_plane = 'DEFAULT_PLANE'
        # flag that tells if plot should be initialized or updated
        self._data_set = False
        # set default surfaces
        self._surfaces = {'Transversal': None, 'Sagittal': None, 'Coronal': None}
        self._actions = {
            'Transversal': self._plot_transversal,
            'Sagittal': self._plot_sagittal,
            'Coronal': self._plot_coronal
        }

    def update_info(self, data):
        current_plane = data.projection_selector.plane
        current_slices = data.projection_selector.get_current_slices()
        last_slices = data.projection_selector.get_last_slices()

        # initialize whole plot if necessary
        if not self._data_set:
            for plane in self._surfaces.keys():
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

    def _plot_plane(self, plane, current_slices, last_slices, current_plane):
        # rescale from [0...last slice] to [-1...1]
        ones = np.multiply(self.one, 2 * current_slices[plane] / last_slices[plane]) - 1
        # plot proper plane
        self._surfaces[plane] = self._actions[plane](ones, current_plane == plane)

    def _plot_transversal(self, ones, is_current_plane):
        # plot full color if this is current plane
        if is_current_plane:
            return self.plot_surface(self.x, self.y, ones, color=self.transversal_color)
        # plot partially transparent if it is not current plane
        else:
            return self.plot_surface(self.x, self.y, ones, alpha=self.alpha, color=self.transversal_color)

    def _plot_sagittal(self, ones, is_current_plane):
        if is_current_plane:
            return self.plot_surface(ones, self.x, self.y, color=self.sagittal_color)
        else:
            return self.plot_surface(ones, self.x, self.y, alpha=self.alpha, color=self.sagittal_color)

    def _plot_coronal(self, ones, is_current_plane):
        if is_current_plane:
            return self.plot_surface(self.x, ones, self.y, color=self.coronal_color)
        else:
            return self.plot_surface(self.x, ones, self.y, alpha=self.alpha, color=self.coronal_color)


register_projection(CoordinateInfo)