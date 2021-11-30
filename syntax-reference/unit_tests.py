import unittest
from thing_to_test import idChecker

class testIdChecker(unittest.TestCase):
    def test_add(self):
        self.assertEqual(idChecker(23), "you may enter")

if __name__ == '__main__':
    unittest.main()