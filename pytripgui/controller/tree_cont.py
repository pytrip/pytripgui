import logging

from PyQt5 import QtCore
# from PyQt5 import QtGui
from PyQt5 import QtWidgets
import pytrip as pt

logger = logging.getLogger(__name__)


class TreeController(object):
    def __init__(self, model, treeview, app, mctrl):
        """
        :param MyModel model:
        :param TreeView tree:
        """
        self.model = model
        self.tv = treeview
        self.app = app
        self.mctrl = mctrl  # refactor me
        self.items = []  # test items

        self.tmodel = CustomModel(self.items, self.model, mctrl)  # refactor me
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

        # TODO: question, any better way of handling this? Passing self.app all the way here seems strange.
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
            editMenu = QtWidgets.QAction("Calc DVH", self.app)
            menu.addAction(editMenu)

        menu.exec_(self.tv.viewport().mapToGlobal(position))

        if editMenu:
            pass  # disable callbacks for now as they are not implemented
            logger.debug("action triggered TreeView level {}".format(level))
            # TODO: this is just a test, must be made much nicer.
            self.app.ctrl.dvh.add_dvh(self.app.model.dos[-1], self.app.model.vdx.get_voi_by_name(_dat))
            # editMenu.triggered.connect(partial(self.editObjFunc, index))

    def update_tree(self):
        """
        updates and populates the tree
        """
        logger.debug("update_tree()")
        self.tv.setModel(self.tmodel)  # TODO: something with emitDataChanged, to avoid collapsing tree each update
        self.tmodel.updateModel(None)
        # self.tmodel.emitDataChanged()

    def add_ctx(self, ctx):
        """ Adds a CTX item to the treeView
        """
        # self.items.append(CustomNode("CTX: {}".format(ctx.basename)))
        self.items.append(CustomNode(ctx))
        self.tmodel = CustomModel(self.items, self.model, self.mctrl)  # TODO: brutal hack, fix me
        self.update_tree()

    def rm_ctx(self, ctx):
        """ TODO
        """
        pass

    def add_vdx(self, vdx):
        """ Adds a VDX item to the treeView
        """
        # self.items.append(CustomNode("ROIs"))
        self.items.append(CustomNode(vdx))
        # TODO: add something to expand the node

        # add all the VOIs to the tree, but use those from the model.class. We want to show all available
        # VOIs, also those which are not plotted in the canvas.
        for voi in vdx.vois:
            # self.items[-1].addChild(CustomNode(voi.name))
            self.items[-1].addChild(CustomNode(voi))

            # TODO: add colored icon or checkbox
            # pixmap = QtGui.QPixmap(12,12)
            # pixmap.fill(value)
            # icon = QtGui.QPixmap(pixmap)

        # self.tmodel = CustomModel(self.items, self.model)
        self.update_tree()

    def add_dos(self, dos):
        """ Adds a DosCube item to the treeView
        """
        # self.items.append(CustomNode("Dose: {}".format(dos.basename)))
        self.items.append(CustomNode(dos))
        self.tmodel = CustomModel(self.items, self.model, self.mctrl)  # TODO: brutal hack, fix me
        self.update_tree()

    def add_let(self, let):
        """ Adds a LETCube item to the treeView
        """
        # self.items.append(CustomNode("LET: {}".format(let.basename)))
        self.items.append(CustomNode(let))
        self.tmodel = CustomModel(self.items, self.model, self.mctrl)  # TODO: brutal hack, fix me
        self.update_tree()


