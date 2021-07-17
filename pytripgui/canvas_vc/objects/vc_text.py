import logging

logger = logging.getLogger(__name__)


class ViewCanvasTextCont:
    """
    This class holds logic for plotting all various text decorators for the ViewCanvas plot.
    # TODO: find better name than "ViewCanvas" for this object.
    """
    def __init__(self, projection_selector):
        self.projection_selector = projection_selector
        self.zoom = 100.0
        self.center = [50.0, 50.0]

    def offset(self, plc):
        """
        """

        bbox = plc.axes.get_window_extent().transformed(plc.figure.dpi_scale_trans.inverted())
        width, height = bbox.width * plc.figure.dpi, bbox.height * plc.figure.dpi
        size = [width, height]

        width = (float(size[0]) / self.zoom) * 100.0
        height = (float(size[1]) / self.zoom) * 100.0
        center = [float(size[0]) * self.center[0] / 100, float(size[1]) * self.center[1] / 100]
        offset = [center[0] - width / 2, center[1] - height / 2]
        return offset

    def plot(self, plc):
        """
        Plot the text overlays
        :params idx: index of slice to be plotted.
        """

        # pm = plc._model
        #
        # size = pm.slice_size
        # offset = self.offset(plc)
        # idx = pm.slice_pos_idx  # current slice index (starts at 0, takes plane of view into account)

        axes = plc.axes

        bbox = plc.axes.get_window_extent().transformed(plc.figure.dpi_scale_trans.inverted())
        width, height = bbox.width * plc.figure.dpi, bbox.height * plc.figure.dpi
        # size = [width, height]
        # width = size[0]
        # height = size[1]
        #
        # _slices = pm.slice_size[2]
        # _slice_pos = pm.slice_pos_mm

        if self.projection_selector.plane == "Transversal":
            markers = ['R', 'L', 'A', 'P']
        elif self.projection_selector.plane == "Sagittal":
            markers = ['D', 'V', 'A', 'P']
        elif self.projection_selector.plane == "Coronal":
            markers = ['R', 'L', 'A', 'P']

        # relative position of orientation markers
        rel_pos = ((0.03, 0.5), (0.95, 0.5), (0.5, 0.02), (0.5, 0.95))

        for i, marker in enumerate(markers):
            axes.text(rel_pos[i][0] * width,
                      rel_pos[i][1] * height,
                      marker,
                      color=plc.text_color,
                      va="top",
                      fontsize=20)

        # # text label on current slice# and position in mm
        # axes.text(#offset[0],
        #           #offset[1] + 3.0 / self.zoom * 100,
        #           "Slice #: {:d}/{:d}\n".format(idx + 1, _slices) +
        #           "Slice Position: {:.1f} mm ".format(_slice_pos),
        #           color=pm.text_color,
        #           va="top",
        #           fontsize=8)
        #
        # # text label on HU higher and lower level
        # # TODO: what does "W / L" mean?
        # axes.text(offset[0] + width / self.zoom * 100,
        #           offset[1] + 3.0 / self.zoom * 100,
        #           "W / L: %d / %d" % (pm.contrast_ct[1], pm.contrast_ct[0]),
        #           ha="right",
        #           color=pm.text_color,
        #           va="top",
        #           fontsize=8)
        #
        # # current plane of view
        # axes.text(offset[0],
        #           offset[1] + (height - 5) / self.zoom * 100,
        #           pm.plane,
        #           color=pm.text_color,
        #           va="bottom",
        #           fontsize=8)
