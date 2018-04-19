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
    def openFileNameDialog(app):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(app,
                                                  "QFileDialog.getOpenFileName()",
                                                  "", "All Files (*);;Python Files (*.py)",
                                                  options=options)
        if fileName:
            logger.debug(fileName)
            return fileName  # TODO: alternatively pass the filename as a signal to some slot?

    @staticmethod
    def openFileNamesDialog(app):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(app,
                                                "QFileDialog.getOpenFileNames()",
                                                "", "All Files (*);;Python Files (*.py)",
                                                options=options)
        if files:
            logger.debug(files)
            return files

    @staticmethod
    def saveFileDialog(app):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(app,
                                                  "QFileDialog.getSaveFileName()",
                                                  "", "All Files (*);;Text Files (*.txt)",
                                                  options=options)
        if fileName:
            logger.debug(fileName)
            return fileName
