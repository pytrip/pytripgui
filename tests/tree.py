from anytree import NodeMixin, RenderTree
import logging

from pytripgui.plan_executor.patient_model import PatientModel
from pytrip.tripexecuter.plan import Plan
from pytrip.tripexecuter.field import Field

logger = logging.getLogger(__name__)


class PatientList(NodeMixin):
    def __init__(self):
        super().__init__()
        self.parent = None
        self.data = list()

    def _post_attach_children(self, children):
        for child in children:
            self.data.append(child.data)


class PatientItem(NodeMixin):
    def __init__(self, data=PatientModel(), parent=None, children=None):
        super().__init__()
        self.parent = parent
        if children:
            self.children = children

        if isinstance(data, PatientModel):
            self.data = data
        else:
            raise Exception("FieldItem can only holds field data")

        if parent and not isinstance(parent, PatientList):
            raise Exception("FieldItems can only be added to PlanItem")

    def _post_attach_children(self, children):
        print("Adding plan to PatientItem")
        for child in children:
            self.data.plans.append(child.data)


class PlanItem(NodeMixin):
    def __init__(self, data=Plan(), parent=None, children=None):
        super().__init__()
        self.parent = parent
        if children:
            self.children = children

        if isinstance(data, Plan):
            self.data = data
        else:
            raise Exception("FieldItem can only holds field data")

        if parent and not isinstance(parent, PatientItem):
            raise Exception("Only FieldItems can be added to PlanItem")


class FieldItem(NodeMixin):
    def __init__(self, data=Field(), parent=None, children=None):
        super().__init__()
        self.parent = parent
        self.name = "sad"
        if children:
            self.children = children

        if isinstance(data, Field):
            self.data = data
        else:
            raise Exception("FieldItem can only holds field data")

        if parent and not isinstance(parent, PlanItem):
            raise Exception("FieldItems can only be added to PlanItem")


patient_list = PatientList()

udo = PatientItem()
udo1 = PatientItem()

patient_list.children += tuple([udo, udo1])
patient_list.children += tuple([PatientItem()])

udo.children += tuple([PlanItem()])
udo.children[0].children += tuple([FieldItem()])

print(udo)

print(RenderTree(patient_list))
