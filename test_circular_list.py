"""Need to fix these test and implement a real testrunner"""
import unittest
import circular_list as circ_list


class CircListInitializationTests(unittest.TestCase):

    def setUp(self):
        # Initialize a new empty CircList instance
        self.list = circ_list.CircList()

    def test_head_initialization(self):
        """The head attribute should be initialized to zero"""
        self.assertEqual(self.list.head, 0)


class CircListManipulationTests(unittest.TestCase):

    """Test manipulations of a CircList of 5 different integer elements"""

    def setUp(self):
        self.list = circ_list.CircList(range(5))

    def test_head_setter_below_range(self):
        self.list.head = -1
        self.assertEqual(self.list.head, 4)

    def test_head_setter_in_range(self):
        self.list.head = 3
        self.assertEqual(self.list.head, 3)

    def test_head_setter_above_range(self):
        self.list.head = 7
        self.assertEqual(self.list.head, 2)


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(CircListInitializationTests))
    suite.addTests(loader.loadTestsFromTestCase(CircListManipulationTests))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
