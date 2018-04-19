import unittest

from pytripgui.main import main


class TestStart(unittest.TestCase):
    def test_check(self):
        try:
            main.main()
        except SystemExit as e:
            self.assertEqual(e.code, 'Unable to access the X Display, is $DISPLAY set properly?')


if __name__ == '__main__':
    unittest.main()
