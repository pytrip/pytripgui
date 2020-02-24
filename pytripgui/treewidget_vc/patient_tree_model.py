from PyQt5.QtCore import QVariant, QModelIndex, Qt
from PyQt5.QtCore import QAbstractItemModel
import logging

logger = logging.getLogger(__name__)


class PatientItem:
    def __init__(self, data, parent=None):
        self._data = data
        self._parent = parent

    def has_index(self, p_int):
        if p_int < len(self._data):
            return True
        return False

    def index(self, p_int, p_int_1, obj):
        if not self.has_index(p_int) or p_int_1 != 0:
            return QModelIndex()

        if self._parent is None:
            index = obj.createIndex(p_int, p_int_1, self._patient_list[p_int])
            print("index from adapter")
            index.data()
            return index

        return QModelIndex()


class PatientTreeModel(QAbstractItemModel):
    def __init__(self, patient_list, parent=None):
        super().__init__(parent)
        self._root_item = PatientItem(patient_list)

    def columnCount(self, parent=None, *args, **kwargs):
        print("columnCount", parent)
        return 1

    def rowCount(self, parent=None, *args, **kwargs):
        print("rowCount:", parent)
        return 5

    def hasChildren(self, parent=None, *args, **kwargs):
        if not parent.isValid():
            print("It has got a parent")
            return True

        print("It hasn't got a parent")
        return True

    def index(self, p_int, p_int_1, parent=None, *args, **kwargs):
        print("#### index ", p_int, p_int_1, parent, "####")

        if not self.hasIndex(p_int, p_int_1, parent):
            return QModelIndex()

        # Patient
        if not parent.isValid():
            print("Create patient")
            return self._patient_list.index(p_int, p_int_1, self)

    def hasIndex(self, p_int, p_int_1, parent=None, *args, **kwargs):
        print("#### HAS INDEX #####")

        # Patient
        if not parent.isValid():
            return self._patient_list.has_index(p_int)

        return True

    def data(self, q_model_index, role=None):
        print("dssgdsg sdgf sdf sdf data:")
        if not q_model_index.parent().isValid():
            return QVariant()
        if not q_model_index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            return "Display"

        if role == Qt.UserRole:
            return "user"

    def parent(self, q_model_index=None):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        if not q_model_index.isValid():
            print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
            return QModelIndex()
        print("Here")
        return q_model_index.parent()
