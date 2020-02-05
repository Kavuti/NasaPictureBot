import unittest
from main import *


class Test(unittest.TestCase):
    def test__api_call(self):
        self.assertEqual(get_photo().status_code, 200)


if __name__ == '__main__':
    unittest.main()
