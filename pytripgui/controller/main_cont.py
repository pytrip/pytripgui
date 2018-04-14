
class MainController(object):

    def __init__(self, model):
        self.model = model

    # called from view class
    def change_foobar(self, value):
        # put control logic here
        self.model.foobar = value
        self.model.announce_update()
