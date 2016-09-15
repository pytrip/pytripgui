import unittest
import os

import pytripgui


class TestStart(unittest.TestCase):
    def test_check(self):
        try:
            pytripgui.start()
        except SystemExit as e:
            self.assertEqual(e.code, 2)


if __name__ == '__main__':
    unittest.main()
