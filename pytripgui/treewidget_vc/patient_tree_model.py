from PyQt5.QtCore import QVariant, QModelIndex, Qt
from PyQt5.QtCore import QAbstractItemModel
import logging

logger = logging.getLogger(__name__)


class PatientItem:
    def __init__(self, data, parent=None):
        self._data = data
        self._parent_item = parent

    def has_index(self, p_int):
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

        if self._parent_item is None:
            patient_item = PatientItem(self._data[p_int], self)
            index = obj.createIndex(p_int, p_int_1, patient_item)
            return index

        return QModelIndex()

    def parent(self):
        if self._parent_item is None:
            return QModelIndex()
        return self._parent_item

    @property
    def child_items(self):
        return self._data


class PatientTreeModel(QAbstractItemModel):
    def __init__(self, patient_list, parent=None):
        super().__init__(parent)
        self._root_item = PatientItem(patient_list)

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role == Qt.DisplayRole:
            return QVariant("Patients: ")

    def columnCount(self, parent=None, *args, **kwargs):
        logger.debug("columnCount()")
        return 1

    def rowCount(self, parent=None, *args, **kwargs):
        logger.debug("roeCount()")
        return 2

    def hasChildren(self, parent=None, *args, **kwargs):
        logger.debug("hasChildren()")
        if not parent.isValid():
            print("It hasn't got a parent, means this is root item")
            return True

        print("It has got a parent")
        return True

    def index(self, p_int, p_int_1, parent=None, *args, **kwargs):
        logger.debug("index(){}{}".format(p_int, p_int_1))

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
            return "Display"

        if role == Qt.UserRole:
            return "user"

    def parent(self, q_model_index=None):
    #     logger.debug("parent()")
    #     if not q_model_index.isValid():
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
