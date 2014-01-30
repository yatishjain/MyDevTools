import unittest

from bst import BST

def _factory(l):
    pass
    '''
    _bst = bst(l[0])
    for item in l[1:]:
        _l.insert(item)
    return _l
    '''


class TestBST(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_sanity(self):
        # Act
        l = BST(1)

        # Assert
        self.assertEqual(1, l.item)
        self.assertEqual(None, l.next())

    def test_insert(self):
        # Arrange
        l = BST(1)

        # Act
        l.insert(2)
        l.insert(3)

        # Assert
        self.assertEqual(1, l.item)
        self.assertEqual(2, l.next().item)
        self.assertEqual(3, l.next().next().item)
        self.assertEqual(None, l.next().next().next())

    def test_insert_illegal_type_raises_ValueError(self):
        # Arrange
        l = BST(1)

        # Act + Assert
        with self.assertRaises(ValueError):
            l.insert('2')

    def test__eq__when_equal(self):
        # Arrange
        l1 = _factory([1,2,3])
        l2 = _factory([1,2,3])

        #Assert
        self.assertTrue(l1 == l2)

    def test__eq__when_not_equal(self):
        # Arrange
        l1 = _factory([1,2,3])
        l2 = _factory([1,3,2])

        #Assert
        self.assertFalse(l1 == l2)

    def test_search_contains_return_list(self):
        # Arrange
        l = _factory([1,2,3,4,5])
        expected = _factory([4,5])

        # Act
        actual = l.search(4)

        # Assert
        self.assertEqual(expected, actual)

    def test_search_not_contains_return_None(self):
        # Arrange
        l = _factory([1,2,3,4,5])

        # Act + Assert
        self.assertIsNone(l.search(6))

    def test_delete_list_item(self):
        # Arrange
        l = _factory([1,2,3,4,5])

        # Act
        BST.delete_list(l, 3)

        # Assert
        self.assertEqual(_factory([1,2,4,5]), l)

    def test_delete_list_item_that_doesnt_exist_raise_value_error(self):
        # Arrange
        l = _factory([1,2,3,4,5])

        # Act + Assert
        with self.assertRaises(ValueError):
            BST.delete_list(l, 6)

    def test_delete_item(self):
        # Arrange
        l = _factory([1,2,3,4,5])

        # Act
        l.delete_list(l, 3)

        # Assert
        self.assertEqual(_factory([1,2,4,5]), l)

    def test_delete_item_that_doesnt_exist_raise_value_error(self):
        # Arrange
        l = _factory([1,2,3,4,5])

        # Act + Assert
        with self.assertRaises(ValueError):
            l.delete_list(l, 6)

    def test__str__(self):
        # Arrange
        l = _factory([1,2,3,4,5])

        # Act + Assert
        self.assertEqual('1->2->3->4->5', str(l))

    def test__str__(self):
        # Arrange
        l = _factory([1,2,3])

        # Act + Assert
        self.assertEqual('BST(item=1, _next=BST(item=2, _next=BST(item=3, _next=None)))', l.__repr__())


if __name__ == '__main__':
    unittest.main()

