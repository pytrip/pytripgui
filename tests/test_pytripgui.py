import unittest
import os

import pytripgui


class TestStart(unittest.TestCase):
    def test_check(self):
        pytripgui.start()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
