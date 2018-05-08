import logging
import configparser

logger = logging.getLogger(__name__)


class Settings:
    """ Class for interacting with saved configurations
    """

    def __init__(self):
        """
        Prepare config parser.
        """
        import os

        self.path = os.path.join(self.get_user_directory(), "settings.dat")
        logger.debug("Setup config parser based on {:s}".format(self.path))

        self.config = configparser.ConfigParser()

    def load(self, key):
        """
        Looks up a value in the settings file.
        :params str key: string in the form of 'trip98.spc.z6.rifi3'
        :retruns: a string holding the result. If key is not found, return empty string.
        """
        self.config.read(self.path)

        # for 'trip98.spc.z6.rifi3' the first word before the dot is the section.
        _sec, _opt = key.split('.', 1)

        if not self.config.has_section(_sec):
            logger.debug("Settings: section {:s} not found, returning empty string".format(_sec))
            return ""
        if not self.config.has_option(_sec, _opt):
            logger.debug("Settings: option {:s} not found, returning empty string".format(_opt))
            return ""

        # return value is always guaranteed to be a string.
        logger.debug("_sec:{} _opt:{}")
        return self.config.get(_sec, _opt)  # this is python2 specific

    def save(self, key, value):
        """
        Save a value for key. If config section does not exist, it is created.
        :params str key:  string in the form of 'trip98.spc.z6.rifi3'
        :params str value: the value to be stored. Must be string format.
        """

        self.config.read(self.path)

        # for 'trip98.spc.z6.rifi3' key the first word before the dot is the section.
        _sec, _opt = key.split('.', 1)

        if not self.config.has_section(_sec):
            self.config.add_section(_sec)

        self.config.set(_sec, _opt, value)  # this is python2 specific

        with open(self.path, 'w') as configfile:
            self.config.write(configfile)

        text = "Updated {:s}".format(self.path)
        logger.debug(text)

    @staticmethod
    def get_user_directory():
        import os
        path = os.path.join(os.path.expanduser("~"), ".pytrip")
        if not os.path.exists(path):
            os.makedirs(path)
        return path
