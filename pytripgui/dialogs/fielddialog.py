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
from wx.xrc import XRCCTRL, XRCID


class FieldDialog(wx.Dialog):
    def __init__(self):
        pre = wx.PreDialog()
        self.PostCreate(pre)

    def Init(self, field):
        """
        Prepares the field dialog panel.
        :params field: a pytrip.tripexecuter.field object
        """
        self.field = field
        self.btn_ok = XRCCTRL(self, 'btn_ok')
        wx.EVT_BUTTON(self, XRCID('btn_ok'), self.save_and_close)

        self.btn_cancel = XRCCTRL(self, 'btn_close')
        wx.EVT_BUTTON(self, XRCID('btn_close'), self.close)

        self.label_fieldname = XRCCTRL(self, 'label_fieldname')
        self.label_fieldname.SetLabel(field.basename)

        self.check_isocenter = XRCCTRL(self, 'check_isocenter')
        if self.field.isocenter:
            self.check_isocenter.SetValue(True)
        self.check_isocenter.Bind(wx.EVT_CHECKBOX, self.on_check_isocenter_changed)

        self.txt_targetx = XRCCTRL(self, 'txt_targetx')
        self.txt_targety = XRCCTRL(self, 'txt_targety')
        self.txt_targetz = XRCCTRL(self, 'txt_targetz')
        if self.field.isocenter:
            self.txt_targetx.SetValue("%.2f" % (self.field.isocenter[0]))
            self.txt_targety.SetValue("%.2f" % (self.field.isocenter[1]))
            self.txt_targetz.SetValue("%.2f" % (self.field.isocenter[2]))
        else:
            self.txt_targetx.Enable(False)
            self.txt_targety.Enable(False)
            self.txt_targetz.Enable(False)

        self.txt_gantry = XRCCTRL(self, 'txt_gantry')
        self.txt_gantry.SetValue("%.2f" % field.gantry)

        self.txt_couch = XRCCTRL(self, 'txt_couch')
        self.txt_couch.SetValue("%.2f" % field.couch)

        self.txt_fwhm = XRCCTRL(self, 'txt_fwhm')
        self.txt_fwhm.SetValue("%.2f" % field.fwhm)

        self.txt_zsteps = XRCCTRL(self, 'txt_zsteps')
        self.txt_zsteps.SetValue("%.2f" % field.zsteps)

        self.txt_doseextension = XRCCTRL(self, 'txt_doseext')
        self.txt_doseextension.SetValue("%.2f" % field.dose_extension)

        self.txt_contourextension = XRCCTRL(self, 'txt_contourext')
        self.txt_contourextension.SetValue("%.2f" % field.contour_extension)

        self.txt_raster1 = XRCCTRL(self, 'txt_raster1')
        self.txt_raster2 = XRCCTRL(self, 'txt_raster2')

        self.txt_raster1.SetValue("%.2f" % field.raster_step[0])
        self.txt_raster2.SetValue("%.2f" % field.raster_step[1])

        # Projectiles cannot be specified at Field level currently, since all plans are single-projectile type only.
        # Therefore projectiles are specified in the plan-dialog instead.
        # self.drop_projectile = XRCCTRL(self, 'drop_projectile')  # this is set in the plan dialog.
        # self.drop_projectile.SetSelection(self.drop_projectile.GetItems().index(field.projectile))

    def on_check_isocenter_changed(self, evt):
        """ Enable or grey-out the isocenter dialog.
        """
        if self.check_isocenter.IsChecked():
            self.txt_targetx.Enable(True)
            self.txt_targety.Enable(True)
            self.txt_targetz.Enable(True)
        else:
            self.txt_targetx.Enable(False)
            self.txt_targety.Enable(False)
            self.txt_targetz.Enable(False)

    def save_and_close(self, evt):
        """
        Invoked when Field dialog is closed.
        """
        self.field.couch = float(self.txt_couch.GetValue())
        self.field.gantry = float(self.txt_gantry.GetValue())
        self.field.fwhm = float(self.txt_fwhm.GetValue())
        if self.check_isocenter.IsChecked():
            self.field.set_isocenter_from_string(self.txt_targetx.GetValue() + ","
                                                 + self.txt_targety.GetValue() + ","
                                                 + self.txt_targetz.GetValue())
        else:
            self.field.isocenter = []
        self.field.zsteps = float(self.txt_zsteps.GetValue())

        self.field.dose_extension = float(self.txt_doseextension.GetValue())
        self.field.contour_extension = float(self.txt_contourextension.GetValue())
        self.field.raster_step = [float(self.txt_raster1.GetValue()), float(self.txt_raster2.GetValue())]
        self.field.projectile = self.drop_projectile.GetStringSelection()  # field.projectile is a string
        self.Close()

    def close(self, evt):
        self.Close()
