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
import sys
import logging
import wx

import pytrip.tripexecuter as pte

from pytripgui.util import get_class_name
from pytripgui.settings import Settings
import pytripgui.guihelper

if getattr(sys, 'frozen', False):
    from wx.lib.pubsub import setuparg1  # noqa
    from wx.lib.pubsub import pub
else:
    try:
        from wx.lib.pubsub import Publisher as pub
    except:
        from wx.lib.pubsub import setuparg1  # noqa
        from wx.lib.pubsub import pub

logger = logging.getLogger(__name__)


class FieldsCollection(list):
    pass


class ROIsCollection(list):
    pass


class LeftMenuTree(wx.TreeCtrl):
    def __init__(self, *args, **kwargs):
        super(LeftMenuTree, self).__init__(*args, **kwargs)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_leftmenu_rightclick)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.end_edit)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.begin_drag)
        self.Bind(wx.EVT_TREE_END_DRAG, self.end_drag)
        self.context_menu = {"images": [{"text": "View"}],
                             "image": [{"text": "View",
                                        "callback": self.show_image}],
                             "plans": [{"text": "New plan with ROIs",
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
                             "DoseCube": [{"text": "Delete",
                                           "callback": self.plan_remove_dose},
                                          {"text": "Set Active For Plan",
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

    def prepare_icons(self):
        """
        TODO: documentation. Possibly these are the colour boxes inside the treelist, which is
        simply an empty 16x16 px large blank box.
        """
        self.icon_size = (16, 16)
        self.image_list = wx.ImageList(self.icon_size[0], self.icon_size[1])
        self.AssignImageList(self.image_list)

    def toggle_selected_voi(self, evt):
        """ Toggles whether VOI is displayed or not. Only selected VOIs are displayed
        """
        logger.debug("toggle_selected_voi()")
        voi = self.GetItemData(self.selected_item).GetData()
        voi.selected = not voi.selected
        # add proper callback here smth like:
        pub.sendMessage("voi.selection_changed", voi)  # I am guessing here

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

    def get_parent_plan_data(self, node):
        """
        TODO: possibly this can be omitted for some more elegant solution
        to simply use data.active_plan instead ?
        """
        logger.debug("get_parent_plan_data()")
        item = node
        while True:
            data = self.GetItemData(item).GetData()
            if get_class_name(data) == "Plan":
                return data
            item = self.GetItemParent(item)
            if item is None:
                return None

    def delete_node_from_data(self, parent, data):
        """
        """
        logger.debug("delete_node_from_data()")
        child, cookie = self.GetFirstChild(parent)
        while child:
            if self.GetItemData(child).GetData() is data:
                self.Delete(child)
            child, cookie = self.GetNextChild(parent, cookie)

    def set_label_from_data(self, parent, data, text):
        """
        """
        child, cookie = self.GetFirstChild(parent)
        while child:
            if self.GetItemData(child).GetData() is data:
                self.SetItemText(child, text)
                break
            child, cookie = self.GetNextChild(parent, cookie)

    def get_child_from_data(self, parent, data):
        """
        """
        child, cookie = self.GetFirstChild(parent)
        while child:
            if self.GetItemData(child).GetData() is data:
                return child
            child, cookie = self.GetNextChild(parent, cookie)
        return None

    def search_by_data(self, root, data):
        """
        """
        data = None
        item, cookie = self.GetFirstChild(root)
        while item:
            if self.GetItemData(item).GetData() is data:
                return self.GetItemData(item).GetData()
            if self.GetChildrenCount(item) > 0:
                data = self.search_by_data(item, data)
            if data is not None:
                return data
            item, cookie = self.GetNextChild(item, cookie)
        return data

    def field_properties(self, evt):
        """
        """
        field = self.get_field_from_node()
        pub.sendMessage("gui.field.open", field)

    def dose_properties(self, evt):
        """ Callback for opening the dose properties windows
        """
        dosecube = self.GetItemData(self.selected_item).GetData()
        pub.sendMessage("gui.dose.open", dosecube)

    def plan_properties(self, evt):
        """ Callback for opening the dose properties windows
        """
        plan = self.GetItemData(self.selected_item).GetData()
        pub.sendMessage("gui.tripplan.open", plan)

    def voi_properties(self, evt):
        voi = self.GetItemData(self.selected_item).GetData()
        pub.sendMessage("gui.tripvoi.open", voi)

    def plan_field_deleted(self, msg):
        plan = msg.data["plan"]
        field = msg.data["field"]
        plan_node = self.get_child_from_data(self.plans_node, plan)
        fields_node = self.get_child_from_data(plan_node, plan.get_fields())
        self.Delete(self.get_child_from_data(fields_node, field))
        if self.GetChildrenCount(fields_node) is 0:
            self.Delete(fields_node)

    def plan_load_dose_voxelplan(self, evt):
        plan = self.GetItemData(self.selected_item).GetData()
        dlg = wx.FileDialog(
            self,
            defaultFile=self.voxelplan_path,
            wildcard="Voxelplan headerfile (*.hed)|*.hed",
            message="Choose headerfile")
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            st = Settings()
            st.save("general.import.voxelplan_path", path)
            plan.load_dose(path, "phys")

    def plan_load_let_voxelplan(self, evt):
        plan = self.GetItemData(self.selected_item).GetData()
        dlg = wx.FileDialog(
            self,
            defaultFile=self.voxelplan_path,
            wildcard="Voxelplan headerfile (*.hed)|*.hed",
            message="Choose headerfile")
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            st = Settings()
            st.save("general.import.voxelplan_path", path)
            plan.load_let(path)

    def plan_delete_field(self, evt):
        fields = self.GetItemData(self.GetItemParent(self.selected_item)).GetData()
        field = self.get_field_from_node()
        fields.remove(field)

    def get_field_from_node(self, node=None):
        if node is None:
            node = self.selected_item
        return self.GetItemData(node).GetData()

    def plan_dose_add(self, msg):
        plan = msg.data["plan"]
        dose = msg.data["dose"]
        plan_node = self.get_child_from_data(self.plans_node, plan)
        doselist = self.get_or_create_child(plan_node, "Dose", "dose")
        self.get_or_create_child(doselist, dose.get_type(), dose)

    def plan_dose_removed(self, msg):
        plan = msg.data["plan"]
        dose = msg.data["dose"]
        plan_node = self.get_child_from_data(self.plans_node, plan)
        doselist = self.get_or_create_child(plan_node, "Dose", "dose")
        dose = self.get_child_from_data(doselist, dose)
        self.Delete(dose)
        if self.GetChildrenCount(doselist) is 0:
            self.Delete(doselist)

    def plan_export_exec(self, evt):
        plan = self.GetItemData(self.selected_item).GetData()
        pub.sendMessage("gui.tripexport.open", plan)

    def plan_export_cube(self, evt):
        plan = self.GetItemData(self.selected_item).GetData()
        pub.sendMessage("gui.tripcubeexport.open", plan)

    def plan_let_add(self, msg):
        plan = msg.data["plan"]
        let = msg.data["let"]
        plan_node = self.get_child_from_data(self.plans_node, plan)
        let = self.get_or_create_child(plan_node, "LET", let)

    def plan_let_removed(self, msg):
        plan = msg.data["plan"]
        let = msg.data["let"]
        plan_node = self.get_child_from_data(self.plans_node, plan)
        let = self.get_or_create_child(plan_node, "", let)
        self.Delete(let)

    def plan_remove_let(self, evt):
        plan = self.get_parent_plan_data(self.selected_item)
        plan.remove_let(self.GetItemData(self.selected_item).GetData())

    def plan_remove_dose(self, evt):
        plan = self.get_parent_plan_data(self.selected_item)
        plan.remove_dose(self.GetItemData(self.selected_item).GetData())

    def plan_set_active_dose(self, evt):
        plan = self.get_parent_plan_data(self.selected_item)
        plan.set_active_dose(self.GetItemData(self.selected_item).GetData())

    def plan_field_added(self, msg):
        plan = msg.data["plan"]
        field = msg.data["field"]
        plan_node = self.get_child_from_data(self.plans_node, plan)
        fields = self.get_or_create_child(plan_node, "Fields", plan.get_fields())
        data = wx.TreeItemData()
        data.SetData(field)
        self.AppendItem(fields, field.get_name(), data=data)

    def plan_run_trip(self, evt):
        """
        Callback for TRiP98 Execution.
        This will set the last global parameters and then execute TRiP for the attached plan.
        """
        plan = self.GetItemData(self.selected_item).GetData()
        te = pte.Execute(self.data.ctx, self.data.vdx)

        # Load global parameters from settings file and attach them to this plan.
        st = Settings()
        te.remote = (st.load('trip98.choice.remote') == '1')  # remote if set to '1'
        te.remote_base_dir = st.load('trip98.s.wdir')
        te.servername = st.load('trip98.s.server')
        te.username = st.load('trip98.s.username')
        te.password = st.load('trip98.s.password')

        # tell what configuration files to be used, depending on the
        # projectile / rifi configuration

        # if not specified, use protons without RiFi
        if not hasattr(plan, "_projectile"):
            plan._projectile = 0
        if not hasattr(plan, "_rifi"):
            plan._rifi = 0

        _dion = ('z1', 'z2', 'z6', 'z8', 'z10')
        _drifi = ("rifi0", "rifi3")

        _suffix = '{:s}{:s}'.format(_dion[plan._projectile], _drifi[plan._rifi])

        plan.ddd_dir = st.load('trip98.ddd.{:s}'.format(_suffix))
        plan.spc_dir = st.load('trip98.spc.{:s}'.format(_suffix))
        plan.sis_path = st.load('trip98.sis.{:s}'.format(_suffix))

#        te.execute(plan, False)  # False = dry run
        te.execute(plan)  # False = dry run

    def plan_add_field(self, evt):
        plan = self.get_parent_plan_data(self.selected_item)
        field = pte.Field("")
        plan.fields.append(field)
        pub.sendMessage("plan.active.changed", plan)

    def plan_set_active(self, evt):
        plan = self.get_parent_plan_data(self.selected_item)
        self.data.active_plan = plan

    def plan_toggle_oar(self, evt):
        voi = self.GetItemData(self.selected_item).GetData()
        voi.toggle_oar()

    def plan_toggle_target(self, evt):
        voi = self.GetItemData(self.selected_item).GetData()
        voi.toggle_target()

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
        item = self.get_or_create_child(node, "ROIs", plan.get_vois())
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
            if class_name in ["TripPlan", "VoiCollection"]:
                data.add_voi(self.drag_data)
            if class_name == "TripVoi":
                item = self.GetItemData(self.GetItemParent(self.GetItemParent(evt.GetItem()))).GetData()
                if get_class_name(item) == "TripPlan":
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
        """ Setup the tree viewer in the left panel
        """
        logger.debug("enter populate_tree()")
        self.DeleteAllItems()
        self.rootnode = self.AddRoot(self.data.patient_name)
        data = wx.TreeItemData()
        data.SetData("structures")
        self.structure_node = self.AppendItem(self.rootnode, "ROIs", data=data)
        data = wx.TreeItemData()
        data.SetData("plans")
        self.plans_node = self.AppendItem(self.rootnode, "Plans", data=data)

        ### ctx = self.data.get_images().get_voxelplan()
        for voi in self.data.vdx.vois:
            data = wx.TreeItemData()
            data.SetData(voi)
            item = self.AppendItem(self.structure_node, voi.name, data=data)
            img = self.image_list.Add(pytripgui.guihelper.get_empty_bitmap(self.icon_size[0],
                                                                           self.icon_size[1],
                                                                           voi.color))
            voi.icon = img
            self.SetItemImage(item, img, wx.TreeItemIcon_Normal)

        for plan in self.data.plans:
            data = wx.TreeItemData()
            data.SetData(plan)
            p_id = self.AppendItem(self.plans_node, plan.basename, data=data)
            if plan.vois:
                item = self.get_or_create_child(p_id, "ROIs", plan.vois)
                for voi in plan.vois:
                    node = self.get_child_from_data(self.plans_node, plan)
                    item = self.get_or_create_child(node, "ROIs", plan.vois)
                    data = wx.TreeItemData()
                    data.SetData(voi)
                    i2 = self.AppendItem(item, voi.name, data=data)
                    self.SetItemImage(i2, voi.icon, wx.TreeItemIcon_Normal)
                    self.Expand(item)
                    self.Expand(self.GetItemParent(item))
            if plan.fields:
                fields = self.get_or_create_child(p_id, "Fields", FieldsCollection(plan.fields))
                for field in plan.fields:
                    data = wx.TreeItemData()
                    data.SetData(field)
                    self.AppendItem(fields, field.basename, data=data)
        self.Expand(self.rootnode)
        self.Expand(self.plans_node)

        logger.debug("exit populate_tree()")

    def new_empty_plan(self, evt):
        """ Creates a new plan without any ROIs.
        """
        logger.debug("enter new_empty_plan()")
        plan = pte.Plan()
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
        print(str(field))

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
        if data is not None and get_class_name(data.GetData()) == "TripPlan":
            return self.context_menu["TripVoi"]
        return self.context_menu["MainVoi"]

    def on_leftmenu_rightclick(self, evt):
        tree = evt.GetEventObject()
        selected_data = tree.GetItemData(evt.GetItem()).GetData()
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
