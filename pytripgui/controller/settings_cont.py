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
        Loads the configuration file, sets attributes in model accordingly.
        If file does not exist, exit silently.
        """

        model = self.model
        pyc = self.pyc_path

        if os.path.isfile(pyc):
            with open(pyc, 'rb') as f:
                model.settings = pickle.load(f)

            # set all model attributes accordingly
            for _attr in dir(model.settings):
                _value = getattr(model.settings, _attr)
                setattr(model, _attr, _value)
        else:
            logger.info("Settings file {} not found.".format(pyc))

    def save(self, path=None):
        """
        Saves the current model configuration to the settings file.
        If path is not given, then the settings will be saved in the default config location.

        If path is given, then it will be saved at the given path, but this path is forgotten afterwards.
        This is useful for exporting the settings to different computers.
        """
        model = self.model

        if path:
            pyc = path
        else:
            pyc = self.pyc_path

        with open(pyc, 'wb') as f:
            pickle.dump(model.settings, f)

    @staticmethod
    def get_user_directory():
        """
        Returns PyTRiP user config dir. Create it, if it does not exitself.
        """
        import os
        path = os.path.join(os.path.expanduser("~"), ".pytrip")
        if not os.path.exists(path):
            os.makedirs(path)
        return path