class CustomNode(object):
    """
    http://doc.qt.io/qt-5/qtwidgets-itemviews-editabletreemodel-example.html
    Class dealing with nodes in a tree _model
    Based on http://trevorius.com/scrapbook/uncategorized/pyqt-custom-abstractitemmodel/
    """

    def __init__(self, data):
        """
        Create a new node instance, with the input data "data"
        """

        self._data = data  # set the data, this is of type str or a tuple of str.
        self._isChecked = False
        if type(data) == tuple:
            self._data = list(data)
        if type(data) == str or not hasattr(data, '__getitem__'):
            self._data = [data]

        self._children = []
        self._parent = None
        self._row = 0
        if data:
            # self._columncount = len(in_data)
            self._columncount = 1  # hardcoded for now
        else:
            self._columncount = 0

    def data(self, column):
        """
        Return data in column number 'column'
        :params int column: column number
        """
        if column >= 0 and column < len(self._data):
            return self._data[column]

    def isChecked(self):
        """
        Returns True if checkbox is checked for this node.
        """
        return self._isChecked

    def setChecked(self, value):
        """
        Toggle whether checkbox shall be shown checked or uncheckedself.
        :value bool: True or False.
        """
        # TODO: copy/remove data into plotmodel
        self._isChecked = value

    def columnCount(self):
        """
        Returns number of columns in this node.
        """
        return self._columncount

    def childCount(self):
        """
        Returns number of children in this node.
        """
        return len(self._children)

    def child(self, row):
        """
        Returns child in row number 'row'.
        :params int row: row number which child should be returned.
        """
        if row >= 0 and row < self.childCount():
            return self._children[row]

    def parent(self):
        """
        Returns parent node of current row.
        """
        return self._parent

    def row(self):
        """
        Returns current row.
        """
        return self._row

    def addChild(self, child):
        """
        Adds a new child to current row (making it a parent).
        """
        logger.debug("add child '{}' to CustomModel".format(child._data))
        child._parent = self
        child._isChecked = True  # new kids always added as checked by default
        child._row = len(self._children)  # last row number + 1 where new child will be inserted.
        self._children.append(child)
        # self._columncount = max(in_child.columnCount(), self._columncount)
        self._columncount = 1  # hardcoded for now


