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
import logging

from pytripgui.settings import Settings

from wx.xrc import XRCCTRL, XRCID

logger = logging.getLogger(__name__)


class TripConfigDialog(wx.Dialog):
    def __init__(self):
        pre = wx.PreDialog()
        self.PostCreate(pre)

    def Init(self, plan):
        """ Setup the machinery for tripconfigdialog
        :params plan: tripplan
        """
        self.plan = plan

        # TODO: database for all paths. This should later be made accessible somehow on global level later.
        # TODO: 5 ions and 2 rifis hardcoded. Better would be to have a user defined list of configurations.
        nions = 5
        nrifi = 2
        self.ddd_paths = [["" for _ in range(nions)] for _ in range(nrifi)]
        self.spc_paths = [["" for _ in range(nions)] for _ in range(nrifi)]
        self.sis_paths = ["" for _ in range(nions)]  # SIS depends on ion only.

        # list of all parameters which are to be stored,
        # listed by {topic : attribute name of widget object set in .xrc file}
        self.params = {"trip98.s.wdir": "txt_working_dir",
                       "trip98.s.username": "txt_username",
                       "trip98.s.password": "txt_password",
                       "trip98.s.server": "txt_server",
                       "trip98.choice.remote": "m_choice_location",
                       "trip98.s.hlut": "txt_hlut",
                       "trip98.s.dedx": "txt_dedx",

                       # DDD
                       "trip98.ddd.z1.rifi0": "txt_ddd",
                       "trip98.ddd.z2.rifi0": "txt_ddd",
                       "trip98.ddd.z6.rifi0": "txt_ddd",
                       "trip98.ddd.z8.rifi0": "txt_ddd",
                       "trip98.ddd.z10.rifi0": "txt_ddd",

                       "trip98.ddd.z1.rifi3": "txt_ddd",
                       "trip98.ddd.z2.rifi3": "txt_ddd",
                       "trip98.ddd.z6.rifi3": "txt_ddd",
                       "trip98.ddd.z8.rifi3": "txt_ddd",
                       "trip98.ddd.z10.rifi3": "txt_ddd",

                       # SPC
                       "trip98.spc.z1.rifi0": "txt_spc",
                       "trip98.spc.z2.rifi0": "txt_spc",
                       "trip98.spc.z6.rifi0": "txt_spc",
                       "trip98.spc.z8.rifi0": "txt_spc",
                       "trip98.spc.z10.rifi0": "txt_spc",

                       "trip98.spc.z1.rifi3": "txt_spc",
                       "trip98.spc.z2.rifi3": "txt_spc",
                       "trip98.spc.z6.rifi3": "txt_spc",
                       "trip98.spc.z8.rifi3": "txt_spc",
                       "trip98.spc.z10.rifi3": "txt_spc",

                       # SIS
                       "trip98.sis.z1.rifi0": "txt_sis",
                       "trip98.sis.z2.rifi0": "txt_sis",
                       "trip98.sis.z6.rifi0": "txt_sis",
                       "trip98.sis.z8.rifi0": "txt_sis",
                       "trip98.sis.z10.rifi0": "txt_sis",

                       "trip98.sis.z1.rifi3": "txt_sis",
                       "trip98.sis.z2.rifi3": "txt_sis",
                       "trip98.sis.z6.rifi3": "txt_sis",
                       "trip98.sis.z8.rifi3": "txt_sis",
                       "trip98.sis.z10.rifi3": "txt_sis"}

        # --- Lookup widgets and attach them to this class ---------
        # Main dialog window:
        self.btn_save = XRCCTRL(self, "btn_save")
        self.btn_close = XRCCTRL(self, "btn_close")

        # selector in Access panel for remote/local operation:
        self.m_choice_location = XRCCTRL(self, "m_choice_location")

        # Kernel files panel:
        self.m_choice_ion = XRCCTRL(self, 'm_choice_ion')
        self.m_choice_rifi = XRCCTRL(self, 'm_choice_rifi')

        # loop over those which can be attached automatically (all with the "trip98.s." string in key)
        for _key in self.params:
            if "trip98.s." in _key:
                _attr = self.params[_key]  # string holding the attribute names
                setattr(self, _attr, XRCCTRL(self, _attr))  # lookup attributes names and populate with classes

        # manually add the DDD, SPC and SIS widgets to self:
        self.txt_ddd = XRCCTRL(self, 'txt_ddd')
        self.txt_spc = XRCCTRL(self, 'txt_spc')
        self.txt_sis = XRCCTRL(self, 'txt_sis')

        # --- Attach Callback functions --------
        # Main window
        wx.EVT_BUTTON(self, XRCID('btn_close'), self.close)
        wx.EVT_BUTTON(self, XRCID('btn_save'), self.save)

        # Access panel:
        wx.EVT_BUTTON(self, XRCID('btn_wdir'), self.on_browse_wdir)
        wx.EVT_CHOICE(self, XRCID('m_choice_location'), self.on_select_location)

        # Kernel panel:
        wx.EVT_CHOICE(self, XRCID('m_choice_ion'), self.on_select)
        wx.EVT_CHOICE(self, XRCID('m_choice_rifi'), self.on_select)

        wx.EVT_BUTTON(self, XRCID('btn_ddd'), self.on_browse_ddddir)
        wx.EVT_BUTTON(self, XRCID('btn_spc'), self.on_browse_spcdir)
        wx.EVT_BUTTON(self, XRCID('btn_sis'), self.on_browse_sis)

        wx.EVT_TEXT(self, XRCID('txt_ddd'), self._on_ddd_set)
        wx.EVT_TEXT(self, XRCID('txt_spc'), self._on_spc_set)
        wx.EVT_TEXT(self, XRCID('txt_sis'), self._on_sis_set)

        # LUT panel:
        wx.EVT_BUTTON(self, XRCID('btn_hlut'), self.on_browse_hlut)
        wx.EVT_BUTTON(self, XRCID('btn_dedx'), self.on_browse_dedx)

        # Read the settings file.

        st = Settings()
        for _key in self.params:
            self._store_parameter(_key, st.load(_key))

    def close(self, evt):
        """ Close the dialog.
        """
        self.Close()

    def on_select(self, evt):
        self._update_kernel_panel()

    def _update_kernel_panel(self):
        """ Update DDD, SPC and SIS entry fields according to self.*_paths
        """
        _ion = self.m_choice_ion.GetSelection()
        _rifi = self.m_choice_rifi.GetSelection()

        self.txt_ddd.SetValue(self.ddd_paths[_rifi][_ion])
        self.txt_spc.SetValue(self.spc_paths[_rifi][_ion])
        self.txt_sis.SetValue(self.sis_paths[_ion])

    def on_select_location(self, evt):
        self._update_access_panel()

    def _update_access_panel(self):
        """ Enable/disable text fiels, whether Trip is access locally or remotely.
        """
        if self.m_choice_location.GetSelection() == 0:  # local
            self.txt_server.Disable()
            self.txt_username.Disable()
            self.txt_password.Disable()
        else:
            self.txt_server.Enable()
            self.txt_username.Enable()
            self.txt_password.Enable()

    def _store_parameter(self, _topic, _val):
        """
        Callback function for the answer from SettingsManager, when a parameter was requested.
        This will store the message in appropiate widget for this dialog, however it may require some filtering.
        """

        if _val is None:
            _val = ""

        _attr = self.params[_topic]  # gets class attribute from topic

        # Handler for trivial strings: in this case, the corresponding text entries
        # must simply be updated with the _val.
        if "trip98.s." in _topic:
            if _val is None:
                _val = ""
            XRCCTRL(self, _attr).SetValue(_val)

        # wxChoice attributes need special attention, since it has a different method to update, and wants an integer,
        # not a string.
        if "trip98.choice." in _topic:
            if not _val:
                _val = "0"
            XRCCTRL(self, _attr).SetSelection(int(_val))  # all messages are stored as strings

        # Finally the text fields in the Kernel panel must be updated. This depends on what ion is selected,
        # and is updated via the internal list of paths.

        if "trip98.ddd." in _topic:
            _ion, _rifi = self._selection_id_from_topic(_topic)
            self.ddd_paths[_rifi][_ion] = _val

        if "trip98.spc." in _topic:
            _ion, _rifi = self._selection_id_from_topic(_topic)
            self.spc_paths[_rifi][_ion] = _val

        if "trip98.sis." in _topic:
            _ion, _rifi = self._selection_id_from_topic(_topic)
            self.sis_paths[_ion] = _val

        # bump all text fields in the Kernel panel based on the updated database:
        self._update_kernel_panel()

        # bump Access panel whether remote fields must be greyed or not.
        self._update_access_panel()

    def _on_ddd_set(self, evt):
        """ When the DDD text entry has been set
        """
        _ion = self.m_choice_ion.GetSelection()
        _rifi = self.m_choice_rifi.GetSelection()
        _path = self.txt_ddd.GetValue()
        self.ddd_paths[_rifi][_ion] = _path

    def _on_spc_set(self, evt):
        """ When the SPC text entry has been set
        """
        _ion = self.m_choice_ion.GetSelection()
        _rifi = self.m_choice_rifi.GetSelection()
        _path = self.txt_spc.GetValue()
        self.spc_paths[_rifi][_ion] = _path

    def _on_sis_set(self, evt):
        """ When the SIS text entry has been set
        """
        _ion = self.m_choice_ion.GetSelection()
        _path = self.txt_sis.GetValue()
        self.sis_paths[_ion] = _path

    def _selection_id_from_topic(self, _topic):
        """ Translates a topic such as "trip98.ddd.z6.rifi3" into a ion and rifi integer number for the
        wxChoice class SetChoice() method.
        """

        _dion = {"z1": 0,
                 "z2": 1,
                 "z6": 2,
                 "z8": 3,
                 "z10": 4}

        _drifi = {"rifi0": 0,
                  "rifi3": 1}

        _ion = _topic.split(".")[2]
        _rifi = _topic.split(".")[3]
        return _dion[_ion], _drifi[_rifi]

    def on_browse_wdir(self, evt):
        """ Browse working dir clicked
        """
        path = self._on_browse(self.txt_working_dir.GetValue(),
                               "Select the TRiP98 working directory",
                               True)
        self.txt_working_dir.SetValue(path)

    def on_browse_ddddir(self, evt):
        """ Browse DDD dir clicked
        """
        path = self._on_browse(self.txt_ddd.GetValue(),
                               "Select DDD directory",
                               True)
        self.txt_ddd.SetValue(path)

    def on_browse_spcdir(self, evt):
        """ Browse SPC dir clicked
        """
        path = self._on_browse(self.txt_spc.GetValue(),
                               "Select SPC directory",
                               True)
        self.txt_spc.SetValue(path)

    def on_browse_sis(self, evt):
        """ Browse SIS dir clicked
        """
        path = self._on_browse(self.txt_sis.GetValue(),
                               "Select SIS file",
                               False)
        self.txt_sis.SetValue(path)

    def on_browse_hlut(self, evt):
        """ Browse HLUT dir clicked
        """
        path = self._on_browse(self.txt_hlut.GetValue(),
                               "Select HLUT file",
                               False)
        self.txt_hlut.SetValue(path)

    def on_browse_dedx(self, evt):
        """ Browse dE/dx dir clicked
        """
        path = self._on_browse(self.txt_dedx.GetValue(),
                               "Select dE/dx file",
                               False)
        self.txt_dedx.SetValue(path)

    def _on_browse(self, defpath, message, _dir=True):
        """ Select working directory for TRiP98 via file dialog
        :params defpath: default path to open dialog in
        :params message: message to be displayed in dialog
        :params _dir: set True if directory is to be loaded. False if file.

        :returns: the dir which was selected
        """
        path = None

        if _dir:
            dlg = wx.DirDialog(
                self,
                defaultPath=defpath,
                message=message)
        else:
            dlg = wx.FileDialog(
                self,
                defaultFile=defpath,
                message=message)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            return path

        # in case no file was selected, just return the defpath, so the stuff in the text field is retained.
        if path is None:
            return defpath

    def on_browse_file(self, evt):
        """ Select working directory for TRiP98 via file dialog
        :returns: the dir which was selected
        """
        dlg = wx.FileDialog(
            self,
            defaultPath=self.txt_working_dir.GetValue(),
            message="Choose the TRiP98 working directory")

        if dlg.ShowModal() == wx.ID_OK:
            return dlg.GetPath()

    def save(self, evt):
        """ Saves the dialog settings to the preference file.
        TODO: could probably be improved later, modern GUIs has no save button for prefs.
        """
        logger.debug("save preferences...")
        _save_dict = {}

        # sensitive topics, where values should be extracted from variables instead of text_entry widgets:
        _topics = ("trip98.ddd.", "trip98.spc.", "trip98.sis.")

        # make a new dict of parameters to be saved
        for _key in self.params:
            # _val to be stored in preference files for DDD, SPC and SIS are not from text fields.
            if any(_x in _key for _x in _topics):
                # translate "trip98.ddd.z6.rifi0" to proper indices for table lookup
                _ion, _rifi = self._selection_id_from_topic(_key)

                if "trip98.ddd." in _key:
                    _val = self.ddd_paths[_rifi][_ion]
                if "trip98.spc." in _key:
                    _val = self.spc_paths[_rifi][_ion]
                if "trip98.sis." in _key:
                    _val = self.sis_paths[_ion]
            elif "trip98.s." in _key:  # all parameters which can be read directly from the txt_* widgets.
                _attr = self.params[_key]  # string holding the attribute names
                _val = XRCCTRL(self, _attr).GetValue()  # look up values in the various fields
            elif "trip98.choice." in _key:
                _attr = self.params[_key]
                _val = str(XRCCTRL(self, _attr).GetSelection())  # look up values in the various fields

            _save_dict[_key] = _val

        st = Settings()
        for _key, _value in sorted(_save_dict.items()):
            st.save(_key, _value)
