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
import logging

from wx.xrc import XRCCTRL, XRCID

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


class PlanDialog(wx.Dialog):
    def __init__(self):
        pre = wx.PreDialog()
        self.PostCreate(pre)
        pub.subscribe(self.patient_data_updated, "patient.loaded")
        pub.sendMessage("patient.request", {})
        self.data = None

    def Init(self, plan):
        """
        Initialize the 'Plan properties' dialog.

        :params plan: pytrip.tripexecuter.plan object, the plan which is "active" should be sent in here.
        """
        self.plan = plan

        self.btn_ok = XRCCTRL(self, 'btn_ok')
        wx.EVT_BUTTON(self, XRCID('btn_ok'), self.save_and_close)

        self.btn_cancel = XRCCTRL(self, 'btn_close')
        wx.EVT_BUTTON(self, XRCID('btn_close'), self.close)

        self.init_general()
        self.init_opt_panel()
        self.init_calculation_panel()
        self.init_dose_delivery()

    def patient_data_updated(self, msg):
        self.data = msg.data  # msg comes from on_patient_load (main.py), its a TripData object

    def init_general(self):
        """
        Prepare the 'General' tab in the plan properties dialog.
        """
        self.drop_target_roi = XRCCTRL(self, "drop_target_roi")
        self.listbox_oars = XRCCTRL(self, "listbox_oars")
        self.checkbox_incube = XRCCTRL(self, "checkbox_incube")
        self.drop_incube = XRCCTRL(self, "drop_incube")
        self.drop_target_tissue_type = XRCCTRL(self, "drop_target_tissue_type")
        self.drop_res_tissue_type = XRCCTRL(self, "drop_res_tissue_type")

        _voi_names = []
        if self.plan.vois:
            _voi_names = [v.name for v in self.plan.vois]

        # ----------- Target ROI ------------
        # populate Target ROI wxChooser:
        if self.plan.vois:
            self.drop_target_roi.Enable(True)
            self.drop_target_roi.SetItems(_voi_names)
        else:
            self.drop_target_roi.SetItems(["(no ROIs in plan)"])
            self.drop_target_roi.Enable(False)

        # setup Chooser to point to target ROI if it exists in plan
        if self.plan.voi_target:
            # lookup index for the target ROI
            for _i, _v in enumerate(self.plan.vois):
                if _v == self.plan.voi_target:
                    self.drop_target_roi.SetSelection(_i)
        else:
            self.drop_target_roi.SetSelection(0)

        # ----------- Organs at Risk ------------
        if self.plan.vois:
            self.listbox_oars.Enable(True)
            self.listbox_oars.SetItems(_voi_names)
        else:
            self.listbox_oars.SetItems(["(no ROIs in plan)"])
            self.listbox_oars.Enable(False)

        # ----------- Incube  ------------
        # TODO: regarding incube optimization, then the idea is to allow
        # incube optimization to any dosecubes found in plan.dosecubes.
        # This means, the user must create or load a dosecube into the plan himself.

        # TODO: add incube option to Target ROI wxChooser
        # self.drop_target_roi.SetString(_incube_index, "<incube>")

        # disable incube  for now.
        # [x] should disable Target ROI
        # [ ] should enable Target ROI
        self.checkbox_incube.Enable(False)

        if self.plan.dosecubes:
            self.drop_incube.Enable(True)
            self.drop_incube.SetItems([d.basename for d in self.plan.dosecubes])
        else:
            self.drop_incube.SetItems(["(no dosecubes in plan)"])
            self.drop_incube.Enable(False)

        # if an incube_basename is found in the plan, then let wxChooser point to it
        if self.plan.incube_basename and self.plan.dosecubes:
            for _i, _d in enumerate(self.plan.dosecubes):
                if _d.basename == self.plan.basename:  # TODO: match by UUID is better
                    self.drop_incube.SetSelection(_i)

        # ----------- Target Tissue Type ------------
        # TODO: implement me
        self.drop_target_tissue_type.Enable(False)

        # ----------- Residual Tissue Type ------------
        # TODO: implement me
        self.drop_res_tissue_type.Enable(False)

    def _triptag_from_enum(self, _dict, _i):
        """
        Returns the trip-tag in the _dict for a given number _i.
        """

        for _key in _dict.keys():
            if _i == _dict[_key][0]:
                return _key
        return None

    def _select_drop_by_str(self, _chooser, _str):
        """
        Sets the wxChoice widget to the given string, if it matches the one of the possibilites.

        :params _chooser: wxChoice widget
        :params _str: the value stored in the plan class (which is a string, such as 'phys')
        """
        for i, item in enumerate(_chooser.GetItems()):
            if item == _str:
                _chooser.SetSelection(i)

    def _init_wxchoice_from_dict(self, _chooser, _dict, _show_id=True, _show_alt1=True):
        """
        Populates a wxCooser will all options from _dict, in the order as given in the dict
        Output can be adjusted with _show_id and _show_alt1 flags:

        True True : "cg : Conjugate gradients"
        True False: "cg"
        False True: "conjugate gradients"
        False False: ""

        :params _chooser: wxChoice
        :params _dict: dict as defined in the pytrip.tripexecuter.plan class
        :params _show_id: option for showing the pytrip tag
        :params _show_alt1: option for showing some description of the TRiP tag
        """

        for _key in _dict.keys():
            _i = _dict[_key][0]

            _str = ""
            if _show_id:
                _str += _key
                if _show_alt1:  # add a colon as a seperator if both are to be shown
                    _str += ": "
            if _show_alt1:
                _str += _dict[_key][1]

            _chooser.SetString(_i, "{:s}".format(_str))

    def init_calculation_panel(self):
        """
        Prepare the 'Caluculation' tab in the plan properties dialog.
        """
        self.check_phys_dose = XRCCTRL(self, "check_phys_dose")
        self.check_phys_dose.SetValue(self.plan.want_phys_dose)

        self.check_bio_dose = XRCCTRL(self, "check_bio_dose")
        self.check_bio_dose.SetValue(self.plan.want_bio_dose)

        self.check_dose_mean_let = XRCCTRL(self, "check_mean_let")
        self.check_dose_mean_let.SetValue(self.plan.want_dlet)

        self.check_field = XRCCTRL(self, "check_field")
        self.check_field.SetValue(self.plan.want_rst)

    def init_opt_panel(self):
        """
        Prepare the 'Options' tab in the plan properties dialog.
        """
        self.txt_iterations = XRCCTRL(self, "txt_iterations")
        self.txt_iterations.SetValue("%d" % self.plan.iterations)

        self.txt_eps = XRCCTRL(self, "txt_eps")
        self.txt_eps.SetValue("%f" % self.plan.eps)

        self.txt_geps = XRCCTRL(self, "txt_geps")
        self.txt_geps.SetValue("%f" % self.plan.geps)

        self.drop_opt_method = XRCCTRL(self, "drop_opt_method")
        self._init_wxchoice_from_dict(self.drop_opt_method, self.plan.opt_methods, False, True)
        self._select_drop_by_str(self.drop_opt_method, self.plan.opt_method)

        self.drop_opt_principle = XRCCTRL(self, "drop_opt_principle")
        self._init_wxchoice_from_dict(self.drop_opt_principle, self.plan.opt_principles, True, False)
        self._select_drop_by_str(self.drop_opt_principle, self.plan.opt_principle)

        self.drop_dose_alg = XRCCTRL(self, "drop_dose_alg")
        self._init_wxchoice_from_dict(self.drop_dose_alg, self.plan.dose_algs)
        self._select_drop_by_str(self.drop_dose_alg, self.plan.dose_alg)

        self.drop_bio_alg = XRCCTRL(self, "drop_bio_alg")
        self._init_wxchoice_from_dict(self.drop_bio_alg, self.plan.bio_algs)
        self._select_drop_by_str(self.drop_bio_alg, self.plan.bio_alg)

        self.drop_opt_alg = XRCCTRL(self, "drop_opt_alg")
        self._init_wxchoice_from_dict(self.drop_opt_alg, self.plan.opt_algs)
        self._select_drop_by_str(self.drop_opt_alg, self.plan.opt_alg)

    def init_dose_delivery(self):
        """
        Prepare the 'Dose delivery' tab in the plan properties dialog.
        """
        self.drop_projectile = XRCCTRL(self, "drop_projectile")
        self.drop_rifi = XRCCTRL(self, "drop_rifi")
        self.txt_dose_percent = XRCCTRL(self, "txt_dose_percent")

        wx.EVT_BUTTON(self, XRCID('btn_set_dosepercent'), self.set_dose_percent)
        wx.EVT_CHOICE(self, XRCID('drop_projectile'), self.on_projectile_changed)
        wx.EVT_CHOICE(self, XRCID('drop_rifi'), self.on_rifi_changed)

    def on_rifi_changed(self, evt):
        """ Callback function if ripple filter was changed."
        """
        # This is only minimal ripple filter implementation.
        # this must be improved, once there is proper support for it in pytrip.tripexecuter
        # https://github.com/pytrip/pytrip/issues/347
        # For now we will simply add the ripple filter (single ion plan only supported)
        # as a new internal attribute to plan.
        self.plan._rifi = self.drop_rifi.GetSelection()  # 0: no rifi, 1: 3 mm rifi
        logger.debug("RiFi set to {:d}".format(self.plan._rifi))

    def on_projectile_changed(self, evt):
        """ One dose_percent may be attached to each projectile.
        """
        # projectile string is in the form of 'Ne-20'
        # pytrip currently understands 'H' 'C' 'O' and 'Ne'
        # TODO: this needs to be handled in a much better way.
        self.plan.projectile = self.drop_projectile.GetStringSelection().split("-")[0]

        # similar strategy as in on_rifi_changed():
        # for now we will ignore multi-ion planning, and just try to get planning with
        # single ions.
        # we will store the integer number, as it will be used as an index later in leftmenu.py:plan_run_trip()
        self.plan._projectile = self.drop_projectile.GetSelection()  # store integer
        logger.debug("Projectile set to {:s}".format(self.plan._projectile))

    def set_dose_percent(self, evt):
        """ Set dose percent for a single projectile.
        """
        self.plan.target_dose_percent = float(self.txt_dose_percent.GetValue())

    def save_and_close(self, evt):
        self.plan.res_tissue_type = self.drop_res_tissue_type.GetStringSelection()
        self.plan.target_tissue_type = self.drop_target_tissue_type.GetStringSelection()

        self.plan.iterations = int(self.txt_iterations.GetValue())
        self.plan.eps = float(self.txt_eps.GetValue())
        self.plan.geps = float(self.txt_geps.GetValue())

        # "phys" or "bio"
        self.plan.opt_method = self._triptag_from_enum(self.plan.opt_methods,
                                                       self.drop_opt_method.GetSelection())

        # "H2Obased" or "CTbased"
        self.plan.opt_principle = self._triptag_from_enum(self.plan.opt_principles,
                                                          self.drop_opt_principle.GetSelection())

        # "cl", "ap", "ms"
        self.plan.dose_alg = self._triptag_from_enum(self.plan.dose_algs,
                                                     self.drop_dose_alg.GetSelection())

        # "cl", "ld"
        self.plan.bio_alg = self._triptag_from_enum(self.plan.bio_algs,
                                                    self.drop_bio_alg.GetSelection())

        # "cl", "cg", "gr", "bf", "fr"
        self.plan.opt_alg = self._triptag_from_enum(self.plan.opt_algs,
                                                    self.drop_opt_alg.GetSelection())

        self.plan.want_phys_dose = self.check_phys_dose.GetValue()
        self.plan.want_bio_dose = self.check_bio_dose.GetValue()
        self.plan.want_dlet = self.check_dose_mean_let.GetValue()
        self.plan.want_rst = self.check_field.GetValue()

        _vname = self.drop_target_roi.GetStringSelection()
        for voi in self.plan.vois:
            if voi.name == _vname:
                self.plan.voi_target = voi
                logger.debug("Set plan.target_voi name to {:s}".format(self.plan.voi_target.name))

        # TODO add selected OARs to self.plan
        # _vnames = self.listbox_oars.GetStringSelections()
        # logger.warning("OARs not implemented yet")

        self.Close()

    def close(self, evt):
        self.Close()
