"""
Functions of universal character.
"""
import logging

logger = logging.getLogger(__name__)


def main_dir():
    """
    Returns base dir of pytrip.
    """
    import os
    import sys
    if getattr(sys, 'frozen', False):
        return os.environ.get("_MEIPASS2", os.path.abspath("."))
        # when using single directory installer, this one should be probably used:
        # return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)
