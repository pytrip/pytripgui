from enum import Enum
import logging

from PyQt5.QtCore import QVariant, QModelIndex, Qt
from PyQt5.QtCore import QAbstractItemModel

logger = logging.getLogger(__name__)


class PatientItemType(Enum):
    ROOT = 0
    PATIENT = 1
    PLAN = 2
    FIELD = 3


class PatientItem:
    def __init__(self, data, parent=None):
        self._data = data
        self._parent_item = parent
        self._internal_pointer = None   # to prevent garbage collector deleting PatientItem

        if parent is None:
            self._item_type = PatientItemType.ROOT

    def row_count(self):
        return len(self._data)

    def has_children(self):
        if self._item_type == PatientItemType.ROOT:
            return len(self._data) > 0

    def has_index(self, p_int):
        if self._item_type == PatientItemType.ROOT:
            if p_int < len(self._data):
                return True
        return False

    def row(self):
        if self._parent_item:
            return self._parent_item.child_items.index(self._data)
        return 0

    def index(self, p_int, p_int_1, obj):
        if not self.has_index(p_int) or \
                p_int_1 != 0:   # only one column is supported
            return QModelIndex()

        if self._item_type == PatientItemType.ROOT:
            patient_item = PatientItem(self._data[p_int], self)
            patient_item._internal_pointer = patient_item
            index = obj.createIndex(p_int, p_int_1, patient_item)
            return index

        return QModelIndex()

    def parent(self):
        if self._item_type == PatientItemType.ROOT:
            return QModelIndex()
        return self._parent_item

    def child_items(self):
        return self._data

    @property
    def name(self):
        if isinstance(self._data, list):
            return "Patient list"
        else:
            return self._data.name


class PatientTreeModel(QAbstractItemModel):
    def __init__(self, patient_list, parent=None):
        super().__init__(parent)
        self._root_item = PatientItem(patient_list)

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role == Qt.DisplayRole:
            return QVariant("Patients: ")
        return QVariant()

    def columnCount(self, parent=None, *args, **kwargs):
        logger.debug("columnCount()")
        return 1

    def rowCount(self, parent=None, *args, **kwargs):
        logger.debug("rowCount()")
        return self._root_item.row_count()

    def hasChildren(self, parent=None, *args, **kwargs):
        logger.debug("hasChildren()")
        if not parent.isValid():
            return self._root_item.has_children()

        return False

    def index(self, p_int, p_int_1, parent=None, *args, **kwargs):
        logger.debug("index() {} {}".format(p_int, p_int_1))

        if not self.hasIndex(p_int, p_int_1, parent) or \
                parent is None:
            return QModelIndex()

        # Patient
        if not parent.isValid():
            print("Create patient")
            return self._root_item.index(p_int, p_int_1, self)

        return self.parent.index(p_int, p_int_1, self)

    def hasIndex(self, p_int, p_int_1, parent=None, *args, **kwargs):
        logger.debug("hasIndex()")
        # Patient
        if not parent.isValid():
            return True

        return self._root_item.has_index(p_int)

    def data(self, q_model_index, role=None):
        logger.debug("data()")

        if role == Qt.DisplayRole:
            return q_model_index.internalPointer().name

        if role == Qt.UserRole:
            return "user"

    def parent(self, q_model_index=None):
        logger.debug("parent()")
        if self._root_item == q_model_index:
            logger.debug("q_model_index is invalid")
            return QModelIndex()

        return QModelIndex()
    #
    #     if q_model_index.internalPointer() is None:
    #         return QModelIndex()
    #
    #     print("Hello")
    #     internal = q_model_index.internalPointer()
    #     print(internal)
    #     parent_item = internal.parent()
    #
    #     print("world")
    #     if parent_item == self._root_item:
    #         return QModelIndex()
    #     print("Return")
    #     return self.createIndex(parent_item.row(), 0, parent_item)
