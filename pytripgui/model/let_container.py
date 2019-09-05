import pytrip as pt

import logging
logger = logging.getLogger(__name__)


class LetContainer:
    def __init__(self):
        self.let_list = []

    def import_from_file(self, let_path):
        logger.debug("Open LETCube {:s}".format(let_path))
        let = pt.LETCube()
        let.read(let_path)

        # update model
        self.let_list.append(let)
        return let
