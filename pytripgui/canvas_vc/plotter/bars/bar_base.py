from abc import ABC

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.pyplot import colorbar

from pytripgui.canvas_vc.plotter.bars.projection_enum import BarProjection
"""
This class and its subclasses were made to remove extra responsibilities from mpl_plotter.
This class holds basic logic and parameters that are shared between all of its subclasses.
If it is needed, subclasses can change those parameters - like dos_bar does.
"""


class BarBase(ABC, Axes):
    """
    Abstract base class that holds information how bars should be made
    """
    # projection registration in matplotlib requires class to have parameter called "name"
    name: str = BarProjection.DEFAULT.value

    def __init__(self, fig, rect, **kwargs):
        super().__init__(fig, rect, **kwargs)
        self.text_color = "#33DD33"  # text decorator colour
        self.fg_color = 'white'  # colour for colourbar ticks and labels
        self.bg_color = 'black'  # background colour, i.e. between colourbar and CTX/DOS/LET plot
        self.cb_fontsize = 8  # fontsize of colourbar labels
        self.label = 'DEFAULT_LABEL'
        self.bar = None

    def plot_bar(self, data, **kwargs):
        """
        Plots bar based on passed data
        """
        cb = colorbar(data, cax=self)
        cb.set_label(self.label, color=self.fg_color, fontsize=self.cb_fontsize)
        cb.outline.set_edgecolor(self.bg_color)
        cb.ax.yaxis.set_tick_params(color=self.fg_color)
        plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color=self.fg_color)
        cb.ax.yaxis.set_tick_params(color=self.fg_color, labelsize=self.cb_fontsize)
        self.bar = cb

    def clear_bar(self):
        """
        Clears whole axes, removes bar.
        """
        self.cla()