class CustomModel(QtCore.QAbstractItemModel):
    """
    Custom data model derived from QAbstractItemModel
    Based on http://trevorius.com/scrapbook/uncategorized/pyqt-custom-abstractitemmodel/
    """

    def __init__(self, nodes, model, mctrl):
        """
        Initializes model and sets the root node in self._root.
        :params list nodes: list of data. One child will be added for each item 'nodes'.
        :model MainModel: MainModel for GUI.
        :mctrl MainController: refactor me please
        """
        QtCore.QAbstractItemModel.__init__(self)
        self._root = CustomNode(None)
        for node in nodes:
            self._root.addChild(node)

        self.model = model
        self.mctrl = mctrl

    def rowCount(self, idx):
        """
        Returns number of rows at index 'idx'.
        """
        if idx.isValid():
            return idx.internalPointer().childCount()
        return self._root.childCount()

    def addChild(self, node, parent):
        """
        Adds a new 'node' to 'parent'.
        If parent is not given, then it will be added to the root node.
        """
        if not parent or not parent.isValid():
            _parent = self._root
        else:
            _parent = parent.internalPointer()
        _parent.addChild(node)

    def index(self, row, column, parent=None):
        """
        Returns model index of item at 'row' and 'column' of 'parent'. If None parent, root node is assumed.
        """
        if not parent or not parent.isValid():
            _parent = self._root
        else:
            _parent = parent.internalPointer()

        if not QtCore.QAbstractItemModel.hasIndex(self, row, column, parent):
            return QtCore.QModelIndex()

        child = _parent.child(row)  # get the child at current row.
        if child:
            return QtCore.QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, idx):
        """
        Get current parent form index 'idx'.
        """
        if idx.isValid():
            p = idx.internalPointer().parent()
            if p:
                return QtCore.QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QtCore.QModelIndex()

    def columnCount(self, idx):
        """
        Returns number of columns at current index.
        """
        if idx.isValid():
            return idx.internalPointer().columnCount()
        return self._root.childCount()

    def data(self, idx, role):
        """
        Overloading data. Some logic for what of model.plot is supposed to be shown where in the TreeView widget.
        """

        if not idx.isValid():
            return None

        # pm = self.model.plot
        # row = idx.row()
        column = idx.column()
        node = idx.internalPointer()  # returns CustomNode type

        # in case a text string is to be displayed:
        # depending on what object is in the node, show various text strings.
        if role == QtCore.Qt.DisplayRole and column == 0:
            obj = node.data(idx.column())
            if isinstance(obj, pt.CtxCube):
                return "CTX: {}".format(obj.basename)
            if isinstance(obj, pt.VdxCube):
                return "ROIs"
            if isinstance(obj, pt.Voi):
                return "{}".format(obj.name)
            if isinstance(obj, pt.DosCube):
                return "DOS: {}".format(obj.basename)
            if isinstance(obj, pt.LETCube):
                return "LET: {}".format(obj.basename)

        # in case a checkbox is to be displayed, set state based on which objects are in self.model.plot
        if role == QtCore.Qt.CheckStateRole and column == 0:
            obj = node.data(idx.column())
            checked = QtCore.QVariant(QtCore.Qt.Checked)
            unchecked = QtCore.QVariant(QtCore.Qt.Unchecked)

            # "ROIs" node should not have a checkbox at all for now.
            if isinstance(obj, pt.VdxCube):
                return None
            else:
                if node.isChecked():
                    return checked
                return unchecked

        # for future use, possibly editing names.
        if role == QtCore.Qt.EditRole:
            return node.data(idx.column())

        return None

    def flags(self, idx):
        """
        Flags for adjusting Qt.Item* behaviour.
        """
        if not idx.isValid():
            return None
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable

    def updateModel(self, idx):
        """
        This should update the TreeView widget, to reflect the current state of all.
        """
        logger.debug("updateModel() called")
        self.emitDataChanged()
        # self.dataChanged.emit(idx, idx)
        # self.layoutChanged.emit()

    def setData(self, idx, value, role):
        """
        If the user is chaning the state of the TreeView widget, i.e. by unchecking boxes, then
        the model.plot will be updated accordingly.
        After model.plot is updated, then the TreeView should be updated accordingly.
        """
        logger.debug("setData() called")
        if not idx.isValid():
            return None

        pm = self.model.plot
        row = idx.row()
        # column = idx.column()
        node = idx.internalPointer()  # returns CustomNode type
        obj = node.data(idx.column())  # data object of this node which (e.g. CtxCube, VdxCube etc..)

        if role == QtCore.Qt.CheckStateRole and idx.column() == 0:

            if node.isChecked():  # unselect something and remove it from model.plot
                node.setChecked(False)
                if isinstance(obj, pt.CtxCube):
                    logger.debug("set pm.ctx = None")
                    pm.ctx = None
                if isinstance(obj, pt.Voi):
                    logger.debug("remove Voi {}".format(obj.name))
                    if obj in pm.vois:
                        pm.vois.remove(obj)
                    else:
                        logger.warning("Tried to remove Voi {} which is not in pm.vois.")
                if isinstance(obj, pt.DosCube):
                    logger.debug("set pm.dos = None")
                    pm.dos = None
                if isinstance(obj, pt.LETCube):
                    logger.debug("set pm.let = None")
                    pm.let = None

            else:  # select something and add it to model.plot
                node.setChecked(True)
                logger.debug("row{} isChecked(True)".format(row))
                if isinstance(obj, pt.CtxCube):
                    pm.ctx = obj
                if isinstance(obj, pt.Voi):
                    pm.vois.append(obj)
                if isinstance(obj, pt.DosCube):
                    pm.dos = obj
                if isinstance(obj, pt.LETCube):
                    pm.let = obj

        self.updateModel(idx)  # TODO: this does not work? How to update the TreeView?
        self.mctrl.plot.update_viewcanvas()

        return True

    def emitDataChanged(self):
        """
        TODO: not sure if this one is needed at all.
        """
        print("emit data changed")
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
