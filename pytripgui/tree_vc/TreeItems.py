from anytree import NodeMixin, RenderTree
import logging

from pytripgui.plan_executor.patient_model import PatientModel
from pytrip.tripexecuter.plan import Plan
from pytrip.tripexecuter.field import Field

logger = logging.getLogger(__name__)


class PatientList(NodeMixin):
    """
    Root item in TreeModel
    """
    def __init__(self, name="PatientList"):
        super().__init__()
        self.name = name
        self.parent = None

    def __repr__(self):
        return self.name

    def add_child(self, child):
        if isinstance(child, PatientItem):
            self.children += tuple([child])
        else:
            raise Exception("PatientItem can only be added to PatientList")

    def has_index(self, p_int):
        return p_int < len(self.children)

    # For qt TreeView
    def has_children(self):
        return len(self.children) > 0

    def row_count(self):
        return len(self.children)

    def index(self, p_int, p_int_1, obj):
        from PyQt5.QtCore import QModelIndex

        if not self.has_index(p_int) or \
                p_int_1 != 0:   # only one column is supported
            return QModelIndex()

        index = obj.createIndex(p_int, p_int_1, self.children[p_int])
        return index


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

    # For qt TreeView
    def has_children(self):
        return len(self.children) > 0

    def __repr__(self):
        return self.data.name


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

patient_list.add_child(udo)
patient_list.add_child(udo1)
patient_list.children += tuple([PatientItem()])

udo.children += tuple([PlanItem()])
udo.children[0].children += tuple([FieldItem()])

print(udo)

print(RenderTree(patient_list))
