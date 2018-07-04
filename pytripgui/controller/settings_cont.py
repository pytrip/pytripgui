import os
import pickle
import logging

logger = logging.getLogger(__name__)


class SettingsController:
    """
    Class for interacting with saved configurations.
    """

    def __init__(self, model):
        """
        """

        self.model = model
        # new settings handler here

        self.pyc_path = os.path.join(self.get_user_directory(), "settings.pyc")
        logger.debug("New setup config parser based on {:s}".format(self.pyc_path))

        self.load()

    def load(self):
        """
        Load confif, sets self.model accordingly.
        If file does not exist, exit silently.

        It is connected to Model, in a way that
        - upon SettingsController.load(), SettingsModel attributes starting with "_"  are not written to         Model.
        - upon SettingsController.save(),         Model attributes starting with "__" are not written to SettingsModel.

        This way,
            a) _version is written to disk, but imported into Model when loading
            b) __internal_attribute__ are not passed between Model and SettingsModel
        """

        logger.debug("SettingsController.load() : loading settings from {}".format(self.pyc_path))

        model = self.model
        pyc = self.pyc_path

        if os.path.isfile(pyc):
            with open(pyc, 'rb') as f:
                _ms = pickle.load(f)

            # set all model attributes accordingly
            for _attr in dir(_ms):
                if _attr[0] != "_":  # do not copy internal variables
                    _value = getattr(_ms, _attr)
                    setattr(model, _attr, _value)
        else:
            logger.info("Settings file {} not found.".format(pyc))

    def save(self, path=None):
        """
        Saves the current model configuration to the settings file.
        If path is not given, then the settings will be saved in the default config location.

        If path is given, then it will be saved at the given path, but this path is forgotten afterwards.
        This is useful for exporting the settings to different computers.

        It is connected to Model, in a way that
        - upon SettingsController.load(), SettingsModel attributes starting with "_"  are not written to         Model.
        - upon SettingsController.save(),         Model attributes starting with "__" are not written to SettingsModel.

        This way,
            a) _version is written to disk, but imported into Model when loading
            b) __internal_attribute__ are not passed between Model and SettingsModel
        """
        model = self.model
        _ms = self.model.settings

        if path:
            pyc = path
        else:
            pyc = self.pyc_path

        logger.debug("SettingsController.save() : saving settings to {}".format(self.pyc_path))

        # sync model.settings attributes from model
        for _attr in dir(_ms):
            if "__" not in _attr:  # do not copy internal variables
                _value = getattr(model, _attr)
                setattr(_ms, _attr, _value)

        with open(pyc, 'wb') as f:
            pickle.dump(model.settings, f)

    @staticmethod
    def get_user_directory():
        """
        Returns PyTRiP user config dir. Create it, if it does not exsist.
        """
        import os
        path = os.path.join(os.path.expanduser("~"), ".pytrip")
        if not os.path.exists(path):
            os.makedirs(path)
        return path
