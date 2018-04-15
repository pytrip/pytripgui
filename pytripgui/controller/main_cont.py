import logging
import pytrip as pt

from view.dialogs import MyDialogs

logger = logging.getLogger(__name__)


class MainController(object):

    def __init__(self, model, app):
        self.model = model
        self.app = app  # not sure if this is correct. May controller use App?

    # called from view class
    def change_foobar(self, value):
        # put control logic here
        self.model.foobar = value
        self.model.announce_update()

    def open_ctx(self, model):
        """
        Opens a CTX file, and sets it to the model.
        """
        logger.debug("Open CTX")
        ctx_path = MyDialogs.openFileNameDialog(self.app)
        self.model.ctx = pt.CtxCube()
        self.model.ctx.read(ctx_path)
