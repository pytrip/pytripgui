import logging
logger = logging.getLogger(__name__)


class ViewCanvasTextCont(object):
    """
    This class holds logic for plotting all various text decorators for the ViewCanvas plot.
    # TODO: find better name than "ViewCanvas" for this object.
    """

    def __init__(self):
        self.zoom = 100.0
        self.center = [50.0, 50.0]

    def offset(self, plot_model):
        """
        """
        pm = plot_model
        size = pm.slice_size
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

        pm = plc._model

        size = pm.slice_size
        offset = ViewCanvasTextCont().offset(pm)
        idx = pm.slice_pos_idx  # current slice index (starts at 0, takes plane of view into account)

        axes = plc.axes

        width = size[0]
        height = size[1]

        _slices = pm.slice_size[2]
        _slice_pos = pm.slice_pos_mm

        if pm.plane == "Transversal":
            markers = ['R', 'L', 'A', 'P']
        elif pm.plane == "Sagittal":
            markers = ['D', 'V', 'A', 'P']
        elif pm.plane == "Coronal":
            markers = ['R', 'L', 'A', 'P']

        # relative position of orientation markers
        rel_pos = ((0.03, 0.5), (0.95, 0.5), (0.5, 0.02), (0.5, 0.95))

        for i, marker in enumerate(markers):
            axes.text(offset[0] + rel_pos[i][0] * width / self.zoom * 100,
                      offset[1] + rel_pos[i][1] * height / self.zoom * 100,
                      marker,
                      color=pm.text_color,
                      va="top",
                      fontsize=8)

        # text label on current slice# and position in mm
        axes.text(offset[0],
                  offset[1] + 3.0 / self.zoom * 100,
                  "Slice #: {:d}/{:d}\n".format(idx + 1, _slices) + "Slice Position: {:.1f} mm ".format(_slice_pos),
                  color=pm.text_color,
                  va="top",
                  fontsize=8)

        # text label on HU higher and lower level
        # TODO: what does "W / L" mean?
        axes.text(offset[0] + width / self.zoom * 100,
                  offset[1] + 3.0 / self.zoom * 100,
                  "W / L: %d / %d" % (pm.contrast_ct[1], pm.contrast_ct[0]),
                  ha="right",
                  color=pm.text_color,
                  va="top",
                  fontsize=8)

        # current plane of view
        axes.text(offset[0],
                  offset[1] + (height - 5) / self.zoom * 100,
                  pm.plane,
                  color=pm.text_color,
                  va="bottom",
                  fontsize=8)
