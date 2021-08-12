import numpy as np
from matplotlib.projections import register_projection
from mpl_toolkits.mplot3d import Axes3D


class CoordinateInfo(Axes3D):
    # name to register that as projection in matplotlib
    name: str = 'CoordinateInfo'
    # variables to ease wireframe plotting
    r = [-1, 1]
    x, y = np.meshgrid(r, r)
    one = np.ones(4).reshape(2, 2)
    # wireframe and surface parameters
    alpha = 0.2
    wireframe_color = 'black'
    transversal_color = 'g'
    sagittal_color = 'r'
    coronal_color = 'b'

    def __init__(self, fig, rect, **kwargs):
        super().__init__(fig, rect, **kwargs)
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

        if not self._data_set:
            self._initialise(data)
        else:
            current_slices = data.projection_selector.get_current_slices()
            last_slices = data.projection_selector.get_last_slices()

            # if last and current plane are not the same remove and plot surface that represents last plane
            if self._last_plane != current_plane:
                self._surfaces[self._last_plane].remove()
                self._actions[self._last_plane](current_slices, last_slices, current_plane)

            # remove and plot surface that represents current plane
            self._surfaces[current_plane].remove()
            self._actions[current_plane](current_slices, last_slices, current_plane)

        self._last_plane = current_plane

    def _initialise(self, data):
        # TODO remove this method and copy its body to update_info method
        current_plane = data.projection_selector.plane
        current_slices = data.projection_selector.get_current_slices()
        last_slices = data.projection_selector.get_last_slices()

        for plane, f in self._actions.items():
            f(current_slices, last_slices, current_plane)

        self._data_set = True

    def _plot_transversal(self, current_slices, last_slices, current_plane):
        # rescale from [0...last slice] to [-1...1]
        trans_ones = np.multiply(self.one, 2 * current_slices['Transversal'] / last_slices['Transversal']) - 1

        # plot full color if this is current plane
        if current_plane == 'Transversal':
            self._surfaces['Transversal'] = self.plot_surface(self.x, self.y, trans_ones, color=self.transversal_color)
        # plot partially transparent if it is not current plane
        else:
            self._surfaces['Transversal'] = self.plot_surface(self.x,
                                                              self.y,
                                                              trans_ones,
                                                              alpha=self.alpha,
                                                              color=self.transversal_color)

    def _plot_sagittal(self, current_slices, last_slices, current_plane):
        sag_ones = np.multiply(self.one, 2 * current_slices['Sagittal'] / last_slices['Sagittal']) - 1

        if current_plane == 'Sagittal':
            self._surfaces['Sagittal'] = self.plot_surface(sag_ones, self.x, self.y, color=self.sagittal_color)
        else:
            self._surfaces['Sagittal'] = self.plot_surface(sag_ones,
                                                           self.x,
                                                           self.y,
                                                           alpha=self.alpha,
                                                           color=self.sagittal_color)

    def _plot_coronal(self, current_slices, last_slices, current_plane):
        cor_ones = np.multiply(self.one, 2 * current_slices['Coronal'] / last_slices['Coronal']) - 1

        if current_plane == 'Coronal':
            self._surfaces['Coronal'] = self.plot_surface(self.x, cor_ones, self.y, color=self.coronal_color)
        else:
            self._surfaces['Coronal'] = self.plot_surface(self.x,
                                                          cor_ones,
                                                          self.y,
                                                          alpha=self.alpha,
                                                          color=self.coronal_color)


register_projection(CoordinateInfo)
