from abc import ABC

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.pyplot import colorbar

from pytripgui.canvas_vc.bars.projection_enum import BarProjection


# base abstract class for bars
class BarBase(ABC, Axes):
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
        cb = colorbar(data, cax=self)
        cb.set_label(self.label, color=self.fg_color, fontsize=self.cb_fontsize)
        cb.outline.set_edgecolor(self.bg_color)
        cb.ax.yaxis.set_tick_params(color=self.fg_color)
        plt.setp(plt.getp(cb.ax._axes, 'yticklabels'), color=self.fg_color)
        cb.ax.yaxis.set_tick_params(color=self.fg_color, labelsize=self.cb_fontsize)
        self.bar = cb

    def clear_bar(self):
        self.cla()
