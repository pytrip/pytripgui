from anytree import NodeMixin
import logging

from pytripgui.plan_executor.patient_model import PatientModel
from pytrip.tripexecuter.plan import Plan
from pytrip.tripexecuter.field import Field
from pytrip.tripexecuter.kernel import KernelModel

logger = logging.getLogger(__name__)


class TreeItem(NodeMixin):
    def __init__(self):
        super().__init__()

    # For qt TreeView
    def has_index(self, p_int):
        return p_int < len(self.children)

    def has_children(self):
        return len(self.children) > 0

    def row_count(self):
        return len(self.children)

    def index(self, p_int, p_int_1):
        if not self.has_index(p_int) or \
                p_int_1 != 0:   # only one column is supported
            return None

        return self.children[p_int]

    def row(self):
        """
        :returns Number (row) of this element (on parent list)
        """
        if self.parent is None:
            return 0
        else:
            return self.parent.children.index(self)

    def add_child(self, child):
        """
        With this method You add item to tree.
        Remember to not add one child multiple times.
        :param child: Child to add
        """
        self.children += (child,)


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
            return self.data.name
        return "No named patient"


class PlanItem(TreeItem):
    def __init__(self):
        super().__init__()

        self.data = Plan()

    def __repr__(self):
        if self.data.basename:
            return self.data.basename
        return "No named plan"


class FieldItem(TreeItem):
    def __init__(self):
        super().__init__()

        self.data = Field()

    def __repr__(self):
        if self.data.basename:
            return self.data.basename
        return "No named field"


class KernelItem(TreeItem):
    def __init__(self, parent=None):
        super().__init__()

        self.data = KernelModel()

        if parent and not isinstance(parent, FieldItem):
            raise Exception("Only FieldItem can be parent of KernelItem")
        else:
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
