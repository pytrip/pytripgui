import logging

from anytree import NodeMixin

from pytripgui.field_vc.field_model import FieldModel
from pytripgui.plan_executor.patient_model import PatientModel
from pytrip.tripexecuter.plan import Plan
from pytrip.tripexecuter.kernel import KernelModel

logger = logging.getLogger(__name__)


class TreeItem(NodeMixin):
    def __init__(self):
        self.children = ()
        self.data = None
        self.state = None

    # For qt TreeView
    def has_index(self, p_int):
        return p_int < len(self.children)

    def has_children(self):
        return len(self.children) > 0

    def row_count(self):
        return len(self.children)

    def index(self, p_int, p_int_1):
        # only one column is supported
        if not self.has_index(p_int) or p_int_1 != 0:
            return None

        return self.children[p_int]

    def row(self):
        """
        :returns Number (row) of this element (on parent list)
        """
        if self.parent is None:
            return 0
        return self.parent.children.index(self)

    def add_child(self, child):
        """
        With this method You add item to tree.
        Remember to not add one child multiple times.
        :param child: Child to add
        """
        self.children += (child, )

    def delete_child(self, child):
        """
        With this method You delete item from tree.
        :param child: Child to add
        """
        children = list(self.children)
        children.remove(child)
        self.children = children


class PatientList(TreeItem):
    """
    Root item in TreeModel
    """
    def __init__(self, name="PatientList"):
        super().__init__()
        self.name = name
        self.parent = None

    def __repr__(self):
        return self.name


class PatientItem(TreeItem):
    def __init__(self):
        super().__init__()

        self.data = PatientModel()

    def __repr__(self):
        if self.data.name:
            return "Patient: " + self.data.name
        return "No named patient"


class SimulationResultItem(TreeItem):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        if self.data:
            return self.data.__str__()
        return "Empty simulation"


class PlanItem(TreeItem):
    def __init__(self):
        super().__init__()

        self._data = Plan()
        self.field_counter = 1

    def __repr__(self):
        if self.data.basename:
            return "Plan: " + self.data.basename
        return "No named plan"

    def add_child(self, child):
        super().add_child(child)

        if isinstance(child, FieldItem):
            child.data.number = self.field_counter
            self.field_counter = self.field_counter + 1

    @property
    def data(self):
        self._data.fields = [child.data for child in self.children]
        for field in self._data.fields:
            field.kernel = self._data.default_kernel
        return self._data

    @data.setter
    def data(self, data):
        self._data = data


class FieldItem(TreeItem):
    def __init__(self):
        super().__init__()

        self.data = FieldModel()

    def __repr__(self):
        return "Field: " + str(self.data.number)


class KernelItem(TreeItem):
    def __init__(self, parent=None):
        super().__init__()

        self.data = KernelModel()

        if parent and not isinstance(parent, FieldItem):
            raise Exception("Only FieldItem can be parent of KernelItem")
        self.parent = parent

    def __repr__(self):
        if self.data.name:
            return self.data.name
        return "No named kernel"

    def clone(self):
        """
        :return: New item which contains same data. Only parent item is not copied
        """
        tmp = KernelItem()
        tmp.data = self.data
        return tmp
