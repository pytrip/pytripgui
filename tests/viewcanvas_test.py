import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog

from pytripgui.model.plot_model import PlotModel

from pytripgui.model.dos_container import DosContainer
from pytripgui.model.let_container import LetContainer

from pytripgui.viewcanvas_vc.viewcanvas_view import ViewCanvasView
from pytripgui.viewcanvas_vc.viewcanvas_cont import ViewCanvasCont


import pytrip as pt
import os

def open_voxelplan(smodel, ctx_path):
    """
    Open a Voxelplan type CTX and possibly a VDX if one exists with the same basename.
    """

    model = smodel  # local object of plot_model
    pm = smodel.plot  # local object of plot_model

    # Get the CTX cubes first
    ctx = pt.CtxCube()
    ctx.read(ctx_path)

    # update model
    model.ctx = ctx
    pm.ctx = ctx

    # Point to center of slices for default plotting
    pm.xslice = int(ctx.dimx * 0.5)
    pm.yslice = int(ctx.dimy * 0.5)
    pm.zslice = int(ctx.dimz * 0.5)
    # TODO: we assume transversal view as start. fixme.
    pm.slice_pos_idx = int(ctx.dimz * 0.5)

    # show file basename in window title

    # Check if there is a VDX file with the same basename
    from pytrip.util import TRiP98FilePath
    _d = TRiP98FilePath(ctx_path, ctx).dir_basename  # returns full path, but without suffix.
    vdx_path = _d + ".vdx"

    # If VDX is there, load it.
    if os.path.isfile(vdx_path):
        vdx = pt.VdxCube(smodel.ctx)
        vdx.read(vdx_path)

        # update model
        model.vdx = vdx
        pm.vdx = vdx

        # enable all VOIs to be plotted
        for voi in vdx.vois:
            pm.vois.append(voi)


def test1():
    app = QApplication(sys.argv)

    model = PlotModel()
    model2 = PlotModel()

    ctx = pt.CtxCube()
    ctx.read("/home/deerjelen/guit/TST000000.hed")

    model.import_dose_from_file("/home/deerjelen/guit/TST000000.phys.dos")
    model.import_let_from_file("/home/deerjelen/guit/TST000000.dosemlet.hed")
    model.set_ctx(ctx)
    model2.projection_selector.plane = "Sagittal"
    model2.set_ctx(ctx)
    # dos.plot.let = dos.let_container.import_from_file("/home/deerjelen/guit/TST000000.dosemlet.dos")
    # open_voxelplan(dos, "/home/deerjelen/guit/z/TST000000.hed")

    widget = UiViewCanvas()
    view = ViewCanvasView()
    widget.vc_layout.addWidget(view)
    cont = ViewCanvasCont(model, view)
    # cont.plot_ctx()
    # cont.update_viewcanvas()

    widget.show()

    app.exec_()

def test2():
    app = QApplication(sys.argv)

    # dos = MainModel()
    model = PlotModel()
    model2 = PlotModel()

    dos = DosContainer().import_from_file("/home/deerjelen/guit/TST000000.phys.dos")
    let = LetContainer().import_from_file("/home/deerjelen/guit/TST000000.dosemlet.hed")

    ctx = pt.CtxCube()
    ctx.read("/home/deerjelen/guit/TST000000.hed")

    model.set_let(let)
    model.set_dose(dos)
    model.set_ctx(ctx)
    model2.projection_selector.plane = "Sagittal"
    model2.set_ctx(ctx)
    model2.set_dose(dos)
    # dos.plot.let = dos.let_container.import_from_file("/home/deerjelen/guit/TST000000.dosemlet.dos")
    # open_voxelplan(dos, "/home/deerjelen/guit/z/TST000000.hed")

    widget = ViewCanvasView()
    cont = ViewCanvasCont(model, widget)
    cont.update_viewcanvas()

    widget.show()

    app.exec_()


test2()
