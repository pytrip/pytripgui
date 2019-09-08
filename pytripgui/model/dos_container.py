import pytrip as pt

import logging
logger = logging.getLogger(__name__)


class DosContainer:
    def __init__(self):
        self.dos_list = []

    def import_from_file(self, dos_path):
        logger.debug("Open DosCube {:s}".format(dos_path))
        dos = pt.DosCube()

        dos.read(dos_path)

        # update model
        self.dos_list.append(dos)
        return dos
