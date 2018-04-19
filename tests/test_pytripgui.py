import unittest

from pytripgui.main import main as run_main


class TestStart(unittest.TestCase):
    def test_check(self):
        try:
            run_main()
        except SystemExit as e:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
