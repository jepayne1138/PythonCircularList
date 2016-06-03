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

    # def test_initialized_iter(self):
    #     pass

    def test_initialized_repr(self):
        self.assertEqual(
            repr(self.list),
            'CircList<virtual=[0, 1, 2, 3, 4], raw=[0, 1, 2, 3, 4], head=0>'
        )

    def test_head_modified_repr(self):
        self.list.head = 2
        self.assertEqual(
            repr(self.list),
            'CircList<virtual=[2, 3, 4, 0, 1], raw=[0, 1, 2, 3, 4], head=2>'
        )

class IterEqualTests(unittest.TestCase):

    def test_equal(self):
        self.assertTrue(circ_list.iter_equal(xrange(3), xrange(3)))

    def test_unequal(self):
        self.assertFalse(circ_list.iter_equal(xrange(3), xrange(4)))

    def test_iterable_nones_unequal_size(self):
        """Checks an edge case for a previous version in case I revert

        A previous idea of iter_equal used izip_longest, which filled in
        a None value if the they where not the same size. The added size check
        should take care of that case, but just in case I want to keep a test.
        """
        self.assertFalse(circ_list.iter_equal([None] * 3, [None] * 4))


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(CircListInitializationTests))
    suite.addTests(loader.loadTestsFromTestCase(CircListManipulationTests))
    suite.addTests(loader.loadTestsFromTestCase(IterEqualTests))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
