from PyQt5.QtWidgets import QApplication
from pytripgui.field_editor.field_model import FieldModel
from pytripgui.field_editor.field_view import FieldQtView
from pytripgui.field_editor.field_cont import FieldController
import sys



app = QApplication(sys.argv)

model = FieldModel()
model.set_isocenter_manually(True)
model.set_isocenter_values([1.1, 1.2, 1.3])
model.set_gantry_angle_value(2.1)
model.set_couch_angle_value(3.1)
model.set_spot_size_value(4.1)
model.set_raster_step_value([5.1, 5.2])
model.set_dose_extension_value(6.1)
model.set_contour_extension_value(7.2)
model.set_depth_steps_value(8.2)

view = FieldQtView()

FieldController(model, view).set_view_from_model()

view.show()

#w.show()

sys.exit(app.exec_())
