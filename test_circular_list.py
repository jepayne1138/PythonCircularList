"""Need to fix these test and implement a real testrunner"""
import unittest
import circular_list as circ_list


def iter_equal(iter1, iter2):
    """Checks equality of two iterables

    NO NOT PASS INFINITE GENERATORS OR IT WILL CRASH PYTHON!

    Checks if both iterables have the same length and same items
    """
    return list(iter1) == list(iter2)


class IterEqualTests(unittest.TestCase):

    def test_equal(self):
        self.assertTrue(iter_equal(xrange(3), xrange(3)))

    def test_unequal(self):
        self.assertFalse(iter_equal(xrange(3), xrange(4)))

    def test_iterable_nones_unequal_size(self):
        """Checks an edge case for a previous version in case I revert

        A previous idea of iter_equal used izip_longest, which filled in
        a None value if the they where not the same size. The added size check
        should take care of that case, but just in case I want to keep a test.
        """
        self.assertFalse(iter_equal([None] * 3, [None] * 4))


class CircListInitializationTests(unittest.TestCase):

    def test_init_no_head_keyword(self):
        circle_list = circ_list.CircList()
        self.assertIsNone(circle_list.head)

    def test_init_head_keyword_given(self):
        circle_list = circ_list.CircList(head=2)
        self.assertIsNone(circle_list.head)

    def test_init_default_head_with_initial_list(self):
        circle_list = circ_list.CircList(xrange(3))
        self.assertEqual(circle_list.head, 0)

    def test_init_given_head_with_initial_list_in_range(self):
        circle_list = circ_list.CircList(xrange(3), head=1)
        self.assertEqual(circle_list.head, 1)

    def test_init_given_head_with_initial_list_out_of_range(self):
        circle_list = circ_list.CircList(xrange(3), head=4)
        self.assertEqual(circle_list.head, 1)


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

    def test_eq_underlying_equal(self):
        EQUAL_CIRC_LIST = circ_list.CircList(range(5))
        self.assertEqual(self.list, EQUAL_CIRC_LIST)

    def test_iter_initialized(self):
        self.assertTrue(iter_equal(iter(self.list), xrange(5)))

    def test_iter_head_moved(self):
        self.list.head += 2
        CORRECT_OUTPUT = [2, 3, 4, 0, 1]
        self.assertTrue(iter_equal(iter(self.list), CORRECT_OUTPUT))

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

    def test_append_initialized(self):
        self.list.append(5)
        self.assertEqual(self.list, circ_list.CircList(range(6)))

    def test_append_head_moved(self):
        self.list.head += 2
        CORRECT_OUTPUT = circ_list.CircList([2, 3, 4, 0, 1, 5])
        self.assertTrue(self.list, CORRECT_OUTPUT)


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(CircListInitializationTests))
    suite.addTests(loader.loadTestsFromTestCase(CircListManipulationTests))
    suite.addTests(loader.loadTestsFromTestCase(IterEqualTests))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
