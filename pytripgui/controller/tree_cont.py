import logging

from PyQt5.QtWidgets import QTreeWidgetItem
# from PyQt5 import QtCore

logger = logging.getLogger(__name__)


class TreeController(object):

    def __init__(self, model, tree):
        """
        :param MyModel model:
        :param TreeWidget tree:
        """
        self.model = model  # Q: maybe mark these private? _model, _tree
        self.tree = tree

    def update_tree(self):
        """
        updates and populates the tree
        consider QStandardItemModel or QAbstractItemModel
        """

        # TODO: clear tree.
        #
        #

        if not self.model.ctx:
            self.tree.setHeaderLabel("(no CT loaded")
        else:
            self.tree.setHeaderLabel("Patient: '{:s}'".format(self.model.ctx.patient_name))
            tree_rois = QTreeWidgetItem(self.tree)
            tree_rois.setText(0, "ROIs")
            tree_rois.setExpanded(True)  # TODO remove

            if self.model.vdx:
                for voi in self.model.vdx.vois:
                    child = QTreeWidgetItem([voi.name])
                    # set color to voi.color
                    tree_rois.addChild(child)

            tree_plans = QTreeWidgetItem(self.tree)
            tree_plans.setText(0, "Plans")
            tree_plans.setExpanded(True)  # TODO remove

            if self.model.plans:
                for i, plan in enumerate(self.model.plans):
                    child = QTreeWidgetItem("Plan {:d}".format(i))
                    tree_plans.addChild(child)

                    if plan.fields:
                        tree_fields = QTreeWidgetItem(self.plan)
                        tree_fields.setText(0, "Fields")
                        tree_fields.setExpanded(True)  # TODO remove

                    for i, field in enumerate(plan.fields):
                        child = QTreeWidgetItem("Plan {:d}".format(i))
                        tree_fields.addChild(child)

            self.tree.show()
