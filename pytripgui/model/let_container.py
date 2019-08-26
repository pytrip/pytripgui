import pytrip as pt

import logging
logger = logging.getLogger(__name__)


class LetContainer:
    def __init__(self):
        self.lets = []

    def import_let_from_file(self, let_path):
        logger.debug("Open LETCube {:s}".format(let_path))
        let = pt.LETCube()
        let.read(let_path)

        # update model
        self.lets.append(let)
        return let

    def import_let_from_list(self, let_list):
        for let in let_list:
            self.lets.append(let)

        return let_list[-1]
