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

    def index(self, p_int, p_int_1, obj):
        from PyQt5.QtCore import QModelIndex

        if not self.has_index(p_int) or \
                p_int_1 != 0:   # only one column is supported
            return QModelIndex()

        index = obj.createIndex(p_int, p_int_1, self.children[p_int])
        return index

    def row(self):
        """
        :returns Number (row) of this element (on parent list)
        """
        if self.parent is None:
            return 0
        else:
            return self.parent.children.index(self)


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

    def add_child(self, child=None):
        """
        With this method You add item to tree.
        Remember to not add same child more than once.
        :param child: Child to add
        """
        if child is None:
            self.children += tuple([PatientItem()])
            return

        if isinstance(child, PatientItem):
            self.children += tuple([child])
        else:
            raise Exception("Only PatientItem can be added as child")


class PatientItem(TreeItem):
    def __init__(self, parent=None):
        super().__init__()

        self.data = PatientModel()

        if parent and not isinstance(parent, PatientList):
            raise Exception("Only PatientList can be parent of PatientItem")
        else:
            self.parent = parent

    def __repr__(self):
        return self.data.name

    def add_child(self, child=None):
        """
        With this method You add item to tree.
        Remember to not add same child more than once.
        :param child: Child to add
        """
        if child is None:
            self.children += tuple([PlanItem()])
            return

        if isinstance(child, PlanItem):
            self.children += tuple([child])
        else:
            raise Exception("Only PlanItem can be added as child")


class PlanItem(TreeItem):
    def __init__(self, parent=None):
        super().__init__()

        self.data = Plan()

        if parent and not isinstance(parent, PatientItem):
            raise Exception("Only PatientItem can be parent of PlanItem")
        else:
            self.parent = parent

    def __repr__(self):
        return self.data.basename

    def add_cloned_child(self, child):
        """
        Uses child.clone() method to put clone of child onto tree
        :param child: Data to put into tree
        :return:
        """
        if isinstance(child, FieldItem):
            self.children += tuple([child.clone()])
        else:
            raise Exception("Only FieldItem can be added as child")


class FieldItem(TreeItem):
    def __init__(self, data=Field(), parent=None):
        super().__init__()

        self.data = data

        if parent and not isinstance(parent, PlanItem):
            raise Exception("Only PlanItem can be parent of FieldItem")
        else:
            self.parent = parent

    def __repr__(self):
        return self.data.basename

    def add_cloned_child(self, child):
        if isinstance(child, KernelItem):
            self.children += tuple([child.clone()])
        else:
            raise Exception("Only KernelItem can be added as child")

    def clone(self):
        """
        :return: New item which contains same data. Only parent is not copied
        """
        tmp = FieldItem()
        tmp.data = self.data
        for child in self.children:
            tmp.add_cloned_child(child)
        return tmp


class KernelItem(TreeItem):
    def __init__(self, parent=None):
        super().__init__()

        self.data = KernelModel()

        if parent and not isinstance(parent, FieldItem):
            raise Exception("Only FieldItem can be parent of KernelItem")
        else:
            self.parent = parent

    def __repr__(self):
        return self.data.basename

    def clone(self):
        """
        :return: New item which contains same data. Only parent item is not copied
        """
        tmp = KernelItem()
        tmp.data = self.data
        return tmp
