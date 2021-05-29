import logging

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)


class MyDialogs:
    """
    Class for holding dialogs using along with PyTRiP
    """
    def __init__(self):
        pass

    @staticmethod
    def show_error(text="Unspecified Error"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle("Error")
        msg.exec_()

    @staticmethod
    def _filter(ftype):
        """
        Internal function to generate text string for setting up default files.
        """
        if ftype == "*":
            return "AllFiles (*)"
        if ftype == "dicom":
            return "Dicom Files (*.dcm, *.ima)"  # TODO check if needed, and correct, probably only dirs are loaded.
        if ftype == "ctx":
            return "CtxCube Files (*.ctx)"
        if ftype == "hed":
            return "Header Files (*.hed)"
        if ftype == "dos":
            return "DosCube Files (*.dos)"
        if ftype == "let":
            return "LETCube Files (*.dosemlet.dos)"  # TODO use suffix from pytrip.something module.
        return "AllFiles (*)"

    @staticmethod
    def openDirectoryDialog(app, title="", ddir=""):
        """
        :params dir str: default where to look for file
        """

        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.DontResolveSymlinks
        options |= QFileDialog.DontUseNativeDialog

        filename = QFileDialog.getExistingDirectory(app, title, ddir, options=options)

        if filename:
            logger.debug(filename)
            return filename

        options = QFileDialog.Options()

    @staticmethod
    def openFileNameDialog(app, title="", ddir="", ftype=""):
        """
        :params path str: default where to look for file
        :params type str: default suffix to look for
        """

        filters = MyDialogs._filter(ftype)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(app, title, ddir, filters, options=options)
        if fileName:
            logger.debug(fileName)
            return fileName

    @staticmethod
    def saveFileNameDialog(app, title="", ddir="", ftype=""):
        """
        :params path str: default where to look for file
        :params type str: default suffix to look for
        """

        filters = MyDialogs._filter(ftype)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(app, title, ddir, filters, options=options)
        if fileName:
            logger.debug(fileName)
            return fileName

    @staticmethod
    def saveDirectoryDialog(app, title="", ddir=""):
        """
        :params title str: title for dialog
        :params ddir str: default dir
        """

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        ddir = QFileDialog.getExistingDirectory(app, title, ddir, options=options)
        return ddir

    @staticmethod
    def openFileNamesDialog(app):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(app,
                                                "QFileDialog.getOpenFileNames()",
                                                "",
                                                "All Files (*);;Python Files (*.py)",
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
                                                  "",
                                                  "All Files (*);;Text Files (*.txt)",
                                                  options=options)
        if fileName:
            logger.debug(fileName)
            return fileName
