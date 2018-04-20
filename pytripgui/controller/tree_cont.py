import logging

from PyQt5 import QtCore
# from PyQt5 import QtGui
from PyQt5 import QtWidgets

logger = logging.getLogger(__name__)


class TreeController(object):
    def __init__(self, model, treeview, app):
        """
        :param MyModel model:
        :param TreeView tree:
        """
        self.model = model
        self.tv = treeview
        self.app = app

        self.items = []  # test items

        self.tmodel = CustomModel(self.items)
        # self.tmodel.setHeaderData("(no CT data loaded)")

        # needed for right click to work
        self.tv.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tv.customContextMenuRequested.connect(self.openTreeMenu)

        self.tv.setModel(self.tmodel)

    def openTreeMenu(self, position):
        """ In case of right click on TreeView
        """
        logger.debug("openTreeMenu")

        indexes = self.tv.selectedIndexes()
        level = 0

        if len(indexes) > 0:
            level = 0
            index = indexes[0]

            # demonstrate how to retrieve data from index:
            _dat = self.tmodel.data(index, QtCore.Qt.DisplayRole)
            logger.debug("index data: {}".format(_dat))

            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QtWidgets.QMenu(self.app)
        editMenu = None

        if level == 0:
            editMenu = QtWidgets.QAction("Add CT Data", self.app)
            menu.addAction(editMenu)
        elif level == 1:
            editMenu = QtWidgets.QAction("Edit something else", self.app)
            menu.addAction(editMenu)
        elif level == 2:
            editMenu = QtWidgets.QAction("Edit ROI", self.app)
            menu.addAction(editMenu)

        menu.exec_(self.tv.viewport().mapToGlobal(position))

        if editMenu:
            pass  # disable callbacks for now as they are not implemented
            logger.debug("action triggered TreeView level {}".format(level))
            # editMenu.triggered.connect(partial(self.editObjFunc, index))

    def update_tree(self):
        """
        updates and populates the tree
        """
        self.tv.setModel(self.tmodel)  # TODO: something with emitDataChanged, to avoid collapsing tree each update
        pass

    def add_ctx(self, ctx):
        """ Adds a CTX item to the treeView
        """
        self.items.append(CustomNode("CTX: {}".format(ctx.basename)))
        self.tmodel = CustomModel(self.items)
        self.update_tree()

    def rm_ctx(self, ctx):
        """ TODO
        """
        pass

    def add_vdx(self, vdx):
        """ Adds a VDX item to the treeView
        """
        self.items.append(CustomNode("ROIs"))
        # TODO: add something to expand the node

        for voi in vdx.vois:
            self.items[-1].addChild(CustomNode(voi.name))

            # TODO: add colored icon or checkbox
            # pixmap = QtGui.QPixmap(12,12)
            # pixmap.fill(value)
            # icon = QtGui.QPixmap(pixmap)

        self.tmodel = CustomModel(self.items)
        self.update_tree()

    def add_dos(self, dos):
        """ Adds a DosCube item to the treeView
        """
        self.items.append(CustomNode("Dose: {}".format(dos.basename)))
        self.tmodel = CustomModel(self.items)
        self.update_tree()

    def add_let(self, let):
        """ Adds a LETCube item to the treeView
        """
        self.items.append(CustomNode("LET: {}".format(let.basename)))
        self.tmodel = CustomModel(self.items)
        self.update_tree()


class CustomNode(object):
    """
    http://doc.qt.io/qt-5/qtwidgets-itemviews-editabletreemodel-example.html
    Class dealing with nodes in a tree _model
    Based on http://trevorius.com/scrapbook/uncategorized/pyqt-custom-abstractitemmodel/
    """

    def __init__(self, in_data):
        """
        create new instance of node, with the input data "in_data"
        """

        self._data = in_data
        if type(in_data) == tuple:
            self._data = list(in_data)
        if type(in_data) == str or not hasattr(in_data, '__getitem__'):
            self._data = [in_data]

        self._children = []
        self._parent = None
        self._row = 0
        if in_data:
            # self._columncount = len(in_data)
            self._columncount = 1  # hardcoded for now
        else:
            self._columncount = 0

    def data(self, in_column):
        if in_column >= 0 and in_column < len(self._data):
            return self._data[in_column]

    def columnCount(self):
        return self._columncount

    def childCount(self):
        return len(self._children)

    def child(self, in_row):
        if in_row >= 0 and in_row < self.childCount():
            return self._children[in_row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def addChild(self, in_child):
        logger.debug("add child '{}' to CustomModel".format(in_child._data))
        in_child._parent = self
        in_child._row = len(self._children)
        self._children.append(in_child)
        # self._columncount = max(in_child.columnCount(), self._columncount)
        self._columncount = 1  # hardcoded for now


class CustomModel(QtCore.QAbstractItemModel):
    """
    Custom data model derived from QAbstractItemModel
    Based on http://trevorius.com/scrapbook/uncategorized/pyqt-custom-abstractitemmodel/
    """

    def __init__(self, in_nodes):
        """
        """
        QtCore.QAbstractItemModel.__init__(self)
        self._root = CustomNode(None)
        for node in in_nodes:
            self._root.addChild(node)

    def rowCount(self, in_index):
        if in_index.isValid():
            return in_index.internalPointer().childCount()
        return self._root.childCount()

    def addChild(self, in_node, in_parent):
        if not in_parent or not in_parent.isValid():
            parent = self._root
        else:
            parent = in_parent.internalPointer()
        parent.addChild(in_node)

    def index(self, in_row, in_column, in_parent=None):
        if not in_parent or not in_parent.isValid():
            parent = self._root
        else:
            parent = in_parent.internalPointer()

        if not QtCore.QAbstractItemModel.hasIndex(self, in_row, in_column, in_parent):
            return QtCore.QModelIndex()

        child = parent.child(in_row)
        if child:
            return QtCore.QAbstractItemModel.createIndex(self, in_row, in_column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, in_index):
        if in_index.isValid():
            p = in_index.internalPointer().parent()
            if p:
                return QtCore.QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QtCore.QModelIndex()

    def columnCount(self, in_index):
        if in_index.isValid():
            return in_index.internalPointer().columnCount()
        return self._root.childCount()

    def data(self, in_index, role):
        if not in_index.isValid():
            return None
        node = in_index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return node.data(in_index.column())
        return None

    def emitDataChanged(self):
        print("emit data changed")
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
