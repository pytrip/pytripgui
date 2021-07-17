import logging

from PyQt5.QtCore import QVariant, QModelIndex, Qt
from PyQt5.QtCore import QAbstractItemModel

logger = logging.getLogger(__name__)


class TreeModel(QAbstractItemModel):
    def __init__(self, root_item):
        super().__init__(None)

        self._root_item = root_item

    def headerData(self, p_int, qt_orientation, role=None):
        if p_int > 0:
            return QVariant()

        if role == Qt.DisplayRole:
            return QVariant("Patients: ")

        return QVariant()

    def columnCount(self, parent=None, *args, **kwargs):
        return 1  # Only one column is supported

    def rowCount(self, parent=None, *args, **kwargs):
        if not parent.isValid():
            logger.debug("rowCount() for: {}".format("root"))
            return self._root_item.row_count()
        name = parent.internalPointer().__repr__()
        logger.debug("rowCount() for: {}".format(name))
        return parent.internalPointer().row_count()

    def hasChildren(self, parent=None, *args, **kwargs):
        if not parent.isValid():
            logger.debug("hasChildren() for: {}".format("root"))
            return self._root_item.has_children()
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
            return self._create_index(self._root_item, p_int, p_int_1)
        return self._create_index(parent.internalPointer(), p_int, p_int_1)

    def hasIndex(self, p_int, p_int_1, parent=None, *args, **kwargs):
        if p_int_1 != 0:
            return False  # current implementation supports one column

        if not parent.isValid():
            logger.debug("hasIndex() for: {}:{}:{} returns: {}".format("root", p_int, p_int_1, True))
            return True
        name = parent.internalPointer().__repr__()
        has_index = parent.internalPointer().has_index(p_int)
        logger.debug("hasIndex() for: {}:{}:{} returns: {}".format(name, p_int, p_int_1, has_index))
        return has_index

    def _create_index(self, parent, p_int, p_int_1):
        name = parent.__repr__()
        logger.debug("_create_index() returns: {}".format(name))

        selected_item = parent.index(p_int, p_int_1)
        if selected_item:
            return self.createIndex(p_int, p_int_1, selected_item)
        return QModelIndex()

    def delete_item(self, q_item):
        parent = q_item.parent()
        parent_item = parent.internalPointer()
        row = q_item.row()

        self.beginRemoveRows(parent, row, row)
        parent_item.delete_child(q_item.internalPointer())
        self.endRemoveRows()

    def data(self, q_model_index, role=None):
        if role == Qt.DisplayRole:
            return q_model_index.internalPointer().__repr__()

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
        if parent_item is None:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def insertRows(self, row, count, parent_item=None, child=None):
        if count != 1:
            raise Exception("Only one row at one time")

        if parent_item:
            parent = self.createIndex(parent_item.row(), 0, parent_item)
        else:
            parent_item = self._root_item
            parent = QModelIndex()

        self.beginInsertRows(parent, row, row + count - 1)
        parent_item.add_child(child)
        self.endInsertRows()

        return self.createIndex(child.row(), 0, child)
