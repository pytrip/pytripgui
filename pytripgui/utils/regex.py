from enum import Enum

from PyQt5.QtCore import QRegularExpression


class Regex(Enum):
    STRING = QRegularExpression(r"\w+[\s\w]*")
    INT = QRegularExpression(r"-?\d*")
    INT_POSITIVE = QRegularExpression(r"\d*[1-9]\d*")
    FLOAT = QRegularExpression(r"-?((\d+([,\.]\d{0,3})?)|(\d*[,\.]\d{1,3}))")
    FLOAT_POSITIVE = QRegularExpression(r"(\d*[1-9]\d*([,\.]\d{0,3})?)|(\d*[,\.](?=\d{1,3}$)(\d*[1-9]\d*))")
    FLOAT_UNSIGNED = QRegularExpression(r"0+|((\d*[1-9]\d*([,\.]\d{0,3})?)|(\d*[,\.](?=\d{1,3}$)(\d*[1-9]\d*)))")
