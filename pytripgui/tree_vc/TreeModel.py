import logging

from PyQt5.QtCore import QVariant, QModelIndex, Qt
from PyQt5.QtCore import QAbstractItemModel

from pytripgui.tree_vc.TreeItems import PatientList

logger = logging.getLogger(__name__)


class PatientTreeModel(QAbstractItemModel):
    def __init__(self, patient_list=None, parent=None):
        super().__init__(parent)
        if patient_list:
            self._root_item = patient_list
        else:
            self._root_item = PatientList()

    def headerData(self, p_int, qt_orientation, role=None):
        if p_int > 0:
            return QVariant()

        if role == Qt.DisplayRole:
            return QVariant("Patients: ")

        return QVariant()

    def columnCount(self, parent=None, *args, **kwargs):
        return 1    # Only one column is supported

    def rowCount(self, parent=None, *args, **kwargs):
        if not parent.isValid():
            logger.debug("rowCount() for: {}".format("root"))
            return self._root_item.row_count()
        else:
            name = parent.internalPointer().__repr__()
            logger.debug("rowCount() for: {}".format(name))
            return parent.internalPointer().row_count()

    def hasChildren(self, parent=None, *args, **kwargs):
        if not parent.isValid():
            logger.debug("hasChildren() for: {}".format("root"))
            return self._root_item.has_children()
        else:
            name = parent.internalPointer().__repr__()
            has_children = parent.internalPointer().has_children()
            logger.debug("hasChildren() for: {} returns: {}".format(name, has_children))
            return has_children

    def index(self, p_int, p_int_1, parent=None, *args, **kwargs):
        logger.debug("index() {} {}".format(p_int, p_int_1))

        if not self.hasIndex(p_int, p_int_1, parent) or \
                parent is None:
            return QModelIndex()

        if not parent.isValid():
            logger.debug("index() returns: {}".format("root"))
            return self._root_item.index(p_int, p_int_1, self)
        else:
            name = parent.internalPointer().__repr__()
            logger.debug("index() returns: {}".format("root"))
            return parent.internalPointer().index(p_int, p_int_1, self)

    def hasIndex(self, p_int, p_int_1, parent=None, *args, **kwargs):
        if p_int_1 != 0:
            return False    # current implementation supports one column

        if not parent.isValid():
            logger.debug("hasIndex() for: {}:{}:{} returns: {}".format("root", p_int, p_int_1, True))
            return True
        else:
            name = parent.internalPointer().__repr__()
            has_index = parent.internalPointer().has_index(p_int)
            logger.debug("hasIndex() for: {}:{}:{} returns: {}".format(name, p_int, p_int_1, has_index))
            return has_index

    def data(self, q_model_index, role=None):
        if role == Qt.DisplayRole:
            return q_model_index.internalPointer().__repr__()

        # if role == Qt.UserRole:
        #     return "user"

    def parent(self, q_child_item=None):
        if not q_child_item.isValid():
            logger.debug("q_model_index is invalid")
            return QModelIndex()

        if q_child_item.internalPointer() is None:
            logger.error("No internal pointer")
            return QModelIndex()

        child_item = q_child_item.internalPointer()

        if child_item == self._root_item:
            logger.debug("parent() - root item has't got a parent")
            return QModelIndex()

        parent_item = child_item.parent
        return self.createIndex(parent_item.row(), 0, parent_item)

    def insertRows(self, row, count, parent=None, data=None):
        if row != 0:
            raise Exception("You can only append new element to the end")
        if count != 1:
            raise Exception("Only one row at one time")

        if not parent or not parent.isValid():
            parent = QModelIndex()
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        row_count = parent_item.row_count()
        self.beginInsertRows(parent, row_count, row_count + count - 1)
        parent_item.add_child()
        self.endInsertRows()
        return True
