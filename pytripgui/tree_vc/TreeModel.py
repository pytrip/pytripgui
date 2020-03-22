import logging


from PyQt5.QtCore import QVariant, QModelIndex, Qt
from PyQt5.QtCore import QAbstractItemModel


logger = logging.getLogger(__name__)


class PatientTreeModel(QAbstractItemModel):
    def __init__(self, patient_list, parent=None):
        super().__init__(parent)
        self._root_item = patient_list

    def headerData(self, p_int, qt_orientation, role=None):
        if p_int > 0:
            return QVariant()

        if role == Qt.DisplayRole:
            return QVariant("Patients: ")

        return QVariant()

    def columnCount(self, parent=None, *args, **kwargs):
        return 1    # Only one column is supported

    def rowCount(self, parent=None, *args, **kwargs):
        logger.debug("rowCount()")
        if not parent.isValid():
            return self._root_item.row_count()
        else:
            return parent.internalPointer().row_count()

    def hasChildren(self, parent=None, *args, **kwargs):
        logger.debug("hasChildren()")
        if not parent.isValid():
            return self._root_item.has_children()

        return parent.internalPointer().has_children()

    def index(self, p_int, p_int_1, parent=None, *args, **kwargs):
        logger.debug("index() {} {}".format(p_int, p_int_1))

        if not self.hasIndex(p_int, p_int_1, parent) or \
                parent is None:
            return QModelIndex()

        # Patient
        if not parent.isValid():
            return self._root_item.index(p_int, p_int_1, self)

        return parent.internalPointer().index(p_int, p_int_1, self)

    def hasIndex(self, p_int, p_int_1, parent=None, *args, **kwargs):
        logger.debug("hasIndex()")
        # Patient
        if not parent.isValid():
            return True

        return parent.internalPointer().has_index(p_int)

    def data(self, q_model_index, role=None):
        if role == Qt.DisplayRole:
            return q_model_index.internalPointer().__repr__()

        # if role == Qt.UserRole:
        #     return "user"

    def parent(self, q_child_item=None):
        logger.debug("parent()")
        if q_child_item.isValid():
            logger.debug("q_model_index is invalid")
            return QModelIndex()

        if q_child_item.internalPointer() is None:
            return QModelIndex()

        child_item = q_child_item.internalPointer()
        parent_item = child_item.parent()

        if parent_item == self._root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def invalidate(self):
        logger.debug("Invalidate()")
        index_first = self.createIndex(0, 0)
        index_last = self.createIndex(0, self._root_item.row_count())
        self.dataChanged.emit(index_first, index_last)

# from enum import Enum
# import gc
# from pytripgui.plan_executor.patient_model import PatientModel
# from pytrip.tripexecuter.plan import Plan
# class PatientItemType(Enum):
#     ROOT = 0
#     PATIENT = 1
#     PLAN = 2
#     FIELD = 3
#     OTHER = -1
#
#
# class PatientItem:
#     def __init__(self, data, parent=None):
#         self._data = data
#         self._parent_item = parent
#         self._internal_pointer = None   # to prevent garbage collector deleting PatientItem
#
#         if parent is None:
#             self._item_type = PatientItemType.ROOT
#         elif isinstance(self._data, PatientModel):
#             self._item_type = PatientItemType.PATIENT
#         elif isinstance(self._data, Plan):
#             self._item_type = PatientItemType.PLAN
#         else:
#             self._item_type = PatientItemType.OTHER
#
#     def row_count(self):
#         return len(self._data)
#
#     def has_children(self):
#         if self._item_type == PatientItemType.ROOT:
#             return len(self._data) > 0
#         elif self._item_type == PatientItemType.PATIENT:
#             return len(self._data.plans) > 0
#         return False
#
#     def has_index(self, p_int):
#         if self._item_type == PatientItemType.ROOT:
#             return p_int < len(self._data)
#         elif self._item_type == PatientItemType.PATIENT:
#             return p_int < len(self._data.plans)
#         else:
#             return False
#
#     def row(self):
#         if self._parent_item:
#             return self._parent_item.child_items.index(self._data)
#         return 0
#
#     def index(self, p_int, p_int_1, obj):
#         gc.disable()
#
#         # if not self.has_index(p_int) or \
#         #         p_int_1 != 0:   # only one column is supported
#         #     return QModelIndex()
#         #
#         # if self._item_type == PatientItemType.ROOT:
#         #     patient_item = PatientItem(self._data[p_int], self)
#         #     patient_item._internal_pointer = patient_item
#         #     index = obj.createIndex(p_int, p_int_1, patient_item)
#         #     return index
#         #
#         # elif self._item_type == PatientItemType.PATIENT:
#         #     patient_item_1 = PatientItem(self._data.plans[p_int], self)
#         #     patient_item_1._internal_pointer = patient_item_1
#         #     index = obj.createIndex(p_int, p_int_1, patient_item_1)
#         #     return index
#
#         return QModelIndex()
#
#     def parent(self):
#         if self._item_type == PatientItemType.ROOT:
#             return QModelIndex()
#         return self._parent_item
#
#     def child_items(self):
#         return self._data
#
#     @property
#     def name(self):
#         if self._item_type == PatientItemType.ROOT:
#             return "Patient list"
#         elif self._item_type == PatientItemType.PATIENT:
#             return self._data.name
#         elif self._item_type == PatientItemType.PLAN:
#             return self._data.basename
#
#         else:
#             return "Unsupported by code"
