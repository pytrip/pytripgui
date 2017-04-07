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

from wx.xrc import XmlResource, XRCCTRL, XRCID

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
        self.ddd_paths = [[""] * 5] * 2
        self.spc_paths = [[""] * 5] * 2
        self.sis_paths = [""] * 5 # SIS depends on ion only.

        # list of all parameters which are to be stored, listed by topic : attribute name of widget object set in .xrc file
        self.params = {"trip98.s.wdir": "txt_working_dir",
                       "trip98.s.username": "txt_username",
                       "trip98.s.password": "txt_password",
                       "trip98.s.server": "txt_server",
                       "trip98.choice.remote": "drop_location",
                       "trip98.s.hlut": "txt_hlut",
                       "trip98.s.dedx": "txt_dedx",

                       # DDD
                       "trip98.ddd.z1.rifi0": "txt_ddd",
                       "trip98.ddd.z4.rifi0": "txt_ddd",
                       "trip98.ddd.z6.rifi0": "txt_ddd",
                       "trip98.ddd.z8.rifi0": "txt_ddd",
                       "trip98.ddd.z10.rifi0": "txt_ddd",
                       
                       "trip98.ddd.z1.rifi3": "txt_ddd",
                       "trip98.ddd.z4.rifi3": "txt_ddd",
                       "trip98.ddd.z6.rifi3": "txt_ddd",
                       "trip98.ddd.z8.rifi3": "txt_ddd",
                       "trip98.ddd.z10.rifi3": "txt_ddd",

                       # SPC
                       "trip98.spc.z1.rifi0": "txt_spc",
                       "trip98.spc.z4.rifi0": "txt_spc",
                       "trip98.spc.z6.rifi0": "txt_spc",
                       "trip98.spc.z8.rifi0": "txt_spc",
                       "trip98.spc.z10.rifi0": "txt_spc",
                       
                       "trip98.spc.z1.rifi3": "txt_spc",
                       "trip98.spc.z4.rifi3": "txt_spc",
                       "trip98.spc.z6.rifi3": "txt_spc",
                       "trip98.spc.z8.rifi3": "txt_spc",
                       "trip98.spc.z10.rifi3": "txt_spc",

                       # SIS
                       "trip98.sis.z1.rifi0": "txt_sis",
                       "trip98.sis.z4.rifi0": "txt_sis",
                       "trip98.sis.z6.rifi0": "txt_sis",
                       "trip98.sis.z8.rifi0": "txt_sis",
                       "trip98.sis.z10.rifi0": "txt_sis",
                       
                       "trip98.sis.z1.rifi3": "txt_sis",
                       "trip98.sis.z4.rifi3": "txt_sis",
                       "trip98.sis.z6.rifi3": "txt_sis",
                       "trip98.sis.z8.rifi3": "txt_sis",
                       "trip98.sis.z10.rifi3": "txt_sis"}

        # --- Lookup widgets and attach them to this class ---------
        # Main dialog window:
        self.btn_save = XRCCTRL(self, "btn_save")
        self.btn_close = XRCCTRL(self, "btn_close")

        # selector in Access panel for remote/local operation:
        self.drop_location = XRCCTRL(self, "drop_location")        

        # Kernel files panel:
        self.m_choice_ion = XRCCTRL(self, 'm_choice_ion')
        self.m_choice_rifi = XRCCTRL(self, 'm_choice_rifi')

        # loop over those which can be attached automatically (all with the "trip98.s" string in key)
        for _key in self.params:
            if "trip98.s" in _key:
                _attr = self.params[_key]  # string holding the attribute names
                setattr(self, _attr, XRCCTRL(self, _attr))  # lookup attributes names and populate with classes
                pub.subscribe(self._store_parameter, _key)
        
        # manually add the DDD, SPC and SIS widgets to self:
        self.txt_ddd = XRCCTRL(self, "txt_ddd")
        self.txt_spc = XRCCTRL(self, "txt_spc")
        self.txt_sis = XRCCTRL(self, "txt_sis")

        # --- Attach Callback functions --------
        # Main window
        wx.EVT_BUTTON(self, XRCID("btn_close"), self.close)
        wx.EVT_BUTTON(self, XRCID("btn_save"), self.save)

        # Access panel:
        wx.EVT_BUTTON(self, XRCID('btn_wdir'), self.on_browse_wdir)

        # Kenrel panel:
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

        # finally: load and set all attributes from preference file
        for _key in self.params:
            pub.sendMessage('settings.value.request', _key)


    def close(self, evt):
        """ Close the dialog.
        """
        self.Close()

    def on_select(self, evt):
        _ion = self.m_choice_ion.GetSelection()
        _rifi = self.m_choice_rifi.GetSelection()

        logger.debug("choice {:d} {:d}".format(_ion, _rifi))

        self.txt_ddd.SetValue(self.ddd_paths[_rifi][_ion])
        self.txt_spc.SetValue(self.spc_paths[_rifi][_ion])
        self.txt_sis.SetValue(self.sis_paths[_ion])

    def _store_parameter(self, msg):
        """
        Callback function for the answer from SettingsManager, when a parameter was requested.
        This will store the message in appropiate widget for this dialog, however it may require some filtering.
        """
        _topic = ".".join(msg.topic)
        _val = msg.data

        logger.debug("tripconfigdialog: recieved answer {:s} : {:s} from SettingsManager".format(_topic, _val))

        _topic_list = ("trip98.s", "trip98.ddd", "trip98.spc", "trip98.sis")
        
        if any(_x in _topic for _x in _topic_list):  # handler for trivial strings
            _attr = self.params[_topic]
            if _val is None:
                _val = ""                
            XRCCTRL(self, _attr).SetValue(_val)

        # wxChoice attributes need special attention
        if "trip98.choice." in _topic:
            _attr = self.params[_topic]
            XRCCTRL(self, _attr).SetSelection(int(_val))  # all messages are stored as strings

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
                 "z4": 1,
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
        path = self._on_browse(self.txt_working_dir.GetValue(),
                          "Select DDD directory",
                          True)
        self.txt_ddd.SetValue(path)
        #_ion = self.m_choice_ion.GetSelection()
        #_rifi = self.m_choice_rifi.GetSelection()
        #self.ddd_paths[_rifi][_ion] = path

    def on_browse_spcdir(self, evt):
        path = self._on_browse(self.txt_working_dir.GetValue(),
                          "Select SPC directory",
                          True)
        self.txt_spc.SetValue(path)
    
    def on_browse_sis(self, evt):
        path = self._on_browse(self.txt_working_dir.GetValue(),
                          "Select SIS File",
                          False)
        self.txt_sis.SetValue(path)

    def on_browse_hlut(self, evt):
        path = self._on_browse(self.txt_working_dir.GetValue(),
                          "Select HLUT File",
                          False)
        self.txt_hlut.SetValue(path)

    def on_browse_dedx(self, evt):
        path = self._on_browse(self.txt_working_dir.GetValue(),
                          "Select dE/dx File",
                          False)
        self.txt_dedx.SetValue(path)
    
    def _on_browse(self, defpath, message, _dir=True):
        """ Select working directory for TRiP98 via file dialog
        :params defpath: default path to open dialog in
        :params message: message to be displayed in dialog
        :params _dir: set True if directory is to be loaded. False if file.

        :returns: the dir which was selected
        """
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
            if path is None:
                path = ""
            return path
            
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
        _topics = ("trip98.ddd", "trip98.spc", "trip98.sis")
        
        # make a new dict of parameters to be saved
        for _key in self.params:

            # _val to be stored in preference files for DDD, SPC and SIS are not from text fields.
            if any(_x in _key for _x in _topics):
                _ion, _rifi = self._selection_id_from_topic(_key)  # translate "trip98.ddd.z6.rifi0" to proper indices for table lookup
                if "trip98.ddd." in _key:
                    _val = self.ddd_paths[_rifi][_ion]
                if "trip98.spc." in _key:
                    _val = self.spc_paths[_rifi][_ion]
                if "trip98.sis." in _key:
                    _val = self.sis_paths[_ion]
            elif "trip98.s" in _key: # all parameters which can be read directly from the txt_* widgets.
                _attr = self.params[_key]  # string holding the attribute names
                _val = XRCCTRL(self, _attr).GetValue()  # look up values in the various fields
            elif "trip98.choice." in _key:
                _attr = self.params[_key]
                _val = str(XRCCTRL(self, _attr).GetSelection())  # look up values in the various fields

            _save_dict[_key] = _val
            logger.debug("{:s} : {:s}".format(_key, _val))

        # now _save_dict is a dict holding all parameters from TripConfigDialog which should be saved to .preferences
        pub.sendMessage('settings.value.updated', _save_dict)
