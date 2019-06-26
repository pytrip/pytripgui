from PyQt5.QtWidgets import QApplication
from pytrip.tripexecuter import Field
from pytrip.tripexecuter import KernelModel
from pytripgui.field_editor.field_view import FieldQtView
from pytripgui.field_editor.field_cont import FieldController
import sys


app = QApplication(sys.argv)

global_kernels = [KernelModel("kernelOne"), KernelModel("kernelTwo"),
                  KernelModel("selectedOne"), KernelModel("kernelFour")]


def get_test_model():
    model = Field()
    model.isocenter = [1.1, 1.2, 1.3]
    model.gantry = 2.1
    model.couch = 3.1
    model.fwhm = 4.1
    model.raster_step = [5.1, 5.2]
    model.dose_extension = 6.1
    model.contour_extension = 7.2
    model.zsteps = 8.2
    model.kernel = (global_kernels[2])   # TODO in pytrip
    return model


model = get_test_model()
view = FieldQtView()

controller = FieldController(model, view, global_kernels)
controller.set_view_from_model()

view.show()
app.exec_()

controller.set_view_from_model()
view.show()

sys.exit(app.exec_())
