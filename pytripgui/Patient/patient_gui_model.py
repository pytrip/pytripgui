import logging

from pytripgui.plan_vc import PlanQtView
from pytripgui.plan_vc import PlanController
from pytripgui.field_vc import FieldQtView
from pytripgui.field_vc import FieldController
from pytripgui.model.plot_model import PlotModel
from pytripgui.plan_executor.patient_model import PatientModel

logger = logging.getLogger(__name__)


class PatientGui(PatientModel):
    def __init__(self, global_kernels):
        PatientModel.__init__(self)

        self.global_kernels = global_kernels
        self.plot_model = PlotModel()

    def add_new_plan(self, name=None):
        pass

    def edit_plan(self, plan):
        logger.debug("edit_plan() {}".format(None))

        view = PlanQtView()

        controller = PlanController(plan, view, self.global_kernels, self.vdx.vois)
        controller.set_view_from_model()
        view.show()

    def add_new_field(self, plan):
        logger.debug("add_field_new() {}".format(None))

        new_field = PatientModel.create_new_field()
        view = FieldQtView()
        default_kernel = self.global_kernels[0]  # TODO select default kernel
        new_field.kernel = default_kernel

        controller = FieldController(new_field, view, self.global_kernels)
        controller.set_view_from_model()
        view.show()

        if controller.user_clicked_save:
            new_field.basename = "Field_{}".format(new_field.number)  # TODO it not generate unique numbers
            plan.fields.append(new_field)

    def edit_field(self, field):
        logger.debug("edit_field() {}".format(None))

        view = FieldQtView()

        controller = FieldController(field, view, self.global_kernels)
        controller.set_view_from_model()
        view.show()
