"""
    This file is part of pytripgui.

    pytripgui is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pytripgui is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pytripgui.  If not, see <http://www.gnu.org/licenses/>
"""
import logging
import sys

import pytrip.tripexecuter as pte

import pytripgui.guihelper
from pytripgui.model.settings import Settings
from pytripgui.util import get_class_name

import wx
if getattr(sys, 'frozen', False):
    from wx.lib.pubsub import pub
else:
    try:
        from wx.lib.pubsub import Publisher as pub
    except:
        from wx.lib.pubsub import setuparg1  # noqa
        from wx.lib.pubsub import pub

logger = logging.getLogger(__name__)


class LeftMenuTree(wx.TreeCtrl):
    """ Class for the Menu tree on the left side in GUI.
    TODO: Highly confusing stuff. Please refactor me.

    Hints for the structure:
    Several pytrip.Plan() objects can be loaded. As normally from PyTRiP:
    Each pytrip.Plan() may hold
    - a list of fields in plan.fields
    - a list of pytrip.DosCube() in plan.dosecubes
    - a list of pytrip.LETCube() in plan.letcubes

    However, only on Dose/LET cube can be displayed at a time. Therefore the Plan() object is expanded
    with the attributes:
    - plan.dos    # holding one DosCube() object
    - plan.let    # holding one LETCube() object
    - plan.field  # TODO: is this really needed? No fields are shown anyway in GUI currently.
    - plan.vois   #  this will conflict to the vois already in the plan, possibly
                  # some active attibute will be needed here.

    self.selected_item : currently selected item in TreeList
    self.plans_node : master wxTreeItemId holding all plans, there is only one of this.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize LeftMenuTree.
        Here callback functions are attached to the menu items and events emitted by the tree.
        """
        super(LeftMenuTree, self).__init__(*args, **kwargs)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_leftmenu_changed)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_leftmenu_rightclick)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_leftmenu_doubleclick)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.end_edit)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.begin_drag)
        self.Bind(wx.EVT_TREE_END_DRAG, self.end_drag)

        # build context_menu which holds the various item types.
        self.context_menu = {"images": [{"text": "View"}],
                             "CtxCube": [{"text": "View",
                                          "callback": self.show_image}],
                             "Plans": [{"text": "New plan with ROIs",
                                        "callback": self.new_plan},
                                       {"text": "New empty plan",
                                        "callback": self.new_empty_plan},
                                       {"text": "New plan from .exec",
                                        "callback": self.new_plan_from_exec}],
                             "Plan": [{"text": "Set Active",
                                           "callback": self.plan_set_active},
                                          {"text": "Add Field",
                                           "callback": self.plan_add_field},
                                          {"text": "Export",
                                           "type": "submenu",
                                           "submenu": [{"text": "Plan data",
                                                        "callback": self.plan_export_exec},
                                                       {"text": "ROI cube",
                                                        "callback": self.plan_export_cube}]},
                                          {"text": "Import",
                                           "type": "submenu",
                                           "submenu": [{"text": "Dose (.dos)",
                                                        "callback": self.plan_load_dose_voxelplan},
                                                       {"text": "LET (.dosemlet.dos)",
                                                        "callback": self.plan_load_let_voxelplan}]},
                                          {"text": "Calculate",
                                           "type": "submenu",
                                           "submenu": [{"text": "Execute TRiP",
                                                        "callback": self.plan_run_trip}]},
                                          {"text": "Edit",
                                           "callback": self.edit_label},
                                          {"text": "Delete",
                                           "callback": self.delete_plan},
                                          {"text": "Properites",
                                           "callback": self.plan_properties}],
                             "DosCube": [{"text": "Delete",
                                           "callback": self.plan_remove_dose},
                                          {"text": "Show",
                                           "callback": self.plan_set_active_dose},
                                          {"text": "Properties",
                                           "callback": self.dose_properties}],
                             "LETCube": [{"text": "Delete",
                                          "callback": self.plan_remove_let}],
                             "Voi": self.generate_voi_menu,
                             "TripVoi": [{"text": "Select",
                                          "type": "check",
                                          "value": "selected",
                                          "callback": self.toggle_selected_voi},
                                         {"text": "Target",
                                          "type": "check",
                                          "value": "is_target",
                                          "callback": self.plan_toggle_target},
                                         {"text": "OAR",
                                          "type": "check",
                                          "value": "is_oar",
                                          "callback": self.plan_toggle_oar},
                                         {"text": "Move Up",
                                          "callback":
                                          self.plan_up_voi},
                                         {"text": "Move Down",
                                          "callback":
                                          self.plan_down_voi},
                                         {"text": "Delete",
                                          "callback": self.plan_delete_voi},
                                         {"text": "Properties",
                                          "callback": self.voi_properties}],
                             "MainVoi": [{"text": "Select",
                                          "type": "check",
                                          "value": "selected",
                                          "callback": self.toggle_selected_voi},
                                         {"text": "Add To Plan",
                                          "type": "submenu",
                                          "submenu": self.plan_submenu}],
                             "FieldsCollection": [{"text": "Add Field",
                                                  "callback": self.plan_add_field}],
                             "Field": [{"text": "Delete",
                                        "callback": self.plan_delete_field},
                                       {"text": "Properties",
                                        "callback": self.field_properties}]}

        # TODO: removed vs. deleted... unify it
        # consider "dose" -> "dosecube"
        pub.subscribe(self.on_patient_load, "patient.load")
        pub.subscribe(self.voi_added, "patient.voi.added")
        pub.subscribe(self.plan_added, "plan.new")
        pub.subscribe(self.plan_renamed, "plan.renamed")
        pub.subscribe(self.plan_deleted, "plan.deleted")
        pub.subscribe(self.plan_voi_added, "plan.voi.added")
        pub.subscribe(self.plan_voi_removed, "plan.voi.remove")
        pub.subscribe(self.plan_field_added, "plan.field.added")
        pub.subscribe(self.plan_field_deleted, "plan.field.deleted")
        pub.subscribe(self.plan_dose_add, "plan.dose.added")
        pub.subscribe(self.plan_dose_removed, "plan.dose.removed")
        pub.subscribe(self.plan_let_add, "plan.let.added")
        pub.subscribe(self.plan_let_removed, "plan.let.removed")
        pub.subscribe(self.plan_voi_moved, "plan.voi.moved")

        st = Settings()
        self.voxelplan_path = st.load("general.import.voxelplan_path")
        self.dicom_path = st.load("general.import.dicom_path")
        self.prepare_icons()

    def print_tree(self, root=None):
        """
        Printing tree of associated data, just for debugging purposes

        :param root: Node to start walking the tree
        :return:
        """
        if not root:
            root = self.GetRootItem()

        data_item = self.GetItemData(root)
        if data_item is None:
            data = None
        else:
            data = data_item.GetData()
        logger.debug("Visiting node " + str(self.GetItemText(root)) + " with data: " + str(data))

        if self.GetChildrenCount(root) == 0:
            logger.debug("No more children in node " + str(self.GetItemText(root)))
        else:
            child, cookie = self.GetFirstChild(root)
            while child.IsOk():
                self.print_tree(root=child)
                child, cookie = self.GetNextChild(root, cookie)

        return

    def prepare_icons(self):
        """
        TODO: documentation. Possibly these are the colour boxes inside the treelist, which is
        simply an empty 16x16 px large blank box.
        """
        self.icon_size = (16, 16)
        self.image_list = wx.ImageList(self.icon_size[0], self.icon_size[1])
        self.AssignImageList(self.image_list)

    def toggle_selected_voi(self, evt):
        """
        Toggles whether VOI is displayed or not. Only selected VOIs are displayed
        """
        logger.debug("toggle_selected_voi()")
        voi = self.GetItemData(self.selected_item).GetData()
        voi.selected = not voi.selected
        pub.sendMessage("voi.selection_changed", voi)

    def show_image(self, evt):
        """
        """
        logger.debug("show_image()")
        a = self.GetItemData(self.selected_item).GetData()
        id = int(a.split(" ")[1])
        pub.sendMessage("2dplot.image.active_id", id)

    def plan_view_dose(self, evt):
        """
        """
        logger.debug("plan_view_dose()")
        dose = self.GetItemData(self.selected_item).GetData()
        pub.sendMessage("2dplot.dose.set", dose)

    def get_parent_plan_data(self, item):
        """
        For a given wxTreeItemId, return the Plan() object, or None if it doent exist.

        :params wxTreeItemId item: item of the tree to get.
        :returns pytrip.Plan(): for the associated item
        """
        logger.debug("get_parent_plan_data()")
        while True:
            data = self.GetItemData(item).GetData()
            if get_class_name(data) == "Plan":
                return data
            item = self.GetItemParent(item)
            if item is None:
                return None

    def delete_node_from_data(self, parent, data):
        """
        For a given data object, find the corresponding wxTreeItem and delete it from the Tree,
        and move all subsequent childs up to fill out the gap.

        :params wxTreeItemId parent: parent of the child to be deleted
        :params object data: data payhold which is assosicated to child to be deleted
        """
        logger.debug("delete_node_from_data()")
        child, cookie = self.GetFirstChild(parent)
        while child:
            if self.GetItemData(child).GetData() is data:
                self.Delete(child)
            child, cookie = self.GetNextChild(parent, cookie)

    def set_label_from_data(self, parent, data, text):
        """
        Sets the TreeItem label to text, for a given parent and data object.

        :params wxTreeItemId parent: parent item, holding the children with possible data
        :params object data: data payload associated with child TreeItem
        :params str text: string to be written to TreeItem label

        """
        child, cookie = self.GetFirstChild(parent)
        while child:
            if self.GetItemData(child).GetData() is data:
                self.SetItemText(child, text)
                break
            child, cookie = self.GetNextChild(parent, cookie)

    def get_child_from_data(self, parent, data):
        """
        Find child from a wxTreeItemId parent and a known data payload.

        :params wxTreeItemId parent: parent item, holding the children with possible data
        :params data: data payload associated with child TreeItem

        :returns: wxTreeItemId of child matching data, else None.
        """
        if parent:
            logger.debug("enter get_child_from_data(), parent = " + str(self.GetItemText(parent)))
        else:
            logger.debug("enter get_child_from_data(), parent is none")
            return None
        child, cookie = self.GetFirstChild(parent)

        while child:
            if self.GetItemData(child).GetData() is data:
                return child
            child, cookie = self.GetNextChild(parent, cookie)
        logger.debug("exit get_child_from_data()")
        return None

    def field_properties(self, evt):
        """
        Callback for opening the Field -> Properties menu
        """
        field = self.get_field_from_node()  # Field() object
        pub.sendMessage("gui.field.open", field)

    def dose_properties(self, evt):
        """
        Callback for opening the Dose -> Properties menu
        """
        dos = self.GetItemData(self.selected_item).GetData()  # DosCube() object
        pub.sendMessage("gui.dose.open", dos)

    def plan_properties(self, evt):
        """
        Callback for opening the Plan -> Properties menu
        """
        plan = self.GetItemData(self.selected_item).GetData()  # Plan() object
        pub.sendMessage("gui.tripplan.open", plan)

        # multi-ion treatment is not supported currently by TRiP
        # so all fields will be set to the ion species set in the Plan object.
        for f in plan.fields:
            f.projectile = plan.projectile
        logger.debug("plan UUID: {:s}".format(plan.__uuid__))

    def voi_properties(self, evt):
        """
        Callback function for the Voi -> Properties menu.
        """
        voi = self.GetItemData(self.selected_item).GetData()
        pub.sendMessage("gui.tripvoi.open", voi)

    def plan_field_deleted(self, msg):
        """
        Deletes a Field from the Plan tree
        """
        logger.debug("enter plan_field_deleted()")

        plan = msg.data["plan"]  # Plan() object
        field = msg.data["field"]  # Filed() object

        # Figure out the parent wxTreeItemId holding the Plan() object
        plan_node = self.get_child_from_data(self.plans_node, plan)

        node = self.get_child_from_data(self.plans_node, plan)
        child, cookie = self.GetFirstChild(node)
        fields_node = None
        while child:
            if str(self.GetItemText(child)) == "Fields":
                fields_node = child
            child, cookie = self.GetNextChild(node, cookie)

        self.Delete(self.get_child_from_data(fields_node, field))
        if self.GetChildrenCount(fields_node) is 0:
            self.Delete(fields_node)
        logger.debug("exit plan_field_deleted()")


    def plan_load_dose_voxelplan(self, evt):
        """
        Callback for loading a (.phys).dos cube
        """
        plan = self.GetItemData(self.selected_item).GetData()
        dlg = wx.FileDialog(
            self,
            defaultFile=self.voxelplan_path,
            wildcard="Voxelplan DoseCube (*.dos)|*.dos",
            message="Choose dosecube")
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            st = Settings()
            st.save("general.import.voxelplan_path", path)
            plan.load_dose(path, "phys")  # new dose cube is appended to plan.dosecubes list
        pub.sendMessage('plan.dose.added', {"plan": plan, "dose": plan.dosecubes[-1]})
        logger.debug("exit plan_load_dose_voxelplan()")

    def plan_load_let_voxelplan(self, evt):
        """
        Callback for loading a dosemlet.dos cube
        """
        plan = self.GetItemData(self.selected_item).GetData()
        dlg = wx.FileDialog(
            self,
            defaultFile=self.voxelplan_path,
            wildcard="Voxelplan LETCube (*.dosemlet.dos)|*.dosemlet.dos",
            message="Choose LETCube")
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            st = Settings()
            st.save("general.import.voxelplan_path", path)
            plan.load_let(path)
        pub.sendMessage('plan.let.added', {"plan": plan, "let": plan.letcubes[-1]})
        logger.debug("exit plan_load_let_voxelplan()")

    def plan_delete_field(self, evt):
        plan = self.get_parent_plan_data(self.selected_item)
        fields = plan.fields
        field = self.get_field_from_node()
        fields.remove(field)
        pub.sendMessage('plan.field.deleted', {"plan": plan, "field": field})

    def get_field_from_node(self, item=None):
        """
        Return the Field() object stored in the given item.
        If item is not given or None, then look into self.selected_item.

        :params wxTreeItemId item:
        :returns: Field() object stored in item.

        TODO: Throw error if object is not of Field type.
        """
        if item is None:
            item = self.selected_item
        return self.GetItemData(item).GetData()

    def plan_dose_add(self, msg):
        """
        Callback function for adding an existing DosCube() stored in the msg payload to the wxTreeCtrl.
        """
        logger.debug("enter plan_dose_add()")
        plan = msg.data["plan"]
        dos = msg.data["dose"]

        # find what wxTreeItemId belongs to the given plan
        plan_node = self.get_child_from_data(self.plans_node, plan)

        doselist = self.get_or_create_child(plan_node, "DoseList", "dose")  # "DoseList" is label, "dose" is payload
        self.get_or_create_child(doselist, dos.basename, dos)
        plan.dos = dos

        # plot the loaded dose distribution it in the plot window immediately.
        self.plan_set_active_dose(None)

        logger.debug("exit plan_dose_add()")

    def plan_dose_removed(self, msg):
        """
        Callback function for removing an existing DosCube stored in msg and wxTreeCtrl
        """
        logger.debug("enter plan_dose_removed()")
        plan = msg.data["plan"]
        dos = msg.data["dose"]

        # find what wxTreeItemId belongs to the given plan
        plan_node = self.get_child_from_data(self.plans_node, plan)

        doselist_item = self.get_or_create_child(plan_node, "DoseList", "dose")
        dos_item = self.get_child_from_data(doselist_item, dos)
        self.Delete(dos_item)
        # if all DosCube() were deleted, then remove the DoseList node as well.
        if self.GetChildrenCount(doselist_item) is 0:
            self.Delete(doselist)

    def plan_export_exec(self, evt):
        """
        """
        plan = self.GetItemData(self.selected_item).GetData()
        pub.sendMessage("gui.tripexport.open", plan)

    def plan_export_cube(self, evt):
        """
        """
        plan = self.GetItemData(self.selected_item).GetData()
        pub.sendMessage("gui.tripcubeexport.open", plan)

    def plan_let_add(self, msg):
        """
        """
        plan = msg.data["plan"]
        let = msg.data["let"]
        plan_node = self.get_child_from_data(self.plans_node, plan)
        let = self.get_or_create_child(plan_node, "LET", let)

    def plan_let_removed(self, msg):
        """
        """
        plan = msg.data["plan"]
        let = msg.data["let"]
        plan_node = self.get_child_from_data(self.plans_node, plan)
        let = self.get_or_create_child(plan_node, "", let)
        self.Delete(let)

    def plan_remove_let(self, evt):
        """
        """
        plan = self.get_parent_plan_data(self.selected_item)
        plan.letcubes.remove(self.GetItemData(self.selected_item).GetData())

    def plan_remove_dose(self, evt):
        """
        """
        plan = self.get_parent_plan_data(self.selected_item)
        plan.dosecubes.remove(self.GetItemData(self.selected_item).GetData())

    def plan_set_active_dose(self, evt):
        """
        """
        plan = self.get_parent_plan_data(self.selected_item)
        wx.CallAfter(pub.sendMessage, "plan.dose.active_changed", {"plan": plan, "dose": plan.dos})

    def plan_field_added(self, msg):
        """
        """
        logger.debug("enter plan_field_added()")
        plan = msg.data["plan"]
        field = msg.data["field"]

        # lookup parent plan item, which holds the plan with the fields from the given plan object.
        node = self.get_child_from_data(self.plans_node, plan)

        # locate proper field node
        child, cookie = self.GetFirstChild(node)
        f_node = None
        while child:
            if str(self.GetItemText(child)) == "Fields":
                f_node = child
            child, cookie = self.GetNextChild(node, cookie)

        # append new field item to the tree
        data = wx.TreeItemData()
        data.SetData(field)
        if f_node:
            self.AppendItem(f_node, field.basename, data=data)
        logger.debug("exit plan_field_added()")

    def plan_run_trip(self, evt):
        """
        Callback for TRiP98 Execution.
        This will set the last global parameters and then execute TRiP for the attached plan.
        """
        plan = self.GetItemData(self.selected_item).GetData()
        # use vdx.path which is either "" or a real path. This will force to use the
        # original .vdx file (and not a PyTRiP converted one)
        logger.debug("plan_run_trip:self.data.vdx.path = '{:s}'".format(self.data.vdx.path))
        te = pte.Execute(self.data.ctx, self.data.vdx, vdx_path = self.data.vdx.path)

        # Load global parameters from settings file and attach them to this plan.
        st = Settings()
        te.remote = (st.load('trip98.choice.remote') == '1')  # remote if set to '1'
        te.remote_base_dir = st.load('trip98.s.wdir')
        te.servername = st.load('trip98.s.server')
        te.username = st.load('trip98.s.username')
        te.password = st.load('trip98.s.password')
        te.trip_bin_path = st.load('trip98.s.bin_path')

        # tell what configuration files to be used, depending on the
        # projectile / rifi configuration

        # if not specified, use protons without RiFi
        if not hasattr(plan, "_projid"):
            plan._projid = 0
        if not hasattr(plan, "_rifi"):
            plan._rifi = 0

        # These two lines must be synchronized with self.drop_projectile in plandialog.py
        _dion = ('z1', 'z2', 'z6', 'z8', 'z10')
        _drifi = ("rifi0", "rifi3")

        _suffix = '{:s}.{:s}'.format(_dion[plan._projid], _drifi[plan._rifi])

        plan.ddd_dir = st.load('trip98.ddd.{:s}'.format(_suffix))
        plan.spc_dir = st.load('trip98.spc.{:s}'.format(_suffix))
        plan.sis_path = st.load('trip98.sis.{:s}'.format(_suffix))

        plan.make_sis(str(plan.projectile_a) + plan.projectile)

        plan.hlut_path = st.load('trip98.s.hlut')
        plan.dedx_path = st.load('trip98.s.dedx')

        # basename of plan must be in sync with CTX basename / patient_name, else TRiP wont handle it.
        plan.basename = self.data.patient_name

        logger.debug("Executing plan " + str(plan))
        logger.debug("Running executer " + str(te))

        te.execute(plan, True)  # False = dry run

        # after TRiP98 has concluded, we need to display the calculated data.
        #logger.debug("post trip cubes: {:s}".format(dir())

        # TODO: so far we assume only a single DosCube was calculated, so only a single new one is added
        # set current DosCube to most recent calculated.

        if plan.dosecubes:
            plan.dos = plan.dosecubes[-1]
            pub.sendMessage('plan.dose.added', {"plan": plan, "dose": plan.dos})

        if plan.letcubes:
            plan.let = plan.letcubes[-1]
            pub.sendMessage('plan.let.added', {"plan": plan, "let": plan.let})

    def plan_add_field(self, evt):
        logger.debug("enter plan_add_field()")
        plan = self.get_parent_plan_data(self.selected_item)

        field = pte.Field()
        field.number = max([f.number for f in plan.fields]) + 1
        field.basename = "Field {:d}".format(field.number)

        plan.fields.append(field)

        pub.sendMessage("plan.active.changed", plan)
        pub.sendMessage('plan.field.added', {"plan": plan, "field": field})
        logger.debug("exit plan_add_field()")

    def plan_set_active(self, evt):
        plan = self.get_parent_plan_data(self.selected_item)
        self.data.active_plan = plan

    def plan_toggle_oar(self, evt):
        voi = self.GetItemData(self.selected_item).GetData()
        voi.toggle_oar()

    def plan_toggle_target(self, evt):
        voi = self.GetItemData(self.selected_item).GetData()
        plan.voi_target = voi

    def plan_delete_voi(self, evt):
        vois_item = self.GetItemParent(self.selected_item)
        vois_data = self.GetItemData(vois_item).GetData()
        voi = self.GetItemData(self.selected_item).GetData()
        vois_data.delete_voi(voi)

    def plan_up_voi(self, evt):
        vois_item = self.GetItemParent(self.selected_item)
        vois_data = self.GetItemData(vois_item).GetData()
        voi = self.GetItemData(self.selected_item).GetData()
        vois_data.move_voi(voi, -1)

    def plan_down_voi(self, evt):
        vois_item = self.GetItemParent(self.selected_item)
        vois_data = self.GetItemData(vois_item).GetData()
        voi = self.GetItemData(self.selected_item).GetData()
        vois_data.move_voi(voi, 1)

    def plan_voi_removed(self, msg):
        plan = msg.data["plan"]
        voi = msg.data["voi"]
        plan_node = self.get_child_from_data(self.plans_node, plan)
        vois_node = self.get_or_create_child(plan_node, "", plan.get_vois())
        item = self.get_or_create_child(vois_node, "", voi)
        self.Delete(item)
        if self.GetChildrenCount(vois_node) is 0:
            self.Delete(vois_node)

    def plan_voi_added(self, msg):
        plan = msg.data["plan"]
        voi = msg.data["voi"]
        node = self.get_child_from_data(self.plans_node, plan)
        item = self.get_or_create_child(node, "ROIs", plan.vois)
        data = wx.TreeItemData()
        data.SetData(voi)
        i2 = self.AppendItem(item, voi.get_name(), data=data)
        self.SetItemImage(i2, voi.get_voi().get_icon(), wx.TreeItemIcon_Normal)
        self.Expand(item)
        self.Expand(self.GetItemParent(item))

    def plan_voi_moved(self, msg):
        plan = msg.data["plan"]
        voi = msg.data["voi"]
        step = msg.data["step"]
        node = self.get_child_from_data(self.plans_node, plan)
        item = self.get_or_create_child(node, "ROIs", plan.get_vois())
        child = self.get_child_from_data(item, voi)
        child2 = child
        if step < 0:
            for i in range(abs(step) + 1):
                child2 = self.GetPrevSibling(child2)
        elif step > 0:
            for i in range(abs(step)):
                child2 = self.GetNextSibling(child2)
        data = wx.TreeItemData()
        data.SetData(voi)
        item = self.InsertItem(item, child2, self.GetItemText(child), data=data)
        self.SetItemImage(item, voi.get_voi().get_icon(), wx.TreeItemIcon_Normal)
        self.Delete(child)

    def get_or_create_child(self, parent, text, data):
        """
        :params parent: <class 'wx._controls.TreeItemId'>
        :params str text: Name of this TreeItem
        :params data: payload to be associated with this TreeItem
        """
        item = self.get_child_from_data(parent, data)
        if item:
            return item
        treedata = wx.TreeItemData()
        treedata.SetData(data)
        item = self.AppendItem(parent, text, data=treedata)
        return item

    def begin_drag(self, evt):
        self.drag_data = self.GetItemData(evt.GetItem()).GetData()
        self.drag_item = evt.GetItem()
        if get_class_name(self.drag_data) in ["Voi", "TripVoi"]:
            evt.Allow()

    def end_drag(self, evt):
        data = self.GetItemData(evt.GetItem()).GetData()
        class_name = get_class_name(data)
        if get_class_name(self.drag_data) == "Voi":
            if class_name in ["Plan", "VoiCollection"]:
                data.add_voi(self.drag_data)
            if class_name == "TripVoi":
                item = self.GetItemData(self.GetItemParent(self.GetItemParent(evt.GetItem()))).GetData()
                if get_class_name(item) == "Plan":
                    item.add_voi(self.drag_data)
        elif get_class_name(self.drag_data) == "TripVoi":
            if class_name == "TripVoi":
                end = self.get_index_of(evt.GetItem())
                vois = self.GetItemData(self.GetItemParent(evt.GetItem())).GetData()
            elif class_name == "VoiCollection":
                end = 0
                vois = data
            else:
                return
            start = self.get_index_of(self.drag_item)
            step = end - start
            vois.move_voi(self.drag_data, step)

    def get_index_of(self, item):
        parent = self.GetItemParent(item)
        data = self.GetItemData(item).GetData()
        child, cookie = self.GetFirstChild(parent)
        i = 0
        n = self.GetChildrenCount(parent)
        while self.GetItemData(child).GetData() is not data and i < n:
            child, cookie = self.GetNextChild(parent, cookie)
            i += 1
        return i

    def plan_added(self, msg):
        """ updates wx.Tree with new plan
        """
        logger.debug("enter plan_added()")
        plan = msg.data
        treedata = wx.TreeItemData()  # <class 'wx._controls.TreeItemData'>
        treedata.SetData(plan)  # store the entire plan into the tree item data slot

        self.AppendItem(self.plans_node, plan.basename, data=treedata)
        self.Expand(self.plans_node)

        self.populate_tree()  ### TODO: fix this somehow better, how to update the tree properly?
        logger.debug("exit plan_added()")

    def plan_renamed(self, msg):
        self.set_label_from_data(self.plans_node, msg.data, msg.data.get_name())

    def plan_deleted(self, msg):
        self.delete_node_from_data(self.plans_node, msg.data)

    def delete_plan(self, evt):
        plan = self.GetItemData(self.selected_item).GetData()
        self.data.plans.remove(plan)

    def edit_label(self, evt):
        self.EditLabel(self.selected_item)

    def end_edit(self, evt):
        item = self.GetItemData(evt.GetItem()).GetData()
        if len(evt.GetLabel()) is 0 or not hasattr(item, "set_name") or not item.set_name(evt.GetLabel()):
            evt.Veto()

    def voi_added(self, msg):
        voi = msg.data
        data = wx.TreeItemData()
        data.SetData(voi)
        item = self.AppendItem(self.structure_node, voi.get_name(), data=data)
        img = self.image_list.Add(pytripgui.guihelper.get_empty_bitmap(self.icon_size[0],
                                                                       self.icon_size[1],
                                                                       voi.get_color()))
        voi.set_icon(img)
        self.SetItemImage(item, img, wx.TreeItemIcon_Normal)

    def on_patient_load(self, msg):
        self.data = msg.data
        self.populate_tree()

    def populate_tree(self):
        """ Clear and setup the wxTreeCtrl widget, shown in the left panel of the GUI.
        """
        logger.debug("enter populate_tree()")

        # Clear all items in the wxTreeCtrl
        self.DeleteAllItems()

        # Add the root node: this tiem only holds the Pateint
        self.rootnode = self.AddRoot(self.data.patient_name)

        # The "ROIs" TreeItem, may hold multiple "ROI" TreeItems
        data = wx.TreeItemData()
        data.SetData("structures")
        self.structure_node = self.AppendItem(self.rootnode, "ROIs", data=data)

        # The "Plans" TreeItem, may hold multiple "Plan" TreeItems
        data = wx.TreeItemData()  # TODO: Is this redundant?
        data.SetData("Plans")  # master node holds only the "Plans" string for identification for context_menu
        self.plans_node = self.AppendItem(self.rootnode, "Plans", data=data)

        # Add the VOIs loaded from .vdx or RTSTRUCT.
        for voi in self.data.vdx.vois:
            data = wx.TreeItemData()
            data.SetData(voi)
            item = self.AppendItem(self.structure_node, voi.name, data=data)
            img = self.image_list.Add(pytripgui.guihelper.get_empty_bitmap(self.icon_size[0],
                                                                           self.icon_size[1],
                                                                           voi.color))
            voi.icon = img
            self.SetItemImage(item, img, wx.TreeItemIcon_Normal)

        # add all plans into the wxTreeCtrl
        for plan in self.data.plans:
            # append tree item with plan name
            data = wx.TreeItemData()
            data.SetData(plan)
            p_id = self.AppendItem(self.plans_node, plan.basename, data=data)

            # check if this plan has VOIs, if so, add them to the Tree.
            if plan.vois:
                # figure out the parent node for the children for this plan
                node = self.get_child_from_data(self.plans_node, plan)

                # append ROIs node, holding all VOIs in the plan.
                item = self.get_or_create_child(node, "ROIs", plan.vois)

                # append each VOI item
                for voi in plan.vois:
                    data = wx.TreeItemData()  # constructor
                    data.SetData(voi)
                    i2 = self.AppendItem(item, voi.name, data=data)
                    self.SetItemImage(i2, voi.icon, wx.TreeItemIcon_Normal)
                else:
                    self.Expand(item)
                    self.Expand(self.GetItemParent(item))

            # check if plan has any Fields()
            if plan.fields:
                node = self.get_child_from_data(self.plans_node, plan)

                # append if missing Fields item
                item = self.get_or_create_child(node, "Fields", plan.fields)

                # append each Field item
                for field in plan.fields:
                    data = wx.TreeItemData()  # constructor
                    data.SetData(field)
                    self.AppendItem(item, field.basename, data=data)

        self.Expand(self.rootnode)
        self.Expand(self.plans_node)

        logger.debug("exit populate_tree()")

    def new_empty_plan(self, evt):
        """
        Creates a new plan without any ROIs.
        """
        logger.debug("enter new_empty_plan()")
        plan = pte.Plan()

        # TODO: The name of the plan should better not be the same as basename.
        # PyTRiP requires that basenames are more or less in sync,
        # however that would mean that it will be a messy tree, if the same filename is found everywhere
        # one solution could be to add a real name to each plan, which however is not used
        # as a filename or for writing the output?
        plan.basename = "New Plan {:d}".format(len(self.data.plans) + 1)

        # extend original Plan class with local attributes
        # TODO: prefix them with _? They are however not private to the class.
        plan.vois = []
        plan.dos = None
        plan.let = None

        self.data.plans.append(plan)

        pub.sendMessage("plan.new", plan)
        pub.sendMessage("plan.active.changed", plan)
        logger.debug("exit new_empty_plan()")

    def new_plan(self, evt):
        """ Adds a new plan with all ROIs from the current patient, and a single default Field
        """
        logger.debug("enter new_plan()")
        plan = pte.Plan()
        plan.basename = "New Plan {:d}".format(len(self.data.plans) + 1)
        field = pte.Field()
        field.basename = "Field {:d}".format(len(plan.fields) + 1)
        plan.fields.append(field)

        # extend original Plan class with local attributes
        # TODO: prefix them with _? They are however not private to the class.
        plan.vois = []
        plan.dos = None
        plan.let = None
        for voi in self.data.vdx.vois:
            voi.target = False  # add new attribute
            plan.vois.append(voi)

        self.data.plans.append(plan)

        pub.sendMessage("plan.new", plan)
        pub.sendMessage("plan.active.changed", plan)  # update the plot
        logger.debug("exit new_plan()")

    def new_plan_from_exec(self, evt):
        """ Opens the import dialog and sets up a plan.
        """
        logger.debug("enter new_plan_from_exec()")
        #TODO: implement me

    def generate_voi_menu(self, node):
        data = self.GetItemData(self.GetItemParent(self.GetItemParent(node)))
        if data is not None and get_class_name(data.GetData()) == "Plan":
            return self.context_menu["TripVoi"]
        return self.context_menu["MainVoi"]

    def on_leftmenu_changed(self, evt):
        """
        Callback function if item is selected in wxTreeCtrl.
        """
        logger.debug("Left-click in tree")

    def on_leftmenu_doubleclick(self, evt):
        """
        Callback function if item is double clicked upon - could be used for renaming
        """
        logger.debug("doubleclick in tree")

    def on_leftmenu_rightclick(self, evt):
        """
        Callback function if item is rightclicked upon in wxTreeCtrl.
        """
        tree = evt.GetEventObject()
        data = tree.GetItemData(evt.GetItem())

        # TODO: this is messy, should be improved.
        if data:
            selected_data = data.GetData()
        else:
            selected_data = data
        if type(selected_data) is str:
            menu_name = selected_data.split(" ")[0]
        else:
            menu_name = get_class_name(selected_data)

        if menu_name in self.context_menu:
            self.selected_item = evt.GetItem()
            menu_points = self.context_menu[menu_name]
            if type(menu_points) is not list:
                menu_points = menu_points(self.selected_item)

            menu = self.build_menu(menu_points, selected_data)
            self.PopupMenu(menu, evt.GetPoint())
            menu.Destroy()

    def build_menu(self, menu_points, selected_data):
        menu = wx.Menu()
        for menu_item in menu_points:
            id = wx.NewId()
            if "require" in menu_item:
                if getattr(selected_data, menu_item["require"])() is None:
                    continue
            if "type" not in menu_item:
                item = wx.MenuItem(menu, id, menu_item["text"])
                menu.AppendItem(item)
            elif menu_item["type"] == "check":
                item = menu.AppendCheckItem(id, menu_item["text"])
                if getattr(selected_data, menu_item["value"]) is True:
                    item.Check()
            elif menu_item["type"] == "submenu":
                if type(menu_item["submenu"]) is list:
                    item = self.build_menu(menu_item["submenu"], selected_data)
                else:
                    item = menu_item["submenu"]()
                item = menu.AppendSubMenu(item, menu_item["text"])
            if "callback" in menu_item:
                wx.EVT_MENU(self, id, menu_item["callback"])
        return menu

    def plan_add_voi(self, evt):
        name = evt.GetEventObject().GetLabel(evt.GetId())
        list_of_matching_plans = [plan for plan in self.data.plans if plan.basename == name]
        if not list_of_matching_plans:
            raise Exception("No plan found for name " + name)
        if len(list_of_matching_plans) > 1:
            raise Exception("More than one plan found for name " + name)
        plan = list_of_matching_plans[0]
        voi = self.GetItemData(self.selected_item).GetData()
        plan.vois.append(voi)

    def plan_submenu(self):
        submenu = wx.Menu()
        for plan in self.data.plans:
            id = wx.NewId()
            item = wx.MenuItem(submenu, id, plan.basename)
            submenu.AppendItem(item)
            wx.EVT_MENU(submenu, id, self.plan_add_voi)
        return submenu
