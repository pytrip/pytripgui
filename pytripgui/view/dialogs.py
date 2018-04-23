import logging

from PyQt5.QtWidgets import QFileDialog

logger = logging.getLogger(__name__)


class MyDialogs(object):
    """
    Class for holding dialogs using along with PyTRiP
    """

    def __init__(self):
        pass

    @staticmethod
    def _filter(ftype):
        """
        Internal function to generate text string for setting up default files.
        """
        if ftype == "*":
            return "AllFiles (*)"
        if ftype == "ctx":
            return "CtxCube Files (*.ctx)"
        if ftype == "hed":
            return "Header Files (*.hed)"
        if ftype == "dos":
            return "DosCube Files (*.dos)"
        if ftype == "let":
            return "LETCube Files (*.dosemlet.dos)"  # TODO use suffix from pytrip.something module.

    @staticmethod
    def openFileNameDialog(app, title="", dir="", ftype=""):
        """
        :params path str: default where to look for file
        :params type str: default suffix to look for
        """

        filters = MyDialogs._filter(ftype)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            app, title, dir, filters, options=options)
        if fileName:
            logger.debug(fileName)
            return fileName  # TODO: alternatively pass the filename as a signal to some slot?

    @staticmethod
    def openFileNamesDialog(app):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(
            app, "QFileDialog.getOpenFileNames()", "", "All Files (*);;Python Files (*.py)", options=options)
        if files:
            logger.debug(files)
            return files

    @staticmethod
    def saveFileDialog(app):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            app, "QFileDialog.getSaveFileName()", "", "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            logger.debug(fileName)
            return fileName
