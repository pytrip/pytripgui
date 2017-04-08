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
import wx
import sys

if getattr(sys, 'frozen', False):
    from wx.lib.pubsub import setuparg1
    from wx.lib.pubsub import pub
else:
    try:
        from wx.lib.pubsub import Publisher as pub
    except:
        from wx.lib.pubsub import setuparg1
        from wx.lib.pubsub import pub

from wx.xrc import XmlResource, XRCCTRL, XRCID


class PlanDialog(wx.Dialog):
    def __init__(self):
        pre = wx.PreDialog()
        self.PostCreate(pre)
        pub.subscribe(self.patient_data_updated, "patient.loaded")
        pub.sendMessage("patient.request", {})

    def Init(self, plan):
        self.plan = plan

        self.btn_ok = XRCCTRL(self, 'btn_ok')
        wx.EVT_BUTTON(self, XRCID('btn_ok'), self.save_and_close)

        self.btn_cancel = XRCCTRL(self, 'btn_close')
        wx.EVT_BUTTON(self, XRCID('btn_close'), self.close)

        self.init_general()
        self.init_opt_panel()
        self.init_calculation_panel()
        self.init_advanved_dose()

    def patient_data_updated(self, msg):
        self.data = msg.data

    def init_general(self):
        self.drop_res_tissue_type = XRCCTRL(self, "drop_res_tissue_type")
        rbe_list = self.data.get_rbe()
        for rbe in rbe_list.get_rbe_list():
            self.drop_res_tissue_type.Append(rbe.get_name())
        self.select_drop_by_value(self.drop_res_tissue_type, self.plan.get_res_tissue_type())
        self.drop_target_tissue_type = XRCCTRL(self, "drop_target_tissue_type")
        for rbe in rbe_list.get_rbe_list():
            self.drop_target_tissue_type.Append(rbe.get_name())
        self.select_drop_by_value(self.drop_target_tissue_type, self.plan.get_target_tissue_type())

    def select_drop_by_value(self, drop, value):
        for i, item in enumerate(drop.GetItems()):
            if item == value:
                drop.SetSelection(i)

    def init_calculation_panel(self):
        self.check_phys_dose = XRCCTRL(self, "check_phys_dose")
        self.check_phys_dose.SetValue(self.plan.get_out_phys_dose())

        self.check_bio_dose = XRCCTRL(self, "check_bio_dose")
        self.check_bio_dose.SetValue(self.plan.get_out_bio_dose())

        self.check_dose_mean_let = XRCCTRL(self, "check_mean_let")
        self.check_dose_mean_let.SetValue(self.plan.get_out_dose_mean_let())

        self.check_field = XRCCTRL(self, "check_field")
        self.check_field.SetValue(self.plan.get_out_field())

    def init_opt_panel(self):
        self.txt_iterations = XRCCTRL(self, "txt_iterations")
        self.txt_iterations.SetValue("%d" % self.plan.get_iterations())

        self.txt_eps = XRCCTRL(self, "txt_eps")
        self.txt_eps.SetValue("%f" % self.plan.get_eps())

        self.txt_geps = XRCCTRL(self, "txt_geps")
        self.txt_geps.SetValue("%f" % self.plan.get_geps())

        self.drop_opt_method = XRCCTRL(self, "drop_opt_method")
        self.select_drop_by_value(self.drop_opt_method, self.plan.get_opt_method())

        self.drop_opt_principle = XRCCTRL(self, "drop_opt_principle")
        self.select_drop_by_value(self.drop_opt_principle, self.plan.get_opt_princip())

        self.drop_dose_alg = XRCCTRL(self, "drop_dose_alg")
        self.select_drop_by_value(self.drop_dose_alg, self.plan.get_dose_algorithm())

        self.drop_bio_alg = XRCCTRL(self, "drop_bio_alg")
        self.select_drop_by_value(self.drop_bio_alg, self.plan.get_dose_algorithm())

        self.drop_opt_alg = XRCCTRL(self, "drop_opt_alg")
        self.select_drop_by_value(self.drop_opt_alg, self.plan.get_opt_algorithm())

    def init_advanved_dose(self):
        self.drop_projectile = XRCCTRL(self, "drop_projectile")
        ##TODO: add according to name of configurations
        self.drop_projectile.Append("H")
        self.drop_projectile.Append("C")

        self.txt_dose_percent = XRCCTRL(self, "txt_dose_percent")
        wx.EVT_BUTTON(self, XRCID('btn_set_dosepercent'), self.set_dose_percent)
        wx.EVT_CHOICE(self, XRCID('drop_projectile'), self.on_projectile_changed)

    def on_projectile_changed(self, evt):
        projectile = self.drop_projectile.GetStringSelection()
        dose_percent = self.plan.get_dose_percent(projectile)
        if dose_percent is None:
            self.txt_dose_percent.SetValue("")
        else:
            self.txt_dose_percent.SetValue("%d" % dose_percent)

    def set_dose_percent(self, evt):
        if not self.drop_projectile.GetStringSelection() == "":
            self.plan.set_dose_percent(self.drop_projectile.GetStringSelection(), self.txt_dose_percent.GetValue())

    def save_and_close(self, evt):
        self.plan.set_res_tissue_type(self.drop_res_tissue_type.GetStringSelection())
        self.plan.set_target_tissue_type(self.drop_target_tissue_type.GetStringSelection())

        self.plan.set_iterations(self.txt_iterations.GetValue())
        self.plan.set_eps(self.txt_eps.GetValue())
        self.plan.set_geps(self.txt_geps.GetValue())
        self.plan.set_opt_method(self.drop_opt_method.GetStringSelection())
        self.plan.set_opt_princip(self.drop_opt_principle.GetStringSelection())
        self.plan.set_dose_algorithm(self.drop_dose_alg.GetStringSelection())
        self.plan.set_bio_algorithm(self.drop_bio_alg.GetStringSelection())
        self.plan.set_opt_algorithm(self.drop_opt_alg.GetStringSelection())

        self.plan.set_out_phys_dose(self.check_phys_dose.GetValue())
        self.plan.set_out_bio_dose(self.check_bio_dose.GetValue())
        self.plan.set_out_dose_mean_let(self.check_dose_mean_let.GetValue())
        self.plan.set_out_field(self.check_field.GetValue())

        self.Close()

    def close(self, evt):
        self.Close()
