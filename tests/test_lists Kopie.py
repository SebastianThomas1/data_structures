# Sebastian Thomas (datascience at sebastianthomas dot de)

# custom modules
from lists import *

# unit tests
import unittest


class TestLinkedListNode(unittest.TestCase):
    def setUp(self):
        self.node1 = BasicLinkedList.Node(1)
        self.node2 = BasicLinkedList.Node(2, successor=self.node1)
        self.node3 = BasicLinkedList.Node(3, successor=self.node2)

    def test_node_init(self):
        self.assertEqual(self.node1.value, 1)
        self.assertEqual(self.node1.successor, None)
        self.assertEqual(self.node2.value, 2)
        self.assertEqual(self.node2.successor, self.node1)
        self.assertEqual(self.node3.value, 3)
        self.assertEqual(self.node3.successor, self.node2)

    def test_node_repr(self):
        self.assertEqual(repr(self.node1), '1')
        self.assertEqual(repr(self.node2), '2')
        self.assertEqual(repr(self.node3), '3')

    def test_node_str(self):
        self.assertEqual(str(self.node1), '1')
        self.assertEqual(str(self.node2), '2')
        self.assertEqual(str(self.node3), '3')


class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.empty_list = BasicLinkedList()
        self.list_length_1 = BasicLinkedList([0])
        self.range_list = BasicLinkedList(range(4))
        self.list = BasicLinkedList([1, 42, -3, 2, 42])

    def test_init(self):
        # testing empty linked list
        self.assertEqual(self.empty_list._head, None)
        self.assertEqual(self.empty_list.tail, None)
        self.assertEqual(self.empty_list._len, 0)
        # testing linked list of length 1
        self.assertEqual(self.list_length_1._head.value, 0)
        self.assertEqual(self.list_length_1._head.successor, None)
        self.assertEqual(self.list_length_1.tail.value, 0)
        self.assertEqual(self.list_length_1.tail.successor, None)
        self.assertEqual(self.list_length_1._len, 1)
        # testing linked list constructed by range
        self.assertEqual(self.range_list._head.value, 0)
        self.assertEqual(self.range_list._head.successor.value, 1)
        self.assertEqual(self.range_list._head.successor.successor.value, 2)
        self.assertEqual(self.range_list._head.successor.successor.successor,
                         self.range_list.tail)
        self.assertEqual(self.range_list.tail.value, 3)
        self.assertEqual(self.range_list.tail.successor, None)
        self.assertEqual(self.range_list._len, 4)
        # testing linked list constructed by list
        self.assertEqual(self.list._head.value, 1)
        self.assertEqual(self.list._head.successor.value, 42)
        self.assertEqual(self.list._head.successor.successor.value, -3)
        self.assertEqual(self.list._head.successor.successor.successor.value, 2)
        self.assertEqual(self.list._head.successor.successor.successor
                         .successor, self.list.tail)
        self.assertEqual(self.list.tail.value, 42)
        self.assertEqual(self.list.tail.successor, None)
        self.assertEqual(self.list._len, 5)

    def test_bool(self):
        self.assertFalse(bool(self.empty_list))
        self.assertTrue(bool(self.list_length_1))
        self.assertTrue(bool(self.range_list))
        self.assertTrue(bool(self.list))

    def test_iter(self):
        self.assertEqual(list(iter(self.empty_list)), [])
        self.assertEqual(list(iter(self.list_length_1)), [0])
        self.assertEqual(list(iter(self.range_list)), list(range(4)))
        self.assertEqual(list(iter(self.list)), [1, 42, -3, 2, 42])

    def test_reversed(self):
        self.assertEqual(list(reversed(self.empty_list)), [])
        self.assertEqual(list(reversed(self.list_length_1)), [0])
        self.assertEqual(list(reversed(self.range_list)), [3, 2, 1, 0])
        self.assertEqual(list(reversed(self.list)), [42, 2, -3, 42, 1])

    def test_get_item(self):
        self.assertEqual(self.list_length_1[-1], 0)
        self.assertEqual(self.list_length_1[0], 0)
        self.assertEqual(self.range_list[-4], 0)
        self.assertEqual(self.range_list[-3], 1)
        self.assertEqual(self.range_list[-2], 2)
        self.assertEqual(self.range_list[-1], 3)
        self.assertEqual(self.range_list[0], 0)
        self.assertEqual(self.range_list[1], 1)
        self.assertEqual(self.range_list[2], 2)
        self.assertEqual(self.range_list[3], 3)
        self.assertEqual(self.list[-5], 1)
        self.assertEqual(self.list[-4], 42)
        self.assertEqual(self.list[-3], -3)
        self.assertEqual(self.list[-2], 2)
        self.assertEqual(self.list[-1], 42)
        self.assertEqual(self.list[0], 1)
        self.assertEqual(self.list[1], 42)
        self.assertEqual(self.list[2], -3)
        self.assertEqual(self.list[3], 2)
        self.assertEqual(self.list[4], 42)

        with self.assertRaises(IndexError):
            self.empty_list[0]
        with self.assertRaises(IndexError):
            self.list_length_1[-2]
        with self.assertRaises(IndexError):
            self.list_length_1[1]
        with self.assertRaises(IndexError):
            self.range_list[-5]
        with self.assertRaises(IndexError):
            self.range_list[4]
        with self.assertRaises(IndexError):
            self.list[-6]
        with self.assertRaises(IndexError):
            self.list[5]

    def test_set_item(self):
        self.list_length_1[0] = 1
        self.assertEqual(self.list_length_1[0], 1)

        self.range_list[0] = 1
        self.range_list[1] = 2
        self.range_list[2] = 3
        self.range_list[3] = 4
        self.assertEqual(self.range_list[0], 1)
        self.assertEqual(self.range_list[1], 2)
        self.assertEqual(self.range_list[2], 3)
        self.assertEqual(self.range_list[3], 4)

        self.list[-5] = 'l'
        self.list[-4] = 'l'
        self.list[-3] = 'i'
        self.list[-2] = 's'
        self.list[-1] = 't'
        self.assertEqual(self.list[-5], 'l')
        self.assertEqual(self.list[-4], 'l')
        self.assertEqual(self.list[-3], 'i')
        self.assertEqual(self.list[-2], 's')
        self.assertEqual(self.list[-1], 't')
        self.assertEqual(self.list[0], 'l')
        self.assertEqual(self.list[1], 'l')
        self.assertEqual(self.list[2], 'i')
        self.assertEqual(self.list[3], 's')
        self.assertEqual(self.list[4], 't')

        with self.assertRaises(IndexError):
            self.empty_list[0] = 0
        with self.assertRaises(IndexError):
            self.list_length_1[-2] = 0
        with self.assertRaises(IndexError):
            self.list_length_1[1] = 0
        with self.assertRaises(IndexError):
            self.range_list[-5] = 0
        with self.assertRaises(IndexError):
            self.range_list[4] = 0
        with self.assertRaises(IndexError):
            self.list[-6] = 0
        with self.assertRaises(IndexError):
            self.list[5] = 0

    def test_del_item(self):
        with self.assertRaises(IndexError):
            del self.empty_list[0]
        with self.assertRaises(IndexError):
            del self.list_length_1[-2]
        with self.assertRaises(IndexError):
            del self.list_length_1[1]
        with self.assertRaises(IndexError):
            del self.range_list[-5]
        with self.assertRaises(IndexError):
            del self.range_list[4]
        with self.assertRaises(IndexError):
            del self.list[-6]
        with self.assertRaises(IndexError):
            del self.list[5]

        del self.list_length_1[0]
        self.assertEqual(self.list_length_1._head, None)
        self.assertEqual(self.list_length_1.tail, None)
        self.assertEqual(self.list_length_1._len, 0)

        del self.range_list[1]
        self.assertEqual(self.range_list._head.value, 0)
        self.assertEqual(self.range_list.tail.value, 3)
        self.assertEqual(self.range_list._len, 3)
        with self.assertRaises(IndexError):
            self.range_list[-4]
        self.assertEqual(self.range_list[0], 0)
        self.assertEqual(self.range_list[1], 2)
        self.assertEqual(self.range_list[2], 3)
        with self.assertRaises(IndexError):
            self.range_list[3]

        del self.range_list[0]
        self.assertEqual(self.range_list._head.value, 2)
        self.assertEqual(self.range_list.tail.value, 3)
        self.assertEqual(self.range_list._len, 2)
        with self.assertRaises(IndexError):
            self.range_list[-3]
        self.assertEqual(self.range_list[0], 2)
        self.assertEqual(self.range_list[1], 3)
        with self.assertRaises(IndexError):
            self.range_list[2]

        del self.range_list[-1]
        self.assertEqual(self.range_list._head.value, 2)
        self.assertEqual(self.range_list.tail.value, 2)
        self.assertEqual(self.range_list._len, 1)
        with self.assertRaises(IndexError):
            self.range_list[-2]
        self.assertEqual(self.range_list[0], 2)
        with self.assertRaises(IndexError):
            self.range_list[1]

    def test_len(self):
        self.assertEqual(len(self.empty_list), 0)
        self.assertEqual(len(self.list_length_1), 1)
        self.assertEqual(len(self.range_list), 4)
        self.assertEqual(len(self.list), 5)

    def test_eq(self):
        self.assertEqual(self.empty_list, BasicLinkedList())
        self.assertEqual(self.list_length_1, BasicLinkedList(range(1)))
        self.assertEqual(self.range_list, BasicLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.list, BasicLinkedList((1, 42, -3, 2, 42)))
        self.assertNotEqual(self.empty_list, self.list_length_1)
        self.assertNotEqual(self.list_length_1, self.range_list)
        self.assertNotEqual(self.range_list, self.list)
        self.assertNotEqual(self.list, self.empty_list)
        self.assertNotEqual(self.empty_list, [])
        self.assertNotEqual(self.list_length_1, [0])
        self.assertNotEqual(self.range_list, range(4))
        self.assertNotEqual(self.list, [1, 42, -3, 2, 42])

    def test_add(self):
        with self.assertRaises(TypeError):
            self.empty_list + []
        with self.assertRaises(TypeError):
            self.list_length_1 + [1]
        with self.assertRaises(TypeError):
            self.range_list + [2, 3]
        with self.assertRaises(TypeError):
            self.list + ['a', 'b', 'c']

        self.assertEqual(self.empty_list + self.empty_list, BasicLinkedList())
        self.assertEqual(self.empty_list + self.list_length_1, BasicLinkedList([0]))
        self.assertEqual(self.empty_list + self.range_list,
                         BasicLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.empty_list + self.list,
                         BasicLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(self.list_length_1 + self.empty_list, BasicLinkedList([0]))
        self.assertEqual(self.list_length_1 + self.list_length_1,
                         BasicLinkedList([0, 0]))
        self.assertEqual(self.list_length_1 + self.range_list,
                         BasicLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.list_length_1 + self.list,
                         BasicLinkedList([0, 1, 42, -3, 2, 42]))
        self.assertEqual(self.range_list + self.empty_list,
                         BasicLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.range_list + self.list_length_1,
                         BasicLinkedList([0, 1, 2, 3, 0]))
        self.assertEqual(self.range_list + self.range_list,
                         BasicLinkedList([0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(self.range_list + self.list,
                         BasicLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list + self.empty_list,
                         BasicLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(self.list + self.list_length_1,
                         BasicLinkedList([1, 42, -3, 2, 42, 0]))
        self.assertEqual(self.list + self.range_list,
                         BasicLinkedList([1, 42, -3, 2, 42, 0, 1, 2, 3]))
        self.assertEqual(self.list + self.list,
                         BasicLinkedList([1, 42, -3, 2, 42, 1, 42, -3, 2, 42]))

    def test_iadd(self):
        with self.assertRaises(TypeError):
            self.empty_list += 2
        with self.assertRaises(TypeError):
            self.list_length_1 += 2.5
        with self.assertRaises(TypeError):
            self.range_list += True
        with self.assertRaises(TypeError):
            self.list += None

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list += self.list_length_1
        self.list_length_1 += self.range_list
        self.range_list += self.list
        self.list += self.empty_list

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, BasicLinkedList([0]))
        self.assertEqual(self.list_length_1, BasicLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.range_list,
                         BasicLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list, BasicLinkedList([1, 42, -3, 2, 42, 0]))

        self.empty_list += [-1, -1]
        self.list_length_1 += tuple('list')
        self.range_list += (-1, -2, -3)
        self.list += []

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, BasicLinkedList([0, -1, -1]))
        self.assertEqual(self.list_length_1,
                         BasicLinkedList([0, 0, 1, 2, 3, 'l', 'i', 's', 't']))
        self.assertEqual(self.range_list, BasicLinkedList([0, 1, 2, 3, 1, 42, -3, 2,
                                                           42, -1, -2, -3]))
        self.assertEqual(self.list, BasicLinkedList([1, 42, -3, 2, 42, 0]))

    def test_mul(self):
        with self.assertRaises(TypeError):
            self.empty_list * []
        with self.assertRaises(TypeError):
            self.list_length_1 * 3.5
        with self.assertRaises(TypeError):
            self.range_list * (2, 3)
        with self.assertRaises(TypeError):
            self.list * BasicLinkedList(['a', 'b', 'c'])

        with self.assertRaises(ValueError):
            self.empty_list * (-1)
        with self.assertRaises(ValueError):
            self.list_length_1 * (-2)
        with self.assertRaises(ValueError):
            self.range_list * (-3)
        with self.assertRaises(ValueError):
            self.list * (-4)

        self.assertEqual(self.empty_list * 0, BasicLinkedList())
        self.assertEqual(self.empty_list * 1, BasicLinkedList())
        self.assertEqual(self.empty_list * 2, BasicLinkedList())
        self.assertEqual(self.empty_list * 3, BasicLinkedList())
        self.assertEqual(self.list_length_1 * 0, BasicLinkedList())
        self.assertEqual(self.list_length_1 * 1, BasicLinkedList([0]))
        self.assertEqual(self.list_length_1 * 2, BasicLinkedList([0, 0]))
        self.assertEqual(self.list_length_1 * 3, BasicLinkedList([0, 0, 0]))
        self.assertEqual(self.range_list * 0, BasicLinkedList())
        self.assertEqual(self.range_list * 1, BasicLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.range_list * 2,
                         BasicLinkedList([0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(self.range_list * 3,
                         BasicLinkedList([0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(self.list * 0, BasicLinkedList())
        self.assertEqual(self.list * 1, BasicLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(self.list * 2,
                         BasicLinkedList([1, 42, -3, 2, 42, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list * 3, BasicLinkedList([1, 42, -3, 2, 42,
                                                         1, 42, -3, 2, 42,
                                                         1, 42, -3, 2, 42]))

    def test_imul(self):
        with self.assertRaises(TypeError):
            self.empty_list *= []
        with self.assertRaises(TypeError):
            self.list_length_1 *= 3.5
        with self.assertRaises(TypeError):
            self.range_list *= (2, 3)
        with self.assertRaises(TypeError):
            self.list *= BasicLinkedList(['a', 'b', 'c'])

        with self.assertRaises(ValueError):
            self.empty_list *= (-1)
        with self.assertRaises(ValueError):
            self.list_length_1 *= (-2)
        with self.assertRaises(ValueError):
            self.range_list *= (-3)
        with self.assertRaises(ValueError):
            self.list *= (-4)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list *= 2
        self.list_length_1 *= 3
        self.range_list *= 0
        self.list *= 1

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, BasicLinkedList())
        self.assertEqual(self.list_length_1, BasicLinkedList([0, 0, 0]))
        self.assertEqual(self.range_list, BasicLinkedList())
        self.assertEqual(self.list, BasicLinkedList([1, 42, -3, 2, 42]))

    def test_rmul(self):
        with self.assertRaises(TypeError):
            [] * self.empty_list
        with self.assertRaises(TypeError):
            3.5 * self.list_length_1
        with self.assertRaises(TypeError):
            (2, 3) * self.range_list
        with self.assertRaises(TypeError):
            BasicLinkedList(['a', 'b', 'c']) * self.list

        with self.assertRaises(ValueError):
            (-1) * self.empty_list
        with self.assertRaises(ValueError):
            (-2) * self.list_length_1
        with self.assertRaises(ValueError):
            (-3) * self.range_list
        with self.assertRaises(ValueError):
            (-4) * self.list

        self.assertEqual(0 * self.empty_list, BasicLinkedList())
        self.assertEqual(1 * self.empty_list, BasicLinkedList())
        self.assertEqual(2 * self.empty_list, BasicLinkedList())
        self.assertEqual(3 * self.empty_list, BasicLinkedList())
        self.assertEqual(0 * self.list_length_1, BasicLinkedList())
        self.assertEqual(1 * self.list_length_1, BasicLinkedList([0]))
        self.assertEqual(2 * self.list_length_1, BasicLinkedList([0, 0]))
        self.assertEqual(3 * self.list_length_1, BasicLinkedList([0, 0, 0]))
        self.assertEqual(0 * self.range_list, BasicLinkedList())
        self.assertEqual(1 * self.range_list, BasicLinkedList([0, 1, 2, 3]))
        self.assertEqual(2 * self.range_list,
                         BasicLinkedList([0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(3 * self.range_list,
                         BasicLinkedList([0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(0 * self.list, BasicLinkedList())
        self.assertEqual(1 * self.list, BasicLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(2 * self.list,
                         BasicLinkedList([1, 42, -3, 2, 42, 1, 42, -3, 2, 42]))
        self.assertEqual(3 * self.list, BasicLinkedList([1, 42, -3, 2, 42,
                                                         1, 42, -3, 2, 42,
                                                         1, 42, -3, 2, 42]))

    def test_extend_at_head(self):
        with self.assertRaises(TypeError):
            self.empty_list.extend_by_prepending(2)
        with self.assertRaises(TypeError):
            self.list_length_1.extend_by_prepending(2.5)
        with self.assertRaises(TypeError):
            self.range_list.extend_by_prepending(True)
        with self.assertRaises(TypeError):
            self.list.extend_by_prepending(None)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list.extend_by_prepending(self.list_length_1)
        self.list_length_1.extend_by_prepending(self.range_list)
        self.range_list.extend_by_prepending(self.list)
        self.list.extend_by_prepending(self.empty_list)

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, BasicLinkedList([0]))
        self.assertEqual(self.list_length_1, BasicLinkedList([0, 1, 2, 3, 0]))
        self.assertEqual(self.range_list,
                         BasicLinkedList([1, 42, -3, 2, 42, 0, 1, 2, 3]))
        self.assertEqual(self.list, BasicLinkedList([0, 1, 42, -3, 2, 42]))

        self.empty_list.extend_by_prepending([-1, -1])
        self.list_length_1.extend_by_prepending(tuple('list'))
        self.range_list.extend_by_prepending((-1, -2, -3))
        self.list.extend_by_prepending([])

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, BasicLinkedList([-1, -1, 0]))
        self.assertEqual(self.list_length_1,
                         BasicLinkedList(['l', 'i', 's', 't', 0, 1, 2, 3, 0]))
        self.assertEqual(self.range_list, BasicLinkedList([-1, -2, -3,
                                                           1, 42, -3, 2, 42,
                                                           0, 1, 2, 3]))
        self.assertEqual(self.list, BasicLinkedList([0, 1, 42, -3, 2, 42]))

    def test_extend_at_tail(self):
        with self.assertRaises(TypeError):
            self.empty_list.extend_by_appending(2)
        with self.assertRaises(TypeError):
            self.list_length_1.extend_by_appending(2.5)
        with self.assertRaises(TypeError):
            self.range_list.extend_by_appending(True)
        with self.assertRaises(TypeError):
            self.list.extend_by_appending(None)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list.extend_by_appending(self.list_length_1)
        self.list_length_1.extend_by_appending(self.range_list)
        self.range_list.extend_by_appending(self.list)
        self.list.extend_by_appending(self.empty_list)

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, BasicLinkedList([0]))
        self.assertEqual(self.list_length_1, BasicLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.range_list,
                         BasicLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list, BasicLinkedList([1, 42, -3, 2, 42, 0]))

        self.empty_list.extend_by_appending([-1, -1])
        self.list_length_1.extend_by_appending(tuple('list'))
        self.range_list.extend_by_appending((-1, -2, -3))
        self.list.extend_by_appending([])

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, BasicLinkedList([0, -1, -1]))
        self.assertEqual(self.list_length_1,
                         BasicLinkedList([0, 0, 1, 2, 3, 'l', 'i', 's', 't']))
        self.assertEqual(self.range_list, BasicLinkedList([0, 1, 2, 3,
                                                           1, 42, -3, 2, 42,
                                                           -1, -2, -3]))
        self.assertEqual(self.list, BasicLinkedList([1, 42, -3, 2, 42, 0]))

    def test_extend(self):
        with self.assertRaises(TypeError):
            self.empty_list.extend(2)
        with self.assertRaises(TypeError):
            self.list_length_1.extend(2.5)
        with self.assertRaises(TypeError):
            self.range_list.extend(True)
        with self.assertRaises(TypeError):
            self.list.extend(None)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list.extend(self.list_length_1)
        self.list_length_1.extend(self.range_list)
        self.range_list.extend(self.list)
        self.list.extend(self.empty_list)

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, BasicLinkedList([0]))
        self.assertEqual(self.list_length_1, BasicLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.range_list,
                         BasicLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list, BasicLinkedList([1, 42, -3, 2, 42, 0]))

        self.empty_list.extend([-1, -1])
        self.list_length_1.extend(tuple('list'))
        self.range_list.extend((-1, -2, -3))
        self.list.extend([])

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, BasicLinkedList([0, -1, -1]))
        self.assertEqual(self.list_length_1,
                         BasicLinkedList([0, 0, 1, 2, 3, 'l', 'i', 's', 't']))
        self.assertEqual(self.range_list, BasicLinkedList([0, 1, 2, 3,
                                                           1, 42, -3, 2, 42,
                                                           -1, -2, -3]))
        self.assertEqual(self.list, BasicLinkedList([1, 42, -3, 2, 42, 0]))

    def test_repr(self):
        self.assertEqual(repr(self.empty_list), 'LinkedList([])')
        self.assertEqual(repr(self.list_length_1), 'LinkedList([0])')
        self.assertEqual(repr(self.range_list), 'LinkedList([0, 1, 2, 3])')
        self.assertEqual(repr(self.list), 'LinkedList([1, 42, -3, 2, 42])')
        self.assertEqual(repr(BasicLinkedList(range(10))),
                         'LinkedList([0, 1, 2, 3, 4, 5, ...])')

    def test_str(self):
        self.assertEqual(str(self.empty_list), '')
        self.assertEqual(str(self.list_length_1), '0')
        self.assertEqual(str(self.range_list),
                         '0 \u2192 1 \u2192 2 \u2192 3')
        self.assertEqual(str(self.list),
                         '1 \u2192 42 \u2192 -3 \u2192 2 \u2192 42')
        self.assertEqual(str(BasicLinkedList(range(10))),
                         '0 \u2192 1 \u2192 2 \u2192 3 \u2192 4 \u2192 '
                         '5 \u2192 6 \u2192 7 \u2192 8 \u2192 9')

    def test_is_empty(self):
        self.assertTrue(self.empty_list.is_empty())
        self.assertFalse(self.list_length_1.is_empty())
        self.assertFalse(self.range_list.is_empty())
        self.assertFalse(self.list.is_empty())

    def test_index(self):
        self.assertEqual(self.list_length_1.index(0), 0)
        self.assertEqual(self.range_list.index(0), 0)
        self.assertEqual(self.range_list.index(1), 1)
        self.assertEqual(self.range_list.index(2), 2)
        self.assertEqual(self.range_list.index(3), 3)
        self.assertEqual(self.list.index(1), 0)
        self.assertEqual(self.list.index(42), 1)
        self.assertEqual(self.list.index(-3), 2)
        self.assertEqual(self.list.index(2), 3)
        self.assertEqual(self.list.index(42, 2), 4)

        with self.assertRaises(ValueError):
            self.empty_list.index(0)
        with self.assertRaises(ValueError):
            self.list_length_1.index(1)
        with self.assertRaises(ValueError):
            self.range_list.index(-1)
        with self.assertRaises(ValueError):
            self.range_list.index(4)
        with self.assertRaises(ValueError):
            self.range_list.index(0, 1)
        with self.assertRaises(ValueError):
            self.range_list.index(1, 2, 4)
        with self.assertRaises(ValueError):
            self.list.index(41)
        with self.assertRaises(ValueError):
            self.range_list.index(42, 2, 4)

    def test_insert_after(self):
        with self.assertRaises(IndexError):
            self.empty_list.insert_after(0, 0)
        with self.assertRaises(IndexError):
            self.list_length_1.insert_after(-2, 0)
        with self.assertRaises(IndexError):
            self.list_length_1.insert_after(1, 0)
        with self.assertRaises(IndexError):
            self.range_list.insert_after(-5, 0)
        with self.assertRaises(IndexError):
            self.range_list.insert_after(4, 0)
        with self.assertRaises(IndexError):
            self.list.insert_after(-6, 0)
        with self.assertRaises(IndexError):
            self.list.insert_after(5, 0)

        self.list_length_1.insert_after(0, 1)
        self.list_length_1.insert_after(-1, 2)
        self.range_list.insert_after(0, 3)
        self.range_list.insert_after(-1, -1)
        self.range_list.insert_after(-5, 42)
        self.list.insert_after(0, 3)
        self.list.insert_after(-1, -1)
        self.list.insert_after(-5, 42)

        self.assertEqual(self.list_length_1, BasicLinkedList([0, 1, 2]))
        self.assertEqual(self.range_list, BasicLinkedList([0, 3, 42, 1, 2, 3, -1]))
        self.assertEqual(self.list, BasicLinkedList([1, 3, 42, 42, -3, 2, 42, -1]))

    def test_insert_before(self):
        with self.assertRaises(IndexError):
            self.empty_list.insert_before(0, 0)
        with self.assertRaises(IndexError):
            self.list_length_1.insert_before(-2, 0)
        with self.assertRaises(IndexError):
            self.list_length_1.insert_before(1, 0)
        with self.assertRaises(IndexError):
            self.range_list.insert_before(-5, 0)
        with self.assertRaises(IndexError):
            self.range_list.insert_before(4, 0)
        with self.assertRaises(IndexError):
            self.list.insert_before(-6, 0)
        with self.assertRaises(IndexError):
            self.list.insert_before(5, 0)

        self.list_length_1.insert_before(0, 1)
        self.list_length_1.insert_before(-1, 2)
        self.range_list.insert_before(0, 3)
        self.range_list.insert_before(-1, -1)
        self.range_list.insert_before(-5, 42)
        self.list.insert_before(0, 3)
        self.list.insert_before(-1, -1)
        self.list.insert_before(-5, 42)

        self.assertEqual(self.list_length_1, BasicLinkedList([1, 2, 0]))
        self.assertEqual(self.range_list, BasicLinkedList([3, 42, 0, 1, 2, -1, 3]))
        self.assertEqual(self.list, BasicLinkedList([3, 1, 42, 42, -3, 2, -1, 42]))

    def test_insert(self):
        with self.assertRaises(IndexError):
            self.empty_list.insert(0, 0)
        with self.assertRaises(IndexError):
            self.list_length_1.insert(-2, 0)
        with self.assertRaises(IndexError):
            self.list_length_1.insert(1, 0)
        with self.assertRaises(IndexError):
            self.range_list.insert(-5, 0)
        with self.assertRaises(IndexError):
            self.range_list.insert(4, 0)
        with self.assertRaises(IndexError):
            self.list.insert(-6, 0)
        with self.assertRaises(IndexError):
            self.list.insert(5, 0)

        self.list_length_1.insert(0, 1)
        self.list_length_1.insert(-1, 2)
        self.range_list.insert(0, 3)
        self.range_list.insert(-1, -1)
        self.range_list.insert(-5, 42)
        self.list.insert(0, 3)
        self.list.insert(-1, -1)
        self.list.insert(-5, 42)

        self.assertEqual(self.list_length_1, BasicLinkedList([1, 2, 0]))
        self.assertEqual(self.range_list, BasicLinkedList([3, 42, 0, 1, 2, -1, 3]))
        self.assertEqual(self.list, BasicLinkedList([3, 1, 42, 42, -3, 2, -1, 42]))

    def test_prepend(self):
        self.empty_list.prepend(-1)
        self.list_length_1.prepend(-1)
        self.list_length_1.prepend(-2)
        self.range_list.prepend(-1)
        self.range_list.prepend(-2)
        self.range_list.prepend(-3)
        self.list.prepend(-1)
        self.list.prepend(-2)
        self.list.prepend(-3)

        self.assertEqual(self.empty_list, BasicLinkedList([-1]))
        self.assertEqual(self.list_length_1, BasicLinkedList([-2, -1, 0]))
        self.assertEqual(self.range_list, BasicLinkedList([-3, -2, -1, 0, 1, 2, 3]))
        self.assertEqual(self.list, BasicLinkedList([-3, -2, -1, 1, 42, -3, 2, 42]))

    def test_append(self):
        self.empty_list.append(-1)
        self.list_length_1.append(-1)
        self.list_length_1.append(-2)
        self.range_list.append(-1)
        self.range_list.append(-2)
        self.range_list.append(-3)
        self.list.append(-1)
        self.list.append(-2)
        self.list.append(-3)

        self.assertEqual(self.empty_list, BasicLinkedList([-1]))
        self.assertEqual(self.list_length_1, BasicLinkedList([0, -1, -2]))
        self.assertEqual(self.range_list, BasicLinkedList([0, 1, 2, 3, -1, -2, -3]))
        self.assertEqual(self.list, BasicLinkedList([1, 42, -3, 2, 42, -1, -2, -3]))

    def test_reverse(self):
        self.empty_list.reverse()
        self.list_length_1.reverse()
        self.range_list.reverse()
        self.list.reverse()

        self.assertEqual(self.empty_list, BasicLinkedList())
        self.assertEqual(self.list_length_1, BasicLinkedList([0]))
        self.assertEqual(self.range_list, BasicLinkedList([3, 2, 1, 0]))
        self.assertEqual(self.list, BasicLinkedList([42, 2, -3, 42, 1]))

    def test_pop(self):
        with self.assertRaises(IndexError):
            self.empty_list.pop()
        with self.assertRaises(IndexError):
            self.list_length_1.pop(index=-2)
        with self.assertRaises(IndexError):
            self.list_length_1.pop(index=1)
        with self.assertRaises(IndexError):
            self.range_list.pop(index=-5)
        with self.assertRaises(IndexError):
            self.range_list.pop(index=4)
        with self.assertRaises(IndexError):
            self.list.pop(index=-6)
        with self.assertRaises(IndexError):
            self.list.pop(index=5)

        self.list_length_1.pop()
        self.range_list.pop(index=2)
        self.range_list.pop()
        self.list.pop(index=1)
        self.list.pop(index=3)

        self.assertEqual(self.list_length_1, BasicLinkedList())
        self.assertEqual(self.range_list, BasicLinkedList([1, 3]))
        self.assertEqual(self.list, BasicLinkedList([1, -3, 2]))

        self.list.pop()
        self.list.pop()
        self.list.pop()
        with self.assertRaises(IndexError):
            self.list.pop()

    def test_remove_first(self):
        with self.assertRaises(ValueError):
            self.empty_list.remove_first(-1)
        with self.assertRaises(ValueError):
            self.list_length_1.remove_first(-1)
        with self.assertRaises(ValueError):
            self.range_list.remove_first(-1)
        with self.assertRaises(ValueError):
            self.list.remove_first(-1)

        self.list_length_1.remove_first(0)
        self.range_list.remove_first(1)
        self.range_list.remove_first(3)
        self.range_list.remove_first(0)
        self.list.remove_first(42)

        self.assertEqual(self.list_length_1, BasicLinkedList())
        self.assertEqual(self.range_list, BasicLinkedList([2]))
        self.assertEqual(self.list, BasicLinkedList([1, -3, 2, 42]))

        with self.assertRaises(ValueError):
            self.range_list.remove_first(1)
        self.list.remove_first(42)
        with self.assertRaises(ValueError):
            self.list.remove_first(42)

    def test_remove(self):
        with self.assertRaises(ValueError):
            self.empty_list.remove(-1)
        with self.assertRaises(ValueError):
            self.list_length_1.remove(-1)
        with self.assertRaises(ValueError):
            self.range_list.remove(-1)
        with self.assertRaises(ValueError):
            self.list.remove(-1)

        self.list_length_1.remove(0)
        self.range_list.remove(1)
        self.range_list.remove(3)
        self.range_list.remove(0)
        self.list.remove(42)

        self.assertEqual(self.list_length_1, BasicLinkedList())
        self.assertEqual(self.range_list, BasicLinkedList([2]))
        self.assertEqual(self.list, BasicLinkedList([1, -3, 2, 42]))

        with self.assertRaises(ValueError):
            self.range_list.remove(1)
        self.list.remove(42)
        with self.assertRaises(ValueError):
            self.list.remove(42)

    def test_remove_last(self):
        with self.assertRaises(ValueError):
            self.empty_list.remove_last(-1)
        with self.assertRaises(ValueError):
            self.list_length_1.remove_last(-1)
        with self.assertRaises(ValueError):
            self.range_list.remove_last(-1)
        with self.assertRaises(ValueError):
            self.list.remove_last(-1)

        self.list_length_1.remove_last(0)
        self.range_list.remove_last(1)
        self.range_list.remove_last(3)
        self.range_list.remove_last(0)
        self.list.remove_last(42)

        self.assertEqual(self.list_length_1, BasicLinkedList())
        self.assertEqual(self.range_list, BasicLinkedList([2]))
        self.assertEqual(self.list, BasicLinkedList([1, 42, -3, 2]))

        with self.assertRaises(ValueError):
            self.range_list.remove_last(1)
        self.list.remove_last(42)
        with self.assertRaises(ValueError):
            self.list.remove_last(42)


class TestCircularLinkedListNode(unittest.TestCase):
    def setUp(self):
        self.node1 = CircularLinkedList.Node(1)
        self.node2 = CircularLinkedList.Node(2, successor=self.node1)
        self.node3 = CircularLinkedList.Node(3, successor=self.node2)
        self.node1.successor = self.node3

    def test_node_init(self):
        self.assertEqual(self.node1.value, 1)
        self.assertEqual(self.node1.successor, self.node3)
        self.assertEqual(self.node2.value, 2)
        self.assertEqual(self.node2.successor, self.node1)
        self.assertEqual(self.node3.value, 3)
        self.assertEqual(self.node3.successor, self.node2)

    def test_node_repr(self):
        self.assertEqual(repr(self.node1), '1')
        self.assertEqual(repr(self.node2), '2')
        self.assertEqual(repr(self.node3), '3')

    def test_node_str(self):
        self.assertEqual(str(self.node1), '1')
        self.assertEqual(str(self.node2), '2')
        self.assertEqual(str(self.node3), '3')


class TestCircularLinkedList(unittest.TestCase):
    def setUp(self):
        self.empty_list = CircularLinkedList()
        self.list_length_1 = CircularLinkedList([0])
        self.range_list = CircularLinkedList(range(4))
        self.list = CircularLinkedList([1, 42, -3, 2, 42])

    def test_init(self):
        # testing empty linked list
        self.assertEqual(self.empty_list._head, None)
        self.assertEqual(self.empty_list._len, 0)
        # testing linked list of length 1
        self.assertEqual(self.list_length_1._head.value, 0)
        self.assertEqual(self.list_length_1._head.successor,
                         self.list_length_1._head)
        self.assertEqual(self.list_length_1._len, 1)
        # testing linked list constructed by range
        self.assertEqual(self.range_list._head.value, 0)
        self.assertEqual(self.range_list._head.successor.value, 1)
        self.assertEqual(self.range_list._head.successor.successor.value, 2)
        self.assertEqual(self.range_list._head.successor.successor.successor
                         .value, 3)
        self.assertEqual(self.range_list._head.successor.successor.successor
                         .successor, self.range_list._head)
        self.assertEqual(self.range_list._len, 4)
        # testing linked list constructed by list
        self.assertEqual(self.list._head.value, 1)
        self.assertEqual(self.list._head.successor.value, 42)
        self.assertEqual(self.list._head.successor.successor.value, -3)
        self.assertEqual(self.list._head.successor.successor.successor.value, 2)
        self.assertEqual(self.list._head.successor.successor.successor
                         .successor.value, 42)
        self.assertEqual(self.list._head.successor.successor.successor
                         .successor.successor, self.list._head)
        self.assertEqual(self.list._len, 5)

    def test_bool(self):
        self.assertFalse(bool(self.empty_list))
        self.assertTrue(bool(self.list_length_1))
        self.assertTrue(bool(self.range_list))
        self.assertTrue(bool(self.list))

    def test_iter(self):
        self.assertEqual(list(iter(self.empty_list)), [])
        self.assertEqual(list(iter(self.list_length_1)), [0])
        self.assertEqual(list(iter(self.range_list)), list(range(4)))
        self.assertEqual(list(iter(self.list)), [1, 42, -3, 2, 42])

    def test_reversed(self):
        self.assertEqual(list(reversed(self.empty_list)), [])
        self.assertEqual(list(reversed(self.list_length_1)), [0])
        self.assertEqual(list(reversed(self.range_list)), [3, 2, 1, 0])
        self.assertEqual(list(reversed(self.list)), [42, 2, -3, 42, 1])

    def test_get_item(self):
        self.assertEqual(self.list_length_1[-2], 0)
        self.assertEqual(self.list_length_1[-1], 0)
        self.assertEqual(self.list_length_1[0], 0)
        self.assertEqual(self.list_length_1[1], 0)
        self.assertEqual(self.range_list[-8], 0)
        self.assertEqual(self.range_list[-7], 1)
        self.assertEqual(self.range_list[-6], 2)
        self.assertEqual(self.range_list[-5], 3)
        self.assertEqual(self.range_list[-4], 0)
        self.assertEqual(self.range_list[-3], 1)
        self.assertEqual(self.range_list[-2], 2)
        self.assertEqual(self.range_list[-1], 3)
        self.assertEqual(self.range_list[0], 0)
        self.assertEqual(self.range_list[1], 1)
        self.assertEqual(self.range_list[2], 2)
        self.assertEqual(self.range_list[3], 3)
        self.assertEqual(self.range_list[4], 0)
        self.assertEqual(self.range_list[5], 1)
        self.assertEqual(self.range_list[6], 2)
        self.assertEqual(self.range_list[7], 3)
        self.assertEqual(self.list[-10], 1)
        self.assertEqual(self.list[-9], 42)
        self.assertEqual(self.list[-8], -3)
        self.assertEqual(self.list[-7], 2)
        self.assertEqual(self.list[-6], 42)
        self.assertEqual(self.list[-5], 1)
        self.assertEqual(self.list[-4], 42)
        self.assertEqual(self.list[-3], -3)
        self.assertEqual(self.list[-2], 2)
        self.assertEqual(self.list[-1], 42)
        self.assertEqual(self.list[0], 1)
        self.assertEqual(self.list[1], 42)
        self.assertEqual(self.list[2], -3)
        self.assertEqual(self.list[3], 2)
        self.assertEqual(self.list[4], 42)
        self.assertEqual(self.list[5], 1)
        self.assertEqual(self.list[6], 42)
        self.assertEqual(self.list[7], -3)
        self.assertEqual(self.list[8], 2)
        self.assertEqual(self.list[9], 42)

        with self.assertRaises(IndexError):
            self.empty_list[0]

    def test_set_item(self):
        self.list_length_1[-2] = 1
        self.assertEqual(self.list_length_1[0], 1)

        self.range_list[0] = 1
        self.range_list[1] = 2
        self.range_list[2] = 3
        self.range_list[3] = 4
        self.assertEqual(self.range_list[0], 1)
        self.assertEqual(self.range_list[1], 2)
        self.assertEqual(self.range_list[2], 3)
        self.assertEqual(self.range_list[3], 4)

        self.list[-25] = 'l'
        self.list[-19] = 'l'
        self.list[-13] = 'i'
        self.list[8] = 's'
        self.list[14] = 't'
        self.assertEqual(self.list[0], 'l')
        self.assertEqual(self.list[1], 'l')
        self.assertEqual(self.list[2], 'i')
        self.assertEqual(self.list[3], 's')
        self.assertEqual(self.list[4], 't')

        with self.assertRaises(IndexError):
            self.empty_list[0] = 0

    def test_del_item(self):
        with self.assertRaises(IndexError):
            del self.empty_list[0]

        del self.list_length_1[0]
        self.assertEqual(self.list_length_1._head, None)
        self.assertEqual(self.list_length_1._len, 0)

        del self.range_list[1]
        self.assertEqual(self.range_list._head.value, 0)
        self.assertEqual(self.range_list._len, 3)
        self.assertEqual(self.range_list[0], 0)
        self.assertEqual(self.range_list[1], 2)
        self.assertEqual(self.range_list[2], 3)

        del self.range_list[0]
        self.assertEqual(self.range_list._head.value, 2)
        self.assertEqual(self.range_list._len, 2)
        self.assertEqual(self.range_list[0], 2)
        self.assertEqual(self.range_list[1], 3)

        del self.range_list[-1]
        self.assertEqual(self.range_list._head.value, 2)
        self.assertEqual(self.range_list._len, 1)
        self.assertEqual(self.range_list[0], 2)

    def test_len(self):
        self.assertEqual(len(self.empty_list), 0)
        self.assertEqual(len(self.list_length_1), 1)
        self.assertEqual(len(self.range_list), 4)
        self.assertEqual(len(self.list), 5)

    def test_eq(self):
        self.assertEqual(self.empty_list, CircularLinkedList())
        self.assertEqual(self.list_length_1, CircularLinkedList(range(1)))
        self.assertEqual(self.range_list, CircularLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.list, CircularLinkedList((1, 42, -3, 2, 42)))
        self.assertNotEqual(self.empty_list, self.list_length_1)
        self.assertNotEqual(self.list_length_1, self.range_list)
        self.assertNotEqual(self.range_list, self.list)
        self.assertNotEqual(self.list, self.empty_list)
        self.assertNotEqual(self.empty_list, [])
        self.assertNotEqual(self.list_length_1, [0])
        self.assertNotEqual(self.range_list, range(4))
        self.assertNotEqual(self.list, [1, 42, -3, 2, 42])

    def test_add(self):
        with self.assertRaises(TypeError):
            self.empty_list + []
        with self.assertRaises(TypeError):
            self.list_length_1 + [1]
        with self.assertRaises(TypeError):
            self.range_list + [2, 3]
        with self.assertRaises(TypeError):
            self.list + ['a', 'b', 'c']

        self.assertEqual(self.empty_list + self.empty_list,
                         CircularLinkedList())
        self.assertEqual(self.empty_list + self.list_length_1,
                         CircularLinkedList([0]))
        self.assertEqual(self.empty_list + self.range_list,
                         CircularLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.empty_list + self.list,
                         CircularLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(self.list_length_1 + self.empty_list,
                         CircularLinkedList([0]))
        self.assertEqual(self.list_length_1 + self.list_length_1,
                         CircularLinkedList([0, 0]))
        self.assertEqual(self.list_length_1 + self.range_list,
                         CircularLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.list_length_1 + self.list,
                         CircularLinkedList([0, 1, 42, -3, 2, 42]))
        self.assertEqual(self.range_list + self.empty_list,
                         CircularLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.range_list + self.list_length_1,
                         CircularLinkedList([0, 1, 2, 3, 0]))
        self.assertEqual(self.range_list + self.range_list,
                         CircularLinkedList([0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(self.range_list + self.list,
                         CircularLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list + self.empty_list,
                         CircularLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(self.list + self.list_length_1,
                         CircularLinkedList([1, 42, -3, 2, 42, 0]))
        self.assertEqual(self.list + self.range_list,
                         CircularLinkedList([1, 42, -3, 2, 42, 0, 1, 2, 3]))
        self.assertEqual(self.list + self.list,
                         CircularLinkedList([1, 42, -3, 2, 42,
                                             1, 42, -3, 2, 42]))

    def test_iadd(self):
        with self.assertRaises(TypeError):
            self.empty_list += 2
        with self.assertRaises(TypeError):
            self.list_length_1 += 2.5
        with self.assertRaises(TypeError):
            self.range_list += True
        with self.assertRaises(TypeError):
            self.list += None

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list += self.list_length_1
        self.list_length_1 += self.range_list
        self.range_list += self.list
        self.list += self.empty_list

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularLinkedList([0]))
        self.assertEqual(self.list_length_1,
                         CircularLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.range_list,
                         CircularLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list, CircularLinkedList([1, 42, -3, 2, 42, 0]))

        self.empty_list += [-1, -1]
        self.list_length_1 += tuple('list')
        self.range_list += (-1, -2, -3)
        self.list += []

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularLinkedList([0, -1, -1]))
        self.assertEqual(self.list_length_1,
                         CircularLinkedList([0, 0, 1, 2, 3,
                                             'l', 'i', 's', 't']))
        self.assertEqual(self.range_list, CircularLinkedList([0, 1, 2, 3,
                                                              1, 42, -3, 2, 42,
                                                              -1, -2, -3]))
        self.assertEqual(self.list, CircularLinkedList([1, 42, -3, 2, 42, 0]))

    def test_mul(self):
        with self.assertRaises(TypeError):
            self.empty_list * []
        with self.assertRaises(TypeError):
            self.list_length_1 * 3.5
        with self.assertRaises(TypeError):
            self.range_list * (2, 3)
        with self.assertRaises(TypeError):
            self.list * CircularLinkedList(['a', 'b', 'c'])

        with self.assertRaises(ValueError):
            self.empty_list * (-1)
        with self.assertRaises(ValueError):
            self.list_length_1 * (-2)
        with self.assertRaises(ValueError):
            self.range_list * (-3)
        with self.assertRaises(ValueError):
            self.list * (-4)

        self.assertEqual(self.empty_list * 0, CircularLinkedList())
        self.assertEqual(self.empty_list * 1, CircularLinkedList())
        self.assertEqual(self.empty_list * 2, CircularLinkedList())
        self.assertEqual(self.empty_list * 3, CircularLinkedList())
        self.assertEqual(self.list_length_1 * 0, CircularLinkedList())
        self.assertEqual(self.list_length_1 * 1, CircularLinkedList([0]))
        self.assertEqual(self.list_length_1 * 2, CircularLinkedList([0, 0]))
        self.assertEqual(self.list_length_1 * 3, CircularLinkedList([0, 0, 0]))
        self.assertEqual(self.range_list * 0, CircularLinkedList())
        self.assertEqual(self.range_list * 1, CircularLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.range_list * 2,
                         CircularLinkedList([0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(self.range_list * 3, CircularLinkedList([0, 1, 2, 3,
                                                                  0, 1, 2, 3,
                                                                  0, 1, 2, 3]))
        self.assertEqual(self.list * 0, CircularLinkedList())
        self.assertEqual(self.list * 1, CircularLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(self.list * 2, CircularLinkedList([1, 42, -3, 2, 42,
                                                            1, 42, -3, 2, 42]))
        self.assertEqual(self.list * 3, CircularLinkedList([1, 42, -3, 2, 42,
                                                            1, 42, -3, 2, 42,
                                                            1, 42, -3, 2, 42]))

    def test_imul(self):
        with self.assertRaises(TypeError):
            self.empty_list *= []
        with self.assertRaises(TypeError):
            self.list_length_1 *= 3.5
        with self.assertRaises(TypeError):
            self.range_list *= (2, 3)
        with self.assertRaises(TypeError):
            self.list *= CircularLinkedList(['a', 'b', 'c'])

        with self.assertRaises(ValueError):
            self.empty_list *= (-1)
        with self.assertRaises(ValueError):
            self.list_length_1 *= (-2)
        with self.assertRaises(ValueError):
            self.range_list *= (-3)
        with self.assertRaises(ValueError):
            self.list *= (-4)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list *= 2
        self.list_length_1 *= 3
        self.range_list *= 0
        self.list *= 1

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularLinkedList())
        self.assertEqual(self.list_length_1, CircularLinkedList([0, 0, 0]))
        self.assertEqual(self.range_list, CircularLinkedList())
        self.assertEqual(self.list, CircularLinkedList([1, 42, -3, 2, 42]))

    def test_rmul(self):
        with self.assertRaises(TypeError):
            [] * self.empty_list
        with self.assertRaises(TypeError):
            3.5 * self.list_length_1
        with self.assertRaises(TypeError):
            (2, 3) * self.range_list
        with self.assertRaises(TypeError):
            CircularLinkedList(['a', 'b', 'c']) * self.list

        with self.assertRaises(ValueError):
            (-1) * self.empty_list
        with self.assertRaises(ValueError):
            (-2) * self.list_length_1
        with self.assertRaises(ValueError):
            (-3) * self.range_list
        with self.assertRaises(ValueError):
            (-4) * self.list

        self.assertEqual(0 * self.empty_list, CircularLinkedList())
        self.assertEqual(1 * self.empty_list, CircularLinkedList())
        self.assertEqual(2 * self.empty_list, CircularLinkedList())
        self.assertEqual(3 * self.empty_list, CircularLinkedList())
        self.assertEqual(0 * self.list_length_1, CircularLinkedList())
        self.assertEqual(1 * self.list_length_1, CircularLinkedList([0]))
        self.assertEqual(2 * self.list_length_1, CircularLinkedList([0, 0]))
        self.assertEqual(3 * self.list_length_1, CircularLinkedList([0, 0, 0]))
        self.assertEqual(0 * self.range_list, CircularLinkedList())
        self.assertEqual(1 * self.range_list, CircularLinkedList([0, 1, 2, 3]))
        self.assertEqual(2 * self.range_list,
                         CircularLinkedList([0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(3 * self.range_list, CircularLinkedList([0, 1, 2, 3,
                                                                  0, 1, 2, 3,
                                                                  0, 1, 2, 3]))
        self.assertEqual(0 * self.list, CircularLinkedList())
        self.assertEqual(1 * self.list, CircularLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(2 * self.list, CircularLinkedList([1, 42, -3, 2, 42,
                                                            1, 42, -3, 2, 42]))
        self.assertEqual(3 * self.list, CircularLinkedList([1, 42, -3, 2, 42,
                                                            1, 42, -3, 2, 42,
                                                            1, 42, -3, 2, 42]))

    def test_extend_by_prepending(self):
        with self.assertRaises(TypeError):
            self.empty_list.extend_by_prepending(2)
        with self.assertRaises(TypeError):
            self.list_length_1.extend_by_prepending(2.5)
        with self.assertRaises(TypeError):
            self.range_list.extend_by_prepending(True)
        with self.assertRaises(TypeError):
            self.list.extend_by_prepending(None)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list.extend_by_prepending(self.list_length_1)
        self.list_length_1.extend_by_prepending(self.range_list)
        self.range_list.extend_by_prepending(self.list)
        self.list.extend_by_prepending(self.empty_list)

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularLinkedList([0]))
        self.assertEqual(self.list_length_1,
                         CircularLinkedList([0, 1, 2, 3, 0]))
        self.assertEqual(self.range_list,
                         CircularLinkedList([1, 42, -3, 2, 42, 0, 1, 2, 3]))
        self.assertEqual(self.list, CircularLinkedList([0, 1, 42, -3, 2, 42]))

        self.empty_list.extend_by_prepending([-1, -1])
        self.list_length_1.extend_by_prepending(tuple('list'))
        self.range_list.extend_by_prepending((-1, -2, -3))
        self.list.extend_by_prepending([])

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularLinkedList([-1, -1, 0]))
        self.assertEqual(self.list_length_1,
                         CircularLinkedList(['l', 'i', 's', 't',
                                             0, 1, 2, 3, 0]))
        self.assertEqual(self.range_list, CircularLinkedList([-1, -2, -3,
                                                              1, 42, -3, 2, 42,
                                                              0, 1, 2, 3]))
        self.assertEqual(self.list, CircularLinkedList([0, 1, 42, -3, 2, 42]))

    def test_extend_by_appending(self):
        with self.assertRaises(TypeError):
            self.empty_list.extend_by_appending(2)
        with self.assertRaises(TypeError):
            self.list_length_1.extend_by_appending(2.5)
        with self.assertRaises(TypeError):
            self.range_list.extend_by_appending(True)
        with self.assertRaises(TypeError):
            self.list.extend_by_appending(None)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list.extend_by_appending(self.list_length_1)
        self.list_length_1.extend_by_appending(self.range_list)
        self.range_list.extend_by_appending(self.list)
        self.list.extend_by_appending(self.empty_list)

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularLinkedList([0]))
        self.assertEqual(self.list_length_1,
                         CircularLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.range_list,
                         CircularLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list, CircularLinkedList([1, 42, -3, 2, 42, 0]))

        self.empty_list.extend_by_appending([-1, -1])
        self.list_length_1.extend_by_appending(tuple('list'))
        self.range_list.extend_by_appending((-1, -2, -3))
        self.list.extend_by_appending([])

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularLinkedList([0, -1, -1]))
        self.assertEqual(self.list_length_1,
                         CircularLinkedList([0, 0, 1, 2, 3,
                                             'l', 'i', 's', 't']))
        self.assertEqual(self.range_list, CircularLinkedList([0, 1, 2, 3,
                                                              1, 42, -3, 2, 42,
                                                              -1, -2, -3]))
        self.assertEqual(self.list, CircularLinkedList([1, 42, -3, 2, 42, 0]))

    def test_extend(self):
        with self.assertRaises(TypeError):
            self.empty_list.extend(2)
        with self.assertRaises(TypeError):
            self.list_length_1.extend(2.5)
        with self.assertRaises(TypeError):
            self.range_list.extend(True)
        with self.assertRaises(TypeError):
            self.list.extend(None)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list.extend(self.list_length_1)
        self.list_length_1.extend(self.range_list)
        self.range_list.extend(self.list)
        self.list.extend(self.empty_list)

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularLinkedList([0]))
        self.assertEqual(self.list_length_1,
                         CircularLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.range_list,
                         CircularLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list, CircularLinkedList([1, 42, -3, 2, 42, 0]))

        self.empty_list.extend([-1, -1])
        self.list_length_1.extend(tuple('list'))
        self.range_list.extend((-1, -2, -3))
        self.list.extend([])

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularLinkedList([0, -1, -1]))
        self.assertEqual(self.list_length_1,
                         CircularLinkedList([0, 0, 1, 2, 3,
                                             'l', 'i', 's', 't']))
        self.assertEqual(self.range_list, CircularLinkedList([0, 1, 2, 3,
                                                              1, 42, -3, 2, 42,
                                                              -1, -2, -3]))
        self.assertEqual(self.list, CircularLinkedList([1, 42, -3, 2, 42, 0]))

    def test_repr(self):
        self.assertEqual(repr(self.empty_list), 'CircularLinkedList([])')
        self.assertEqual(repr(self.list_length_1), 'CircularLinkedList([0])')
        self.assertEqual(repr(self.range_list),
                         'CircularLinkedList([0, 1, 2, 3])')
        self.assertEqual(repr(self.list),
                         'CircularLinkedList([1, 42, -3, 2, 42])')
        self.assertEqual(repr(CircularLinkedList(range(10))),
                         'CircularLinkedList([0, 1, 2, 3, 4, 5, ...])')

    def test_str(self):
        self.assertEqual(str(self.empty_list), '')
        self.assertEqual(str(self.list_length_1), '0 \u2192')
        self.assertEqual(str(self.range_list),
                         '0 \u2192 1 \u2192 2 \u2192 3 \u2192')
        self.assertEqual(str(self.list),
                         '1 \u2192 42 \u2192 -3 \u2192 2 \u2192 42 \u2192')
        self.assertEqual(str(CircularLinkedList(range(10))),
                         '0 \u2192 1 \u2192 2 \u2192 3 \u2192 4 \u2192 '
                         '5 \u2192 6 \u2192 7 \u2192 8 \u2192 9 \u2192')

    def test_is_empty(self):
        self.assertTrue(self.empty_list.is_empty())
        self.assertFalse(self.list_length_1.is_empty())
        self.assertFalse(self.range_list.is_empty())
        self.assertFalse(self.list.is_empty())

    def test_index(self):
        self.assertEqual(self.list_length_1.index(0), 0)
        self.assertEqual(self.range_list.index(0), 0)
        self.assertEqual(self.range_list.index(1), 1)
        self.assertEqual(self.range_list.index(2), 2)
        self.assertEqual(self.range_list.index(3), 3)
        self.assertEqual(self.list.index(1), 0)
        self.assertEqual(self.list.index(42), 1)
        self.assertEqual(self.list.index(-3), 2)
        self.assertEqual(self.list.index(2), 3)
        self.assertEqual(self.list.index(42, 2), 4)

        with self.assertRaises(ValueError):
            self.empty_list.index(0)
        with self.assertRaises(ValueError):
            self.list_length_1.index(1)
        with self.assertRaises(ValueError):
            self.range_list.index(-1)
        with self.assertRaises(ValueError):
            self.range_list.index(4)
        with self.assertRaises(ValueError):
            self.range_list.index(0, 1)
        with self.assertRaises(ValueError):
            self.range_list.index(1, 2, 4)
        with self.assertRaises(ValueError):
            self.list.index(41)
        with self.assertRaises(ValueError):
            self.range_list.index(42, 2, 4)

    def test_insert_after(self):
        with self.assertRaises(IndexError):
            self.empty_list.insert_after(0, 0)

        self.list_length_1.insert_after(0, 1)
        self.list_length_1.insert_after(-1, 2)
        self.range_list.insert_after(0, 3)
        self.range_list.insert_after(-1, -1)
        self.range_list.insert_after(-5, 42)
        self.list.insert_after(0, 3)
        self.list.insert_after(-1, -1)
        self.list.insert_after(-5, 42)

        self.assertEqual(self.list_length_1, CircularLinkedList([0, 1, 2]))
        self.assertEqual(self.range_list,
                         CircularLinkedList([0, 3, 42, 1, 2, 3, -1]))
        self.assertEqual(self.list,
                         CircularLinkedList([1, 3, 42, 42, -3, 2, 42, -1]))

    def test_insert_before(self):
        with self.assertRaises(IndexError):
            self.empty_list.insert_before(0, 0)

        self.list_length_1.insert_before(0, 1)
        self.list_length_1.insert_before(-1, 2)
        self.range_list.insert_before(0, 3)
        self.range_list.insert_before(-1, -1)
        self.range_list.insert_before(-5, 42)
        self.list.insert_before(0, 3)
        self.list.insert_before(-1, -1)
        self.list.insert_before(-5, 42)

        self.assertEqual(self.list_length_1, CircularLinkedList([1, 2, 0]))
        self.assertEqual(self.range_list,
                         CircularLinkedList([3, 42, 0, 1, 2, -1, 3]))
        self.assertEqual(self.list,
                         CircularLinkedList([3, 1, 42, 42, -3, 2, -1, 42]))

    def test_insert(self):
        with self.assertRaises(IndexError):
            self.empty_list.insert(0, 0)

        self.list_length_1.insert(0, 1)
        self.list_length_1.insert(-1, 2)
        self.range_list.insert(0, 3)
        self.range_list.insert(-1, -1)
        self.range_list.insert(-5, 42)
        self.list.insert(0, 3)
        self.list.insert(-1, -1)
        self.list.insert(-5, 42)

        self.assertEqual(self.list_length_1, CircularLinkedList([1, 2, 0]))
        self.assertEqual(self.range_list,
                         CircularLinkedList([3, 42, 0, 1, 2, -1, 3]))
        self.assertEqual(self.list,
                         CircularLinkedList([3, 1, 42, 42, -3, 2, -1, 42]))

    def test_prepend(self):
        self.empty_list.prepend(-1)
        self.list_length_1.prepend(-1)
        self.list_length_1.prepend(-2)
        self.range_list.prepend(-1)
        self.range_list.prepend(-2)
        self.range_list.prepend(-3)
        self.list.prepend(-1)
        self.list.prepend(-2)
        self.list.prepend(-3)

        self.assertEqual(self.empty_list, CircularLinkedList([-1]))
        self.assertEqual(self.list_length_1, CircularLinkedList([-2, -1, 0]))
        self.assertEqual(self.range_list,
                         CircularLinkedList([-3, -2, -1, 0, 1, 2, 3]))
        self.assertEqual(self.list,
                         CircularLinkedList([-3, -2, -1, 1, 42, -3, 2, 42]))

    def test_append(self):
        self.empty_list.append(-1)
        self.list_length_1.append(-1)
        self.list_length_1.append(-2)
        self.range_list.append(-1)
        self.range_list.append(-2)
        self.range_list.append(-3)
        self.list.append(-1)
        self.list.append(-2)
        self.list.append(-3)

        self.assertEqual(self.empty_list, CircularLinkedList([-1]))
        self.assertEqual(self.list_length_1, CircularLinkedList([0, -1, -2]))
        self.assertEqual(self.range_list,
                         CircularLinkedList([0, 1, 2, 3, -1, -2, -3]))
        self.assertEqual(self.list,
                         CircularLinkedList([1, 42, -3, 2, 42, -1, -2, -3]))

    def test_reverse(self):
        self.empty_list.reverse()
        self.list_length_1.reverse()
        self.range_list.reverse()
        self.list.reverse()

        self.assertEqual(self.empty_list, CircularLinkedList())
        self.assertEqual(self.list_length_1, CircularLinkedList([0]))
        self.assertEqual(self.range_list, CircularLinkedList([3, 2, 1, 0]))
        self.assertEqual(self.list, CircularLinkedList([42, 2, -3, 42, 1]))

    def test_pop(self):
        with self.assertRaises(IndexError):
            self.empty_list.pop()

        self.list_length_1.pop()
        self.range_list.pop(index=2)
        self.range_list.pop()
        self.list.pop(index=1)
        self.list.pop(index=3)

        self.assertEqual(self.list_length_1, CircularLinkedList())
        self.assertEqual(self.range_list, CircularLinkedList([1, 3]))
        self.assertEqual(self.list, CircularLinkedList([1, -3, 2]))

        self.list.pop()
        self.list.pop()
        self.list.pop()
        with self.assertRaises(IndexError):
            self.list.pop()

    def test_remove_first(self):
        with self.assertRaises(ValueError):
            self.empty_list.remove_first(-1)
        with self.assertRaises(ValueError):
            self.list_length_1.remove_first(-1)
        with self.assertRaises(ValueError):
            self.range_list.remove_first(-1)
        with self.assertRaises(ValueError):
            self.list.remove_first(-1)

        self.list_length_1.remove_first(0)
        self.range_list.remove_first(1)
        self.range_list.remove_first(3)
        self.range_list.remove_first(0)
        self.list.remove_first(42)

        self.assertEqual(self.list_length_1, CircularLinkedList())
        self.assertEqual(self.range_list, CircularLinkedList([2]))
        self.assertEqual(self.list, CircularLinkedList([1, -3, 2, 42]))

        with self.assertRaises(ValueError):
            self.range_list.remove_first(1)
        self.list.remove_first(42)
        with self.assertRaises(ValueError):
            self.list.remove_first(42)

    def test_remove(self):
        with self.assertRaises(ValueError):
            self.empty_list.remove(-1)
        with self.assertRaises(ValueError):
            self.list_length_1.remove(-1)
        with self.assertRaises(ValueError):
            self.range_list.remove(-1)
        with self.assertRaises(ValueError):
            self.list.remove(-1)

        self.list_length_1.remove(0)
        self.range_list.remove(1)
        self.range_list.remove(3)
        self.range_list.remove(0)
        self.list.remove(42)

        self.assertEqual(self.list_length_1, CircularLinkedList())
        self.assertEqual(self.range_list, CircularLinkedList([2]))
        self.assertEqual(self.list, CircularLinkedList([1, -3, 2, 42]))

        with self.assertRaises(ValueError):
            self.range_list.remove(1)
        self.list.remove(42)
        with self.assertRaises(ValueError):
            self.list.remove(42)

    def test_remove_last(self):
        with self.assertRaises(ValueError):
            self.empty_list.remove_last(-1)
        with self.assertRaises(ValueError):
            self.list_length_1.remove_last(-1)
        with self.assertRaises(ValueError):
            self.range_list.remove_last(-1)
        with self.assertRaises(ValueError):
            self.list.remove_last(-1)

        self.list_length_1.remove_last(0)
        self.range_list.remove_last(1)
        self.range_list.remove_last(3)
        self.range_list.remove_last(0)
        self.list.remove_last(42)

        self.assertEqual(self.list_length_1, CircularLinkedList())
        self.assertEqual(self.range_list, CircularLinkedList([2]))
        self.assertEqual(self.list, CircularLinkedList([1, 42, -3, 2]))

        with self.assertRaises(ValueError):
            self.range_list.remove_last(1)
        self.list.remove_last(42)
        with self.assertRaises(ValueError):
            self.list.remove_last(42)


class TestDoublyLinkedListNode(unittest.TestCase):
    def setUp(self):
        self.node1 = DoublyLinkedList.Node(1)
        self.node2 = DoublyLinkedList.Node(2, predecessor=self.node1)
        self.node1.successor = self.node2
        self.node3 = DoublyLinkedList.Node(3, predecessor=self.node2)
        self.node2.successor = self.node3

    def test_init(self):
        self.assertEqual(self.node1.value, 1)
        self.assertEqual(self.node1.predecessor, None)
        self.assertEqual(self.node1.successor, self.node2)
        self.assertEqual(self.node2.value, 2)
        self.assertEqual(self.node2.predecessor, self.node1)
        self.assertEqual(self.node2.successor, self.node3)
        self.assertEqual(self.node3.value, 3)
        self.assertEqual(self.node3.predecessor, self.node2)
        self.assertEqual(self.node3.successor, None)

    def test_node_repr(self):
        self.assertEqual(repr(self.node1), '1')
        self.assertEqual(repr(self.node2), '2')
        self.assertEqual(repr(self.node3), '3')

    def test_node_str(self):
        self.assertEqual(str(self.node1), '1')
        self.assertEqual(str(self.node2), '2')
        self.assertEqual(str(self.node3), '3')


class TestDoublyLinkedList(unittest.TestCase):
    def setUp(self):
        self.empty_list = DoublyLinkedList()
        self.list_length_1 = DoublyLinkedList([0])
        self.range_list = DoublyLinkedList(range(4))
        self.list = DoublyLinkedList([1, 42, -3, 2, 42])

    def test_init(self):
        # testing empty linked list
        self.assertEqual(self.empty_list._head, None)
        self.assertEqual(self.empty_list._tail, None)
        self.assertEqual(self.empty_list._len, 0)
        # testing linked list of length 1
        self.assertEqual(self.list_length_1._head.value, 0)
        self.assertEqual(self.list_length_1._head.predecessor, None)
        self.assertEqual(self.list_length_1._head.successor, None)
        self.assertEqual(self.list_length_1._tail.value, 0)
        self.assertEqual(self.list_length_1._tail.predecessor, None)
        self.assertEqual(self.list_length_1._tail.successor, None)
        self.assertEqual(self.list_length_1._len, 1)
        # testing linked list constructed by range
        self.assertEqual(self.range_list._head.value, 0)
        self.assertEqual(self.range_list._head.predecessor, None)
        self.assertEqual(self.range_list._head.successor.value, 1)
        self.assertEqual(self.range_list._head.successor.predecessor.value, 0)
        self.assertEqual(self.range_list._head.successor.successor.value, 2)
        self.assertEqual(self.range_list._head.successor.successor.predecessor
                         .value, 1)
        self.assertEqual(self.range_list._head.successor.successor.successor,
                         self.range_list._tail)
        self.assertEqual(self.range_list._tail.value, 3)
        self.assertEqual(self.range_list._tail.predecessor.value, 2)
        self.assertEqual(self.range_list._tail.successor, None)
        self.assertEqual(self.range_list._len, 4)
        # testing linked list constructed by list
        self.assertEqual(self.list._head.value, 1)
        self.assertEqual(self.list._head.predecessor, None)
        self.assertEqual(self.list._head.successor.value, 42)
        self.assertEqual(self.list._head.successor.predecessor.value, 1)
        self.assertEqual(self.list._head.successor.successor.value, -3)
        self.assertEqual(self.list._head.successor.successor.predecessor.value,
                         42)
        self.assertEqual(self.list._head.successor.successor.successor.value, 2)
        self.assertEqual(self.list._head.successor.successor.successor
                         .predecessor.value, -3)
        self.assertEqual(self.list._head.successor.successor.successor
                         .successor, self.list._tail)
        self.assertEqual(self.list._tail.value, 42)
        self.assertEqual(self.list._tail.predecessor.value, 2)
        self.assertEqual(self.list._tail.successor, None)
        self.assertEqual(self.list._len, 5)

    def test_bool(self):
        self.assertFalse(bool(self.empty_list))
        self.assertTrue(bool(self.list_length_1))
        self.assertTrue(bool(self.range_list))
        self.assertTrue(bool(self.list))

    def test_iter(self):
        self.assertEqual(list(iter(self.empty_list)), [])
        self.assertEqual(list(iter(self.list_length_1)), [0])
        self.assertEqual(list(iter(self.range_list)), list(range(4)))
        self.assertEqual(list(iter(self.list)), [1, 42, -3, 2, 42])

    def test_reversed(self):
        self.assertEqual(list(reversed(self.empty_list)), [])
        self.assertEqual(list(reversed(self.list_length_1)), [0])
        self.assertEqual(list(reversed(self.range_list)), [3, 2, 1, 0])
        self.assertEqual(list(reversed(self.list)), [42, 2, -3, 42, 1])

    def test_get_item(self):
        self.assertEqual(self.list_length_1[-1], 0)
        self.assertEqual(self.list_length_1[0], 0)
        self.assertEqual(self.range_list[-4], 0)
        self.assertEqual(self.range_list[-3], 1)
        self.assertEqual(self.range_list[-2], 2)
        self.assertEqual(self.range_list[-1], 3)
        self.assertEqual(self.range_list[0], 0)
        self.assertEqual(self.range_list[1], 1)
        self.assertEqual(self.range_list[2], 2)
        self.assertEqual(self.range_list[3], 3)
        self.assertEqual(self.list[-5], 1)
        self.assertEqual(self.list[-4], 42)
        self.assertEqual(self.list[-3], -3)
        self.assertEqual(self.list[-2], 2)
        self.assertEqual(self.list[-1], 42)
        self.assertEqual(self.list[0], 1)
        self.assertEqual(self.list[1], 42)
        self.assertEqual(self.list[2], -3)
        self.assertEqual(self.list[3], 2)
        self.assertEqual(self.list[4], 42)

        with self.assertRaises(IndexError):
            self.empty_list[0]
        with self.assertRaises(IndexError):
            self.list_length_1[-2]
        with self.assertRaises(IndexError):
            self.list_length_1[1]
        with self.assertRaises(IndexError):
            self.range_list[-5]
        with self.assertRaises(IndexError):
            self.range_list[4]
        with self.assertRaises(IndexError):
            self.list[-6]
        with self.assertRaises(IndexError):
            self.list[5]

    def test_set_item(self):
        self.list_length_1[0] = 1
        self.assertEqual(self.list_length_1[-1], 1)
        self.assertEqual(self.list_length_1[0], 1)

        self.range_list[0] = 1
        self.range_list[1] = 2
        self.range_list[2] = 3
        self.range_list[3] = 4
        self.assertEqual(self.range_list[0], 1)
        self.assertEqual(self.range_list[1], 2)
        self.assertEqual(self.range_list[2], 3)
        self.assertEqual(self.range_list[3], 4)

        self.list[-5] = 'l'
        self.list[-4] = 'l'
        self.list[-3] = 'i'
        self.list[-2] = 's'
        self.list[-1] = 't'
        self.assertEqual(self.list[0], 'l')
        self.assertEqual(self.list[1], 'l')
        self.assertEqual(self.list[2], 'i')
        self.assertEqual(self.list[3], 's')
        self.assertEqual(self.list[4], 't')

        with self.assertRaises(IndexError):
            self.empty_list[0] = 0
        with self.assertRaises(IndexError):
            self.list_length_1[-2] = 0
        with self.assertRaises(IndexError):
            self.list_length_1[1] = 0
        with self.assertRaises(IndexError):
            self.range_list[-5] = 0
        with self.assertRaises(IndexError):
            self.range_list[4] = 0
        with self.assertRaises(IndexError):
            self.list[-6] = 0
        with self.assertRaises(IndexError):
            self.list[5] = 0

    def test_del_item(self):
        with self.assertRaises(IndexError):
            del self.empty_list[0]
        with self.assertRaises(IndexError):
            del self.list_length_1[-2]
        with self.assertRaises(IndexError):
            del self.list_length_1[1]
        with self.assertRaises(IndexError):
            del self.range_list[-5]
        with self.assertRaises(IndexError):
            del self.range_list[4]
        with self.assertRaises(IndexError):
            del self.list[-6]
        with self.assertRaises(IndexError):
            del self.list[5]

        del self.list_length_1[0]
        self.assertEqual(self.list_length_1._head, None)
        self.assertEqual(self.list_length_1._tail, None)
        self.assertEqual(self.list_length_1._len, 0)

        del self.range_list[1]
        self.assertEqual(self.range_list._head.value, 0)
        self.assertEqual(self.range_list._tail.value, 3)
        self.assertEqual(self.range_list._len, 3)
        with self.assertRaises(IndexError):
            self.range_list[-4]
        self.assertEqual(self.range_list[0], 0)
        self.assertEqual(self.range_list[1], 2)
        self.assertEqual(self.range_list[2], 3)
        with self.assertRaises(IndexError):
            self.range_list[3]

        del self.range_list[0]
        self.assertEqual(self.range_list._head.value, 2)
        self.assertEqual(self.range_list._tail.value, 3)
        self.assertEqual(self.range_list._len, 2)
        with self.assertRaises(IndexError):
            self.range_list[-3]
        self.assertEqual(self.range_list[0], 2)
        self.assertEqual(self.range_list[1], 3)
        with self.assertRaises(IndexError):
            self.range_list[2]

        del self.range_list[-1]
        self.assertEqual(self.range_list._head.value, 2)
        self.assertEqual(self.range_list._tail.value, 2)
        self.assertEqual(self.range_list._len, 1)
        with self.assertRaises(IndexError):
            self.range_list[-2]
        self.assertEqual(self.range_list[0], 2)
        with self.assertRaises(IndexError):
            self.range_list[1]

    def test_len(self):
        self.assertEqual(len(self.empty_list), 0)
        self.assertEqual(len(self.list_length_1), 1)
        self.assertEqual(len(self.range_list), 4)
        self.assertEqual(len(self.list), 5)

    def test_eq(self):
        self.assertEqual(self.empty_list, DoublyLinkedList())
        self.assertEqual(self.list_length_1, DoublyLinkedList(range(1)))
        self.assertEqual(self.range_list, DoublyLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.list, DoublyLinkedList((1, 42, -3, 2, 42)))
        self.assertNotEqual(self.empty_list, self.list_length_1)
        self.assertNotEqual(self.list_length_1, self.range_list)
        self.assertNotEqual(self.range_list, self.list)
        self.assertNotEqual(self.list, self.empty_list)
        self.assertNotEqual(self.empty_list, [])
        self.assertNotEqual(self.list_length_1, [0])
        self.assertNotEqual(self.range_list, range(4))
        self.assertNotEqual(self.list, [1, 42, -3, 2, 42])

    def test_add(self):
        with self.assertRaises(TypeError):
            self.empty_list + []
        with self.assertRaises(TypeError):
            self.list_length_1 + [1]
        with self.assertRaises(TypeError):
            self.range_list + [2, 3]
        with self.assertRaises(TypeError):
            self.list + ['a', 'b', 'c']

        self.assertEqual(self.empty_list + self.empty_list, DoublyLinkedList())
        self.assertEqual(self.empty_list + self.list_length_1,
                         DoublyLinkedList([0]))
        self.assertEqual(self.empty_list + self.range_list,
                         DoublyLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.empty_list + self.list,
                         DoublyLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(self.list_length_1 + self.empty_list,
                         DoublyLinkedList([0]))
        self.assertEqual(self.list_length_1 + self.list_length_1,
                         DoublyLinkedList([0, 0]))
        self.assertEqual(self.list_length_1 + self.range_list,
                         DoublyLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.list_length_1 + self.list,
                         DoublyLinkedList([0, 1, 42, -3, 2, 42]))
        self.assertEqual(self.range_list + self.empty_list,
                         DoublyLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.range_list + self.list_length_1,
                         DoublyLinkedList([0, 1, 2, 3, 0]))
        self.assertEqual(self.range_list + self.range_list,
                         DoublyLinkedList([0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(self.range_list + self.list,
                         DoublyLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list + self.empty_list,
                         DoublyLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(self.list + self.list_length_1,
                         DoublyLinkedList([1, 42, -3, 2, 42, 0]))
        self.assertEqual(self.list + self.range_list,
                         DoublyLinkedList([1, 42, -3, 2, 42, 0, 1, 2, 3]))
        self.assertEqual(self.list + self.list,
                         DoublyLinkedList([1, 42, -3, 2, 42,
                                           1, 42, -3, 2, 42]))

    def test_iadd(self):
        with self.assertRaises(TypeError):
            self.empty_list += 2
        with self.assertRaises(TypeError):
            self.list_length_1 += 2.5
        with self.assertRaises(TypeError):
            self.range_list += True
        with self.assertRaises(TypeError):
            self.list += None

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list += self.list_length_1
        self.list_length_1 += self.range_list
        self.range_list += self.list
        self.list += self.empty_list

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, DoublyLinkedList([0]))
        self.assertEqual(self.list_length_1, DoublyLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.range_list,
                         DoublyLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list, DoublyLinkedList([1, 42, -3, 2, 42, 0]))

        self.empty_list += [-1, -1]
        self.list_length_1 += tuple('list')
        self.range_list += (-1, -2, -3)
        self.list += []

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, DoublyLinkedList([0, -1, -1]))
        self.assertEqual(self.list_length_1,
                         DoublyLinkedList([0, 0, 1, 2, 3, 'l', 'i', 's', 't']))
        self.assertEqual(self.range_list,
                         DoublyLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42, -1,
                                           -2, -3]))
        self.assertEqual(self.list, DoublyLinkedList([1, 42, -3, 2, 42, 0]))

    def test_mul(self):
        with self.assertRaises(TypeError):
            self.empty_list * []
        with self.assertRaises(TypeError):
            self.list_length_1 * 3.5
        with self.assertRaises(TypeError):
            self.range_list * (2, 3)
        with self.assertRaises(TypeError):
            self.list * BasicLinkedList(['a', 'b', 'c'])

        with self.assertRaises(ValueError):
            self.empty_list * (-1)
        with self.assertRaises(ValueError):
            self.list_length_1 * (-2)
        with self.assertRaises(ValueError):
            self.range_list * (-3)
        with self.assertRaises(ValueError):
            self.list * (-4)

        self.assertEqual(self.empty_list * 0, DoublyLinkedList())
        self.assertEqual(self.empty_list * 1, DoublyLinkedList())
        self.assertEqual(self.empty_list * 2, DoublyLinkedList())
        self.assertEqual(self.empty_list * 3, DoublyLinkedList())
        self.assertEqual(self.list_length_1 * 0, DoublyLinkedList())
        self.assertEqual(self.list_length_1 * 1, DoublyLinkedList([0]))
        self.assertEqual(self.list_length_1 * 2, DoublyLinkedList([0, 0]))
        self.assertEqual(self.list_length_1 * 3, DoublyLinkedList([0, 0, 0]))
        self.assertEqual(self.range_list * 0, DoublyLinkedList())
        self.assertEqual(self.range_list * 1, DoublyLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.range_list * 2,
                         DoublyLinkedList([0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(self.range_list * 3, DoublyLinkedList([0, 1, 2, 3,
                                                                0, 1, 2, 3,
                                                                0, 1, 2, 3]))
        self.assertEqual(self.list * 0, DoublyLinkedList())
        self.assertEqual(self.list * 1, DoublyLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(self.list * 2, DoublyLinkedList([1, 42, -3, 2, 42,
                                                          1, 42, -3, 2, 42]))
        self.assertEqual(self.list * 3, DoublyLinkedList([1, 42, -3, 2, 42,
                                                          1, 42, -3, 2, 42,
                                                          1, 42, -3, 2, 42]))

    def test_imul(self):
        with self.assertRaises(TypeError):
            self.empty_list *= []
        with self.assertRaises(TypeError):
            self.list_length_1 *= 3.5
        with self.assertRaises(TypeError):
            self.range_list *= (2, 3)
        with self.assertRaises(TypeError):
            self.list *= BasicLinkedList(['a', 'b', 'c'])

        with self.assertRaises(ValueError):
            self.empty_list *= (-1)
        with self.assertRaises(ValueError):
            self.list_length_1 *= (-2)
        with self.assertRaises(ValueError):
            self.range_list *= (-3)
        with self.assertRaises(ValueError):
            self.list *= (-4)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list *= 2
        self.list_length_1 *= 3
        self.range_list *= 0
        self.list *= 1

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, DoublyLinkedList())
        self.assertEqual(self.list_length_1, DoublyLinkedList([0, 0, 0]))
        self.assertEqual(self.range_list, DoublyLinkedList())
        self.assertEqual(self.list, DoublyLinkedList([1, 42, -3, 2, 42]))

    def test_rmul(self):
        with self.assertRaises(TypeError):
            [] * self.empty_list
        with self.assertRaises(TypeError):
            3.5 * self.list_length_1
        with self.assertRaises(TypeError):
            (2, 3) * self.range_list
        with self.assertRaises(TypeError):
            BasicLinkedList(['a', 'b', 'c']) * self.list

        with self.assertRaises(ValueError):
            (-1) * self.empty_list
        with self.assertRaises(ValueError):
            (-2) * self.list_length_1
        with self.assertRaises(ValueError):
            (-3) * self.range_list
        with self.assertRaises(ValueError):
            (-4) * self.list

        self.assertEqual(0 * self.empty_list, DoublyLinkedList())
        self.assertEqual(1 * self.empty_list, DoublyLinkedList())
        self.assertEqual(2 * self.empty_list, DoublyLinkedList())
        self.assertEqual(3 * self.empty_list, DoublyLinkedList())
        self.assertEqual(0 * self.list_length_1, DoublyLinkedList())
        self.assertEqual(1 * self.list_length_1, DoublyLinkedList([0]))
        self.assertEqual(2 * self.list_length_1, DoublyLinkedList([0, 0]))
        self.assertEqual(3 * self.list_length_1, DoublyLinkedList([0, 0, 0]))
        self.assertEqual(0 * self.range_list, DoublyLinkedList())
        self.assertEqual(1 * self.range_list, DoublyLinkedList([0, 1, 2, 3]))
        self.assertEqual(2 * self.range_list,
                         DoublyLinkedList([0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(3 * self.range_list, DoublyLinkedList([0, 1, 2, 3,
                                                                0, 1, 2, 3,
                                                                0, 1, 2, 3]))
        self.assertEqual(0 * self.list, DoublyLinkedList())
        self.assertEqual(1 * self.list, DoublyLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(2 * self.list, DoublyLinkedList([1, 42, -3, 2, 42,
                                                          1, 42, -3, 2, 42]))
        self.assertEqual(3 * self.list, DoublyLinkedList([1, 42, -3, 2, 42,
                                                          1, 42, -3, 2, 42,
                                                          1, 42, -3, 2, 42]))

    def test_extend_at_head(self):
        with self.assertRaises(TypeError):
            self.empty_list.extend_by_prepending(2)
        with self.assertRaises(TypeError):
            self.list_length_1.extend_by_prepending(2.5)
        with self.assertRaises(TypeError):
            self.range_list.extend_by_prepending(True)
        with self.assertRaises(TypeError):
            self.list.extend_by_prepending(None)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list.extend_by_prepending(self.list_length_1)
        self.list_length_1.extend_by_prepending(self.range_list)
        self.range_list.extend_by_prepending(self.list)
        self.list.extend_by_prepending(self.empty_list)

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, DoublyLinkedList([0]))
        self.assertEqual(self.list_length_1, DoublyLinkedList([0, 1, 2, 3, 0]))
        self.assertEqual(self.range_list,
                         DoublyLinkedList([1, 42, -3, 2, 42, 0, 1, 2, 3]))
        self.assertEqual(self.list, DoublyLinkedList([0, 1, 42, -3, 2, 42]))

        self.empty_list.extend_by_prepending([-1, -1])
        self.list_length_1.extend_by_prepending(tuple('list'))
        self.range_list.extend_by_prepending((-1, -2, -3))
        self.list.extend_by_prepending([])

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, DoublyLinkedList([-1, -1, 0]))
        self.assertEqual(self.list_length_1,
                         DoublyLinkedList(['l', 'i', 's', 't', 0, 1, 2, 3, 0]))
        self.assertEqual(self.range_list, DoublyLinkedList([-1, -2, -3,
                                                            1, 42, -3, 2, 42,
                                                            0, 1, 2, 3]))
        self.assertEqual(self.list, DoublyLinkedList([0, 1, 42, -3, 2, 42]))

    def test_extend_at_tail(self):
        with self.assertRaises(TypeError):
            self.empty_list.extend_by_appending(2)
        with self.assertRaises(TypeError):
            self.list_length_1.extend_by_appending(2.5)
        with self.assertRaises(TypeError):
            self.range_list.extend_by_appending(True)
        with self.assertRaises(TypeError):
            self.list.extend_by_appending(None)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list.extend_by_appending(self.list_length_1)
        self.list_length_1.extend_by_appending(self.range_list)
        self.range_list.extend_by_appending(self.list)
        self.list.extend_by_appending(self.empty_list)

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, DoublyLinkedList([0]))
        self.assertEqual(self.list_length_1, DoublyLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.range_list,
                         DoublyLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list, DoublyLinkedList([1, 42, -3, 2, 42, 0]))

        self.empty_list.extend_by_appending([-1, -1])
        self.list_length_1.extend_by_appending(tuple('list'))
        self.range_list.extend_by_appending((-1, -2, -3))
        self.list.extend_by_appending([])

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, DoublyLinkedList([0, -1, -1]))
        self.assertEqual(self.list_length_1,
                         DoublyLinkedList([0, 0, 1, 2, 3, 'l', 'i', 's', 't']))
        self.assertEqual(self.range_list, DoublyLinkedList([0, 1, 2, 3,
                                                            1, 42, -3, 2, 42,
                                                            -1, -2, -3]))
        self.assertEqual(self.list, DoublyLinkedList([1, 42, -3, 2, 42, 0]))

    def test_extend(self):
        with self.assertRaises(TypeError):
            self.empty_list.extend(2)
        with self.assertRaises(TypeError):
            self.list_length_1.extend(2.5)
        with self.assertRaises(TypeError):
            self.range_list.extend(True)
        with self.assertRaises(TypeError):
            self.list.extend(None)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list.extend(self.list_length_1)
        self.list_length_1.extend(self.range_list)
        self.range_list.extend(self.list)
        self.list.extend(self.empty_list)

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, DoublyLinkedList([0]))
        self.assertEqual(self.list_length_1, DoublyLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.range_list,
                         DoublyLinkedList([0, 1, 2, 3, 1, 42, -3, 2, 42]))
        self.assertEqual(self.list, DoublyLinkedList([1, 42, -3, 2, 42, 0]))

        self.empty_list.extend([-1, -1])
        self.list_length_1.extend(tuple('list'))
        self.range_list.extend((-1, -2, -3))
        self.list.extend([])

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, DoublyLinkedList([0, -1, -1]))
        self.assertEqual(self.list_length_1,
                         DoublyLinkedList([0, 0, 1, 2, 3,
                                           'l', 'i', 's', 't']))
        self.assertEqual(self.range_list, DoublyLinkedList([0, 1, 2, 3,
                                                            1, 42, -3, 2, 42,
                                                            -1, -2, -3]))
        self.assertEqual(self.list, DoublyLinkedList([1, 42, -3, 2, 42, 0]))

    def test_repr(self):
        self.assertEqual(repr(self.empty_list), 'DoublyLinkedList([])')
        self.assertEqual(repr(self.list_length_1), 'DoublyLinkedList([0])')
        self.assertEqual(repr(self.range_list),
                         'DoublyLinkedList([0, 1, 2, 3])')
        self.assertEqual(repr(self.list),
                         'DoublyLinkedList([1, 42, -3, 2, 42])')
        self.assertEqual(repr(DoublyLinkedList(range(10))),
                         'DoublyLinkedList([0, 1, 2, 3, 4, 5, ...])')

    def test_str(self):
        self.assertEqual(str(self.empty_list), '')
        self.assertEqual(str(self.list_length_1), '0')
        self.assertEqual(str(self.range_list),
                         '0 \u21c4 1 \u21c4 2 \u21c4 3')
        self.assertEqual(str(self.list),
                         '1 \u21c4 42 \u21c4 -3 \u21c4 2 \u21c4 42')
        self.assertEqual(str(DoublyLinkedList(range(10))),
                         '0 \u21c4 1 \u21c4 2 \u21c4 3 \u21c4 4 \u21c4 '
                         '5 \u21c4 6 \u21c4 7 \u21c4 8 \u21c4 9')

    def test_is_empty(self):
        self.assertTrue(self.empty_list.is_empty())
        self.assertFalse(self.list_length_1.is_empty())
        self.assertFalse(self.range_list.is_empty())
        self.assertFalse(self.list.is_empty())

    def test_index(self):
        self.assertEqual(self.list_length_1.index(0), 0)
        self.assertEqual(self.range_list.index(0), 0)
        self.assertEqual(self.range_list.index(1), 1)
        self.assertEqual(self.range_list.index(2), 2)
        self.assertEqual(self.range_list.index(3), 3)
        self.assertEqual(self.list.index(1), 0)
        self.assertEqual(self.list.index(42), 1)
        self.assertEqual(self.list.index(-3), 2)
        self.assertEqual(self.list.index(2), 3)
        self.assertEqual(self.list.index(42, 2), 4)

        with self.assertRaises(ValueError):
            self.empty_list.index(0)
        with self.assertRaises(ValueError):
            self.list_length_1.index(1)
        with self.assertRaises(ValueError):
            self.range_list.index(-1)
        with self.assertRaises(ValueError):
            self.range_list.index(4)
        with self.assertRaises(ValueError):
            self.range_list.index(0, 1)
        with self.assertRaises(ValueError):
            self.range_list.index(1, 2, 4)
        with self.assertRaises(ValueError):
            self.list.index(41)
        with self.assertRaises(ValueError):
            self.range_list.index(42, 2, 4)

    def test_insert_after(self):
        with self.assertRaises(IndexError):
            self.empty_list.insert_after(0, 0)
        with self.assertRaises(IndexError):
            self.list_length_1.insert_after(-2, 0)
        with self.assertRaises(IndexError):
            self.list_length_1.insert_after(1, 0)
        with self.assertRaises(IndexError):
            self.range_list.insert_after(-5, 0)
        with self.assertRaises(IndexError):
            self.range_list.insert_after(4, 0)
        with self.assertRaises(IndexError):
            self.list.insert_after(-6, 0)
        with self.assertRaises(IndexError):
            self.list.insert_after(5, 0)

        self.list_length_1.insert_after(0, 1)
        self.list_length_1.insert_after(-1, 2)
        self.range_list.insert_after(0, 3)
        self.range_list.insert_after(-1, -1)
        self.range_list.insert_after(-5, 42)
        self.list.insert_after(0, 3)
        self.list.insert_after(-1, -1)
        self.list.insert_after(-5, 42)

        self.assertEqual(self.list_length_1, DoublyLinkedList([0, 1, 2]))
        self.assertEqual(self.range_list,
                         DoublyLinkedList([0, 3, 42, 1, 2, 3, -1]))
        self.assertEqual(self.list,
                         DoublyLinkedList([1, 3, 42, 42, -3, 2, 42, -1]))

    def test_insert_before(self):
        with self.assertRaises(IndexError):
            self.empty_list.insert_before(0, 0)
        with self.assertRaises(IndexError):
            self.list_length_1.insert_before(-2, 0)
        with self.assertRaises(IndexError):
            self.list_length_1.insert_before(1, 0)
        with self.assertRaises(IndexError):
            self.range_list.insert_before(-5, 0)
        with self.assertRaises(IndexError):
            self.range_list.insert_before(4, 0)
        with self.assertRaises(IndexError):
            self.list.insert_before(-6, 0)
        with self.assertRaises(IndexError):
            self.list.insert_before(5, 0)

        self.list_length_1.insert_before(0, 1)
        self.list_length_1.insert_before(-1, 2)
        self.range_list.insert_before(0, 3)
        self.range_list.insert_before(-1, -1)
        self.range_list.insert_before(-5, 42)
        self.list.insert_before(0, 3)
        self.list.insert_before(-1, -1)
        self.list.insert_before(-5, 42)

        self.assertEqual(self.list_length_1,
                         DoublyLinkedList([1, 2, 0]))
        self.assertEqual(self.range_list,
                         DoublyLinkedList([3, 42, 0, 1, 2, -1, 3]))
        self.assertEqual(self.list,
                         DoublyLinkedList([3, 1, 42, 42, -3, 2, -1, 42]))

    def test_insert(self):
        with self.assertRaises(IndexError):
            self.empty_list.insert(0, 0)
        with self.assertRaises(IndexError):
            self.list_length_1.insert(-2, 0)
        with self.assertRaises(IndexError):
            self.list_length_1.insert(1, 0)
        with self.assertRaises(IndexError):
            self.range_list.insert(-5, 0)
        with self.assertRaises(IndexError):
            self.range_list.insert(4, 0)
        with self.assertRaises(IndexError):
            self.list.insert(-6, 0)
        with self.assertRaises(IndexError):
            self.list.insert(5, 0)

        self.list_length_1.insert(0, 1)
        self.list_length_1.insert(-1, 2)
        self.range_list.insert(0, 3)
        self.range_list.insert(-1, -1)
        self.range_list.insert(-5, 42)
        self.list.insert(0, 3)
        self.list.insert(-1, -1)
        self.list.insert(-5, 42)

        self.assertEqual(self.list_length_1, DoublyLinkedList([1, 2, 0]))
        self.assertEqual(self.range_list,
                         DoublyLinkedList([3, 42, 0, 1, 2, -1, 3]))
        self.assertEqual(self.list,
                         DoublyLinkedList([3, 1, 42, 42, -3, 2, -1, 42]))

    def test_prepend(self):
        self.empty_list.prepend(-1)
        self.list_length_1.prepend(-1)
        self.list_length_1.prepend(-2)
        self.range_list.prepend(-1)
        self.range_list.prepend(-2)
        self.range_list.prepend(-3)
        self.list.prepend(-1)
        self.list.prepend(-2)
        self.list.prepend(-3)

        self.assertEqual(self.empty_list, DoublyLinkedList([-1]))
        self.assertEqual(self.list_length_1, DoublyLinkedList([-2, -1, 0]))
        self.assertEqual(self.range_list,
                         DoublyLinkedList([-3, -2, -1, 0, 1, 2, 3]))
        self.assertEqual(self.list,
                         DoublyLinkedList([-3, -2, -1, 1, 42, -3, 2, 42]))

    def test_append(self):
        self.empty_list.append(-1)
        self.list_length_1.append(-1)
        self.list_length_1.append(-2)
        self.range_list.append(-1)
        self.range_list.append(-2)
        self.range_list.append(-3)
        self.list.append(-1)
        self.list.append(-2)
        self.list.append(-3)

        self.assertEqual(self.empty_list, DoublyLinkedList([-1]))
        self.assertEqual(self.list_length_1, DoublyLinkedList([0, -1, -2]))
        self.assertEqual(self.range_list,
                         DoublyLinkedList([0, 1, 2, 3, -1, -2, -3]))
        self.assertEqual(self.list,
                         DoublyLinkedList([1, 42, -3, 2, 42, -1, -2, -3]))

    def test_reverse(self):
        self.empty_list.reverse()
        self.list_length_1.reverse()
        self.range_list.reverse()
        self.list.reverse()

        self.assertEqual(self.empty_list, DoublyLinkedList())
        self.assertEqual(self.list_length_1, DoublyLinkedList([0]))
        self.assertEqual(self.range_list, DoublyLinkedList([3, 2, 1, 0]))
        self.assertEqual(self.list, DoublyLinkedList([42, 2, -3, 42, 1]))

    def test_pop(self):
        with self.assertRaises(IndexError):
            self.empty_list.pop()
        with self.assertRaises(IndexError):
            self.list_length_1.pop(index=-2)
        with self.assertRaises(IndexError):
            self.list_length_1.pop(index=1)
        with self.assertRaises(IndexError):
            self.range_list.pop(index=-5)
        with self.assertRaises(IndexError):
            self.range_list.pop(index=4)
        with self.assertRaises(IndexError):
            self.list.pop(index=-6)
        with self.assertRaises(IndexError):
            self.list.pop(index=5)

        self.list_length_1.pop()
        self.range_list.pop(index=2)
        self.range_list.pop()
        self.list.pop(index=1)
        self.list.pop(index=3)

        self.assertEqual(self.list_length_1, DoublyLinkedList())
        self.assertEqual(self.range_list, DoublyLinkedList([0, 1]))
        self.assertEqual(self.list, DoublyLinkedList([1, -3, 2]))

        self.list.pop()
        self.list.pop()
        self.list.pop()
        with self.assertRaises(IndexError):
            self.list.pop()

    def test_remove_first(self):
        with self.assertRaises(ValueError):
            self.empty_list.remove_first(-1)
        with self.assertRaises(ValueError):
            self.list_length_1.remove_first(-1)
        with self.assertRaises(ValueError):
            self.range_list.remove_first(-1)
        with self.assertRaises(ValueError):
            self.list.remove_first(-1)

        self.list_length_1.remove_first(0)
        self.range_list.remove_first(1)
        self.range_list.remove_first(3)
        self.range_list.remove_first(0)
        self.list.remove_first(42)

        self.assertEqual(self.list_length_1, DoublyLinkedList())
        self.assertEqual(self.range_list, DoublyLinkedList([2]))
        self.assertEqual(self.list, DoublyLinkedList([1, -3, 2, 42]))

        with self.assertRaises(ValueError):
            self.range_list.remove_first(1)
        self.list.remove_first(42)
        with self.assertRaises(ValueError):
            self.list.remove_first(42)

    def test_remove(self):
        with self.assertRaises(ValueError):
            self.empty_list.remove(-1)
        with self.assertRaises(ValueError):
            self.list_length_1.remove(-1)
        with self.assertRaises(ValueError):
            self.range_list.remove(-1)
        with self.assertRaises(ValueError):
            self.list.remove(-1)

        self.list_length_1.remove(0)
        self.range_list.remove(1)
        self.range_list.remove(3)
        self.range_list.remove(0)
        self.list.remove(42)

        self.assertEqual(self.list_length_1, DoublyLinkedList())
        self.assertEqual(self.range_list, DoublyLinkedList([2]))
        self.assertEqual(self.list, DoublyLinkedList([1, -3, 2, 42]))

        with self.assertRaises(ValueError):
            self.range_list.remove(1)
        self.list.remove(42)
        with self.assertRaises(ValueError):
            self.list.remove(42)

    def test_remove_last(self):
        with self.assertRaises(ValueError):
            self.empty_list.remove_last(-1)
        with self.assertRaises(ValueError):
            self.list_length_1.remove_last(-1)
        with self.assertRaises(ValueError):
            self.range_list.remove_last(-1)
        with self.assertRaises(ValueError):
            self.list.remove_last(-1)

        self.list_length_1.remove_last(0)
        self.range_list.remove_last(1)
        self.range_list.remove_last(3)
        self.range_list.remove_last(0)
        self.list.remove_last(42)

        self.assertEqual(self.list_length_1, DoublyLinkedList())
        self.assertEqual(self.range_list, DoublyLinkedList([2]))
        self.assertEqual(self.list, DoublyLinkedList([1, 42, -3, 2]))

        with self.assertRaises(ValueError):
            self.range_list.remove_last(1)
        self.list.remove_last(42)
        with self.assertRaises(ValueError):
            self.list.remove_last(42)


class TestCircularDoublyLinkedListNode(unittest.TestCase):
    def setUp(self):
        self.node1 = CircularDoublyLinkedList.Node(1)
        self.node2 = CircularDoublyLinkedList.Node(2, predecessor=self.node1)
        self.node1.successor = self.node2
        self.node3 = CircularDoublyLinkedList.Node(3, predecessor=self.node2)
        self.node2.successor = self.node3

    def test_init(self):
        self.assertEqual(self.node1.value, 1)
        self.assertEqual(self.node1.predecessor, None)
        self.assertEqual(self.node1.successor, self.node2)
        self.assertEqual(self.node2.value, 2)
        self.assertEqual(self.node2.predecessor, self.node1)
        self.assertEqual(self.node2.successor, self.node3)
        self.assertEqual(self.node3.value, 3)
        self.assertEqual(self.node3.predecessor, self.node2)
        self.assertEqual(self.node3.successor, None)

    def test_node_repr(self):
        self.assertEqual(repr(self.node1), '1')
        self.assertEqual(repr(self.node2), '2')
        self.assertEqual(repr(self.node3), '3')

    def test_node_str(self):
        self.assertEqual(str(self.node1), '1')
        self.assertEqual(str(self.node2), '2')
        self.assertEqual(str(self.node3), '3')


class TestCircularDoublyLinkedList(unittest.TestCase):
    def setUp(self):
        self.empty_list = CircularDoublyLinkedList()
        self.list_length_1 = CircularDoublyLinkedList([0])
        self.range_list = CircularDoublyLinkedList(range(4))
        self.list = CircularDoublyLinkedList([1, 42, -3, 2, 42])

    def test_init(self):
        # testing empty linked list
        self.assertEqual(self.empty_list._head, None)
        self.assertEqual(self.empty_list._len, 0)
        # testing linked list of length 1
        self.assertEqual(self.list_length_1._head.value, 0)
        self.assertEqual(self.list_length_1._head.predecessor,
                         self.list_length_1._head)
        self.assertEqual(self.list_length_1._head.successor,
                         self.list_length_1._head)
        self.assertEqual(self.list_length_1._len, 1)
        # testing linked list constructed by range
        self.assertEqual(self.range_list._head.value, 0)
        self.assertEqual(self.range_list._head.predecessor.value, 3)
        self.assertEqual(self.range_list._head.successor.value, 1)
        self.assertEqual(self.range_list._head.successor.predecessor.value, 0)
        self.assertEqual(self.range_list._head.successor.successor.value, 2)
        self.assertEqual(self.range_list._head.successor.successor.predecessor
                         .value, 1)
        self.assertEqual(self.range_list._head.successor.successor.successor
                         .value, 3)
        self.assertEqual(self.range_list._head.successor.successor.successor
                         .predecessor.value, 2)
        self.assertEqual(self.range_list._head.successor.successor.successor
                         .successor, self.range_list._head)
        self.assertEqual(self.range_list._len, 4)
        # testing linked list constructed by list
        self.assertEqual(self.list._head.value, 1)
        self.assertEqual(self.list._head.predecessor.value, 42)
        self.assertEqual(self.list._head.successor.value, 42)
        self.assertEqual(self.list._head.successor.predecessor.value, 1)
        self.assertEqual(self.list._head.successor.successor.value, -3)
        self.assertEqual(self.list._head.successor.successor.predecessor.value,
                         42)
        self.assertEqual(self.list._head.successor.successor.successor.value, 2)
        self.assertEqual(self.list._head.successor.successor.successor
                         .predecessor.value, -3)
        self.assertEqual(self.list._head.successor.successor.successor
                         .successor.value, 42)
        self.assertEqual(self.list._head.successor.successor.successor
                         .successor.predecessor.value, 2)
        self.assertEqual(self.list._head.successor.successor.successor
                         .successor.successor, self.list._head)
        self.assertEqual(self.list._len, 5)

    def test_bool(self):
        self.assertFalse(bool(self.empty_list))
        self.assertTrue(bool(self.list_length_1))
        self.assertTrue(bool(self.range_list))
        self.assertTrue(bool(self.list))

    def test_iter(self):
        self.assertEqual(list(iter(self.empty_list)), [])
        self.assertEqual(list(iter(self.list_length_1)), [0])
        self.assertEqual(list(iter(self.range_list)), list(range(4)))
        self.assertEqual(list(iter(self.list)), [1, 42, -3, 2, 42])

    def test_reversed(self):
        self.assertEqual(list(reversed(self.empty_list)), [])
        self.assertEqual(list(reversed(self.list_length_1)), [0])
        self.assertEqual(list(reversed(self.range_list)), [3, 2, 1, 0])
        self.assertEqual(list(reversed(self.list)), [42, 2, -3, 42, 1])

    def test_get_item(self):
        self.assertEqual(self.list_length_1[-2], 0)
        self.assertEqual(self.list_length_1[-1], 0)
        self.assertEqual(self.list_length_1[0], 0)
        self.assertEqual(self.list_length_1[1], 0)
        self.assertEqual(self.range_list[-8], 0)
        self.assertEqual(self.range_list[-7], 1)
        self.assertEqual(self.range_list[-6], 2)
        self.assertEqual(self.range_list[-5], 3)
        self.assertEqual(self.range_list[-4], 0)
        self.assertEqual(self.range_list[-3], 1)
        self.assertEqual(self.range_list[-2], 2)
        self.assertEqual(self.range_list[-1], 3)
        self.assertEqual(self.range_list[0], 0)
        self.assertEqual(self.range_list[1], 1)
        self.assertEqual(self.range_list[2], 2)
        self.assertEqual(self.range_list[3], 3)
        self.assertEqual(self.range_list[4], 0)
        self.assertEqual(self.range_list[5], 1)
        self.assertEqual(self.range_list[6], 2)
        self.assertEqual(self.range_list[7], 3)
        self.assertEqual(self.list[-10], 1)
        self.assertEqual(self.list[-9], 42)
        self.assertEqual(self.list[-8], -3)
        self.assertEqual(self.list[-7], 2)
        self.assertEqual(self.list[-6], 42)
        self.assertEqual(self.list[-5], 1)
        self.assertEqual(self.list[-4], 42)
        self.assertEqual(self.list[-3], -3)
        self.assertEqual(self.list[-2], 2)
        self.assertEqual(self.list[-1], 42)
        self.assertEqual(self.list[0], 1)
        self.assertEqual(self.list[1], 42)
        self.assertEqual(self.list[2], -3)
        self.assertEqual(self.list[3], 2)
        self.assertEqual(self.list[4], 42)
        self.assertEqual(self.list[5], 1)
        self.assertEqual(self.list[6], 42)
        self.assertEqual(self.list[7], -3)
        self.assertEqual(self.list[8], 2)
        self.assertEqual(self.list[9], 42)

        with self.assertRaises(IndexError):
            self.empty_list[0]

    def test_set_item(self):
        self.list_length_1[-2] = 1
        self.assertEqual(self.list_length_1[0], 1)

        self.range_list[0] = 1
        self.range_list[1] = 2
        self.range_list[2] = 3
        self.range_list[3] = 4
        self.assertEqual(self.range_list[0], 1)
        self.assertEqual(self.range_list[1], 2)
        self.assertEqual(self.range_list[2], 3)
        self.assertEqual(self.range_list[3], 4)

        self.list[-25] = 'l'
        self.list[-19] = 'l'
        self.list[-13] = 'i'
        self.list[8] = 's'
        self.list[14] = 't'
        self.assertEqual(self.list[0], 'l')
        self.assertEqual(self.list[1], 'l')
        self.assertEqual(self.list[2], 'i')
        self.assertEqual(self.list[3], 's')
        self.assertEqual(self.list[4], 't')

        with self.assertRaises(IndexError):
            self.empty_list[0] = 0

    def test_del_item(self):
        with self.assertRaises(IndexError):
            del self.empty_list[0]

        del self.list_length_1[0]
        self.assertEqual(self.list_length_1._head, None)
        self.assertEqual(self.list_length_1._len, 0)

        del self.range_list[1]
        self.assertEqual(self.range_list._head.value, 0)
        self.assertEqual(self.range_list._len, 3)
        self.assertEqual(self.range_list[0], 0)
        self.assertEqual(self.range_list[1], 2)
        self.assertEqual(self.range_list[2], 3)

        del self.range_list[0]
        self.assertEqual(self.range_list._head.value, 2)
        self.assertEqual(self.range_list._len, 2)
        self.assertEqual(self.range_list[0], 2)
        self.assertEqual(self.range_list[1], 3)

        del self.range_list[-1]
        self.assertEqual(self.range_list._head.value, 2)
        self.assertEqual(self.range_list._len, 1)
        self.assertEqual(self.range_list[0], 2)

    def test_len(self):
        self.assertEqual(len(self.empty_list), 0)
        self.assertEqual(len(self.list_length_1), 1)
        self.assertEqual(len(self.range_list), 4)
        self.assertEqual(len(self.list), 5)

    def test_eq(self):
        self.assertEqual(self.empty_list, CircularDoublyLinkedList())
        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList(range(1)))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.list,
                         CircularDoublyLinkedList((1, 42, -3, 2, 42)))
        self.assertNotEqual(self.empty_list, self.list_length_1)
        self.assertNotEqual(self.list_length_1, self.range_list)
        self.assertNotEqual(self.range_list, self.list)
        self.assertNotEqual(self.list, self.empty_list)
        self.assertNotEqual(self.empty_list, [])
        self.assertNotEqual(self.list_length_1, [0])
        self.assertNotEqual(self.range_list, range(4))
        self.assertNotEqual(self.list, [1, 42, -3, 2, 42])

    def test_add(self):
        with self.assertRaises(TypeError):
            self.empty_list + []
        with self.assertRaises(TypeError):
            self.list_length_1 + [1]
        with self.assertRaises(TypeError):
            self.range_list + [2, 3]
        with self.assertRaises(TypeError):
            self.list + ['a', 'b', 'c']

        self.assertEqual(self.empty_list + self.empty_list,
                         CircularDoublyLinkedList())
        self.assertEqual(self.empty_list + self.list_length_1,
                         CircularDoublyLinkedList([0]))
        self.assertEqual(self.empty_list + self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.empty_list + self.list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(self.list_length_1 + self.empty_list,
                         CircularDoublyLinkedList([0]))
        self.assertEqual(self.list_length_1 + self.list_length_1,
                         CircularDoublyLinkedList([0, 0]))
        self.assertEqual(self.list_length_1 + self.range_list,
                         CircularDoublyLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.list_length_1 + self.list,
                         CircularDoublyLinkedList([0, 1, 42, -3, 2, 42]))
        self.assertEqual(self.range_list + self.empty_list,
                         CircularDoublyLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.range_list + self.list_length_1,
                         CircularDoublyLinkedList([0, 1, 2, 3, 0]))
        self.assertEqual(self.range_list + self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(self.range_list + self.list,
                         CircularDoublyLinkedList([0, 1, 2, 3,
                                                   1, 42, -3, 2, 42]))
        self.assertEqual(self.list + self.empty_list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(self.list + self.list_length_1,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42, 0]))
        self.assertEqual(self.list + self.range_list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42,
                                                   0, 1, 2, 3]))
        self.assertEqual(self.list + self.list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42,
                                                   1, 42, -3, 2, 42]))

    def test_iadd(self):
        with self.assertRaises(TypeError):
            self.empty_list += 2
        with self.assertRaises(TypeError):
            self.list_length_1 += 2.5
        with self.assertRaises(TypeError):
            self.range_list += True
        with self.assertRaises(TypeError):
            self.list += None

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list += self.list_length_1
        self.list_length_1 += self.range_list
        self.range_list += self.list
        self.list += self.empty_list

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularDoublyLinkedList([0]))
        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3,
                                                   1, 42, -3, 2, 42]))
        self.assertEqual(self.list, CircularDoublyLinkedList([1, 42, -3, 2, 42,
                                                              0]))

        self.empty_list += [-1, -1]
        self.list_length_1 += tuple('list')
        self.range_list += (-1, -2, -3)
        self.list += []

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list,
                         CircularDoublyLinkedList([0, -1, -1]))
        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([0, 0, 1, 2, 3,
                                                   'l', 'i', 's', 't']))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3,
                                                   1, 42, -3, 2, 42,
                                                   -1, -2, -3]))
        self.assertEqual(self.list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42, 0]))

    def test_mul(self):
        with self.assertRaises(TypeError):
            self.empty_list * []
        with self.assertRaises(TypeError):
            self.list_length_1 * 3.5
        with self.assertRaises(TypeError):
            self.range_list * (2, 3)
        with self.assertRaises(TypeError):
            self.list * BasicLinkedList(['a', 'b', 'c'])

        with self.assertRaises(ValueError):
            self.empty_list * (-1)
        with self.assertRaises(ValueError):
            self.list_length_1 * (-2)
        with self.assertRaises(ValueError):
            self.range_list * (-3)
        with self.assertRaises(ValueError):
            self.list * (-4)

        self.assertEqual(self.empty_list * 0, CircularDoublyLinkedList())
        self.assertEqual(self.empty_list * 1, CircularDoublyLinkedList())
        self.assertEqual(self.empty_list * 2, CircularDoublyLinkedList())
        self.assertEqual(self.empty_list * 3, CircularDoublyLinkedList())
        self.assertEqual(self.list_length_1 * 0, CircularDoublyLinkedList())
        self.assertEqual(self.list_length_1 * 1, CircularDoublyLinkedList([0]))
        self.assertEqual(self.list_length_1 * 2,
                         CircularDoublyLinkedList([0, 0]))
        self.assertEqual(self.list_length_1 * 3,
                         CircularDoublyLinkedList([0, 0, 0]))
        self.assertEqual(self.range_list * 0, CircularDoublyLinkedList())
        self.assertEqual(self.range_list * 1,
                         CircularDoublyLinkedList([0, 1, 2, 3]))
        self.assertEqual(self.range_list * 2,
                         CircularDoublyLinkedList([0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(self.range_list * 3,
                         CircularDoublyLinkedList([0, 1, 2, 3, 0, 1, 2, 3,
                                                   0, 1, 2, 3]))
        self.assertEqual(self.list * 0, CircularDoublyLinkedList())
        self.assertEqual(self.list * 1,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(self.list * 2,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42,
                                                   1, 42, -3, 2, 42]))
        self.assertEqual(self.list * 3,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42,
                                                   1, 42, -3, 2, 42,
                                                   1, 42, -3, 2, 42]))

    def test_imul(self):
        with self.assertRaises(TypeError):
            self.empty_list *= []
        with self.assertRaises(TypeError):
            self.list_length_1 *= 3.5
        with self.assertRaises(TypeError):
            self.range_list *= (2, 3)
        with self.assertRaises(TypeError):
            self.list *= BasicLinkedList(['a', 'b', 'c'])

        with self.assertRaises(ValueError):
            self.empty_list *= (-1)
        with self.assertRaises(ValueError):
            self.list_length_1 *= (-2)
        with self.assertRaises(ValueError):
            self.range_list *= (-3)
        with self.assertRaises(ValueError):
            self.list *= (-4)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list *= 2
        self.list_length_1 *= 3
        self.range_list *= 0
        self.list *= 1

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularDoublyLinkedList())
        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([0, 0, 0]))
        self.assertEqual(self.range_list, CircularDoublyLinkedList())
        self.assertEqual(self.list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42]))

    def test_rmul(self):
        with self.assertRaises(TypeError):
            [] * self.empty_list
        with self.assertRaises(TypeError):
            3.5 * self.list_length_1
        with self.assertRaises(TypeError):
            (2, 3) * self.range_list
        with self.assertRaises(TypeError):
            BasicLinkedList(['a', 'b', 'c']) * self.list

        with self.assertRaises(ValueError):
            (-1) * self.empty_list
        with self.assertRaises(ValueError):
            (-2) * self.list_length_1
        with self.assertRaises(ValueError):
            (-3) * self.range_list
        with self.assertRaises(ValueError):
            (-4) * self.list

        self.assertEqual(0 * self.empty_list, CircularDoublyLinkedList())
        self.assertEqual(1 * self.empty_list, CircularDoublyLinkedList())
        self.assertEqual(2 * self.empty_list, CircularDoublyLinkedList())
        self.assertEqual(3 * self.empty_list, CircularDoublyLinkedList())
        self.assertEqual(0 * self.list_length_1, CircularDoublyLinkedList())
        self.assertEqual(1 * self.list_length_1, CircularDoublyLinkedList([0]))
        self.assertEqual(2 * self.list_length_1,
                         CircularDoublyLinkedList([0, 0]))
        self.assertEqual(3 * self.list_length_1,
                         CircularDoublyLinkedList([0, 0, 0]))
        self.assertEqual(0 * self.range_list, CircularDoublyLinkedList())
        self.assertEqual(1 * self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3]))
        self.assertEqual(2 * self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3, 0, 1, 2, 3]))
        self.assertEqual(3 * self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3, 0, 1, 2, 3,
                                                   0, 1, 2, 3]))
        self.assertEqual(0 * self.list, CircularDoublyLinkedList())
        self.assertEqual(1 * self.list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42]))
        self.assertEqual(2 * self.list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42,
                                                   1, 42, -3, 2, 42]))
        self.assertEqual(3 * self.list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42,
                                                   1, 42, -3, 2, 42,
                                                   1, 42, -3, 2, 42]))

    def test_extend_by_prepending(self):
        with self.assertRaises(TypeError):
            self.empty_list.extend_by_prepending(2)
        with self.assertRaises(TypeError):
            self.list_length_1.extend_by_prepending(2.5)
        with self.assertRaises(TypeError):
            self.range_list.extend_by_prepending(True)
        with self.assertRaises(TypeError):
            self.list.extend_by_prepending(None)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list.extend_by_prepending(self.list_length_1)
        self.list_length_1.extend_by_prepending(self.range_list)
        self.range_list.extend_by_prepending(self.list)
        self.list.extend_by_prepending(self.empty_list)

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularDoublyLinkedList([0]))
        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([0, 1, 2, 3, 0]))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42,
                                                   0, 1, 2, 3]))
        self.assertEqual(self.list,
                         CircularDoublyLinkedList([0, 1, 42, -3, 2, 42]))

        self.empty_list.extend_by_prepending([-1, -1])
        self.list_length_1.extend_by_prepending(tuple('list'))
        self.range_list.extend_by_prepending((-1, -2, -3))
        self.list.extend_by_prepending([])

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list,
                         CircularDoublyLinkedList([-1, -1, 0]))
        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList(['l', 'i', 's', 't',
                                                   0, 1, 2, 3, 0]))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([-1, -2, -3,
                                                   1, 42, -3, 2, 42,
                                                   0, 1, 2, 3]))
        self.assertEqual(self.list,
                         CircularDoublyLinkedList([0, 1, 42, -3, 2, 42]))

    def test_extend_by_appending(self):
        with self.assertRaises(TypeError):
            self.empty_list.extend_by_appending(2)
        with self.assertRaises(TypeError):
            self.list_length_1.extend_by_appending(2.5)
        with self.assertRaises(TypeError):
            self.range_list.extend_by_appending(True)
        with self.assertRaises(TypeError):
            self.list.extend_by_appending(None)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list.extend_by_appending(self.list_length_1)
        self.list_length_1.extend_by_appending(self.range_list)
        self.range_list.extend_by_appending(self.list)
        self.list.extend_by_appending(self.empty_list)

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularDoublyLinkedList([0]))
        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3,
                                                   1, 42, -3, 2, 42]))
        self.assertEqual(self.list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42, 0]))

        self.empty_list.extend_by_appending([-1, -1])
        self.list_length_1.extend_by_appending(tuple('list'))
        self.range_list.extend_by_appending((-1, -2, -3))
        self.list.extend_by_appending([])

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list,
                         CircularDoublyLinkedList([0, -1, -1]))
        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([0, 0, 1, 2, 3,
                                                   'l', 'i', 's', 't']))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3,
                                                   1, 42, -3, 2, 42,
                                                   -1, -2, -3]))
        self.assertEqual(self.list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42, 0]))

    def test_extend(self):
        with self.assertRaises(TypeError):
            self.empty_list.extend(2)
        with self.assertRaises(TypeError):
            self.list_length_1.extend(2.5)
        with self.assertRaises(TypeError):
            self.range_list.extend(True)
        with self.assertRaises(TypeError):
            self.list.extend(None)

        id_empty_list = id(self.empty_list)
        id_list_length_1 = id(self.list_length_1)
        id_range_list = id(self.range_list)
        id_list = id(self.list)

        self.empty_list.extend(self.list_length_1)
        self.list_length_1.extend(self.range_list)
        self.range_list.extend(self.list)
        self.list.extend(self.empty_list)

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list, CircularDoublyLinkedList([0]))
        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([0, 0, 1, 2, 3]))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3,
                                                   1, 42, -3, 2, 42]))
        self.assertEqual(self.list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42, 0]))

        self.empty_list.extend([-1, -1])
        self.list_length_1.extend(tuple('list'))
        self.range_list.extend((-1, -2, -3))
        self.list.extend([])

        self.assertEqual(id(self.empty_list), id_empty_list)
        self.assertEqual(id(self.list_length_1), id_list_length_1)
        self.assertEqual(id(self.range_list), id_range_list)
        self.assertEqual(id(self.list), id_list)
        self.assertEqual(self.empty_list,
                         CircularDoublyLinkedList([0, -1, -1]))
        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([0, 0, 1, 2, 3,
                                                   'l', 'i', 's', 't']))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3,
                                                   1, 42, -3, 2, 42,
                                                   -1, -2, -3]))
        self.assertEqual(self.list,
                         CircularDoublyLinkedList([1, 42, -3, 2, 42, 0]))

    def test_repr(self):
        self.assertEqual(repr(self.empty_list), 'CircularDoublyLinkedList([])')
        self.assertEqual(repr(self.list_length_1),
                         'CircularDoublyLinkedList([0])')
        self.assertEqual(repr(self.range_list),
                         'CircularDoublyLinkedList([0, 1, 2, 3])')
        self.assertEqual(repr(self.list),
                         'CircularDoublyLinkedList([1, 42, -3, 2, 42])')
        self.assertEqual(repr(CircularDoublyLinkedList(range(10))),
                         'CircularDoublyLinkedList([0, 1, 2, 3, 4, 5, ...])')

    def test_str(self):
        self.assertEqual(str(self.empty_list), '')
        self.assertEqual(str(self.list_length_1), '0 \u21c4')
        self.assertEqual(str(self.range_list),
                         '0 \u21c4 1 \u21c4 2 \u21c4 3 \u21c4')
        self.assertEqual(str(self.list),
                         '1 \u21c4 42 \u21c4 -3 \u21c4 2 \u21c4 42 \u21c4')
        self.assertEqual(str(CircularDoublyLinkedList(range(10))),
                         '0 \u21c4 1 \u21c4 2 \u21c4 3 \u21c4 4 \u21c4 '
                         '5 \u21c4 6 \u21c4 7 \u21c4 8 \u21c4 9 \u21c4')

    def test_is_empty(self):
        self.assertTrue(self.empty_list.is_empty())
        self.assertFalse(self.list_length_1.is_empty())
        self.assertFalse(self.range_list.is_empty())
        self.assertFalse(self.list.is_empty())

    def test_index(self):
        self.assertEqual(self.list_length_1.index(0), 0)
        self.assertEqual(self.range_list.index(0), 0)
        self.assertEqual(self.range_list.index(1), 1)
        self.assertEqual(self.range_list.index(2), 2)
        self.assertEqual(self.range_list.index(3), 3)
        self.assertEqual(self.list.index(1), 0)
        self.assertEqual(self.list.index(42), 1)
        self.assertEqual(self.list.index(-3), 2)
        self.assertEqual(self.list.index(2), 3)
        self.assertEqual(self.list.index(42, 2), 4)

        with self.assertRaises(ValueError):
            self.empty_list.index(0)
        with self.assertRaises(ValueError):
            self.list_length_1.index(1)
        with self.assertRaises(ValueError):
            self.range_list.index(-1)
        with self.assertRaises(ValueError):
            self.range_list.index(4)
        with self.assertRaises(ValueError):
            self.range_list.index(0, 1)
        with self.assertRaises(ValueError):
            self.range_list.index(1, 2, 4)
        with self.assertRaises(ValueError):
            self.list.index(41)
        with self.assertRaises(ValueError):
            self.range_list.index(42, 2, 4)

    def test_insert_after(self):
        with self.assertRaises(IndexError):
            self.empty_list.insert_after(0, 0)

        self.list_length_1.insert_after(0, 1)
        self.list_length_1.insert_after(-1, 2)
        self.range_list.insert_after(0, 3)
        self.range_list.insert_after(-1, -1)
        self.range_list.insert_after(-5, 42)
        self.list.insert_after(0, 3)
        self.list.insert_after(-1, -1)
        self.list.insert_after(-5, 42)

        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([0, 1, 2]))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([0, 3, 42, 1, 2, 3, -1]))
        self.assertEqual(self.list, CircularDoublyLinkedList([1, 3, 42, 42, -3,
                                                              2, 42, -1]))

    def test_insert_before(self):
        with self.assertRaises(IndexError):
            self.empty_list.insert_before(0, 0)

        self.list_length_1.insert_before(0, 1)
        self.list_length_1.insert_before(-1, 2)
        self.range_list.insert_before(0, 3)
        self.range_list.insert_before(-1, -1)
        self.range_list.insert_before(-5, 42)
        self.list.insert_before(0, 3)
        self.list.insert_before(-1, -1)
        self.list.insert_before(-5, 42)

        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([1, 2, 0]))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([3, 42, 0, 1, 2, -1, 3]))
        self.assertEqual(self.list, CircularDoublyLinkedList([3, 1, 42, 42, -3,
                                                              2, -1, 42]))

    def test_insert(self):
        with self.assertRaises(IndexError):
            self.empty_list.insert(0, 0)

        self.list_length_1.insert(0, 1)
        self.list_length_1.insert(-1, 2)
        self.range_list.insert(0, 3)
        self.range_list.insert(-1, -1)
        self.range_list.insert(-5, 42)
        self.list.insert(0, 3)
        self.list.insert(-1, -1)
        self.list.insert(-5, 42)

        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([1, 2, 0]))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([3, 42, 0, 1, 2, -1, 3]))
        self.assertEqual(self.list, CircularDoublyLinkedList([3, 1, 42, 42, -3,
                                                              2, -1, 42]))

    def test_prepend(self):
        self.empty_list.prepend(-1)
        self.list_length_1.prepend(-1)
        self.list_length_1.prepend(-2)
        self.range_list.prepend(-1)
        self.range_list.prepend(-2)
        self.range_list.prepend(-3)
        self.list.prepend(-1)
        self.list.prepend(-2)
        self.list.prepend(-3)

        self.assertEqual(self.empty_list, CircularDoublyLinkedList([-1]))
        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([-2, -1, 0]))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([-3, -2, -1, 0, 1, 2, 3]))
        self.assertEqual(self.list, CircularDoublyLinkedList([-3, -2, -1, 1,
                                                              42, -3, 2, 42]))

    def test_append(self):
        self.empty_list.append(-1)
        self.list_length_1.append(-1)
        self.list_length_1.append(-2)
        self.range_list.append(-1)
        self.range_list.append(-2)
        self.range_list.append(-3)
        self.list.append(-1)
        self.list.append(-2)
        self.list.append(-3)

        self.assertEqual(self.empty_list, CircularDoublyLinkedList([-1]))
        self.assertEqual(self.list_length_1,
                         CircularDoublyLinkedList([0, -1, -2]))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([0, 1, 2, 3, -1, -2, -3]))
        self.assertEqual(self.list, CircularDoublyLinkedList([1, 42, -3, 2, 42,
                                                              -1, -2, -3]))

    def test_reverse(self):
        self.empty_list.reverse()
        self.list_length_1.reverse()
        self.range_list.reverse()
        self.list.reverse()

        self.assertEqual(self.empty_list, CircularDoublyLinkedList())
        self.assertEqual(self.list_length_1, CircularDoublyLinkedList([0]))
        self.assertEqual(self.range_list,
                         CircularDoublyLinkedList([3, 2, 1, 0]))
        self.assertEqual(self.list,
                         CircularDoublyLinkedList([42, 2, -3, 42, 1]))

    def test_pop(self):
        with self.assertRaises(IndexError):
            self.empty_list.pop()

        self.list_length_1.pop()
        self.range_list.pop(index=2)
        self.range_list.pop()
        self.list.pop(index=1)
        self.list.pop(index=3)

        self.assertEqual(self.list_length_1, CircularDoublyLinkedList())
        self.assertEqual(self.range_list, CircularDoublyLinkedList([0, 1]))
        self.assertEqual(self.list, CircularDoublyLinkedList([1, -3, 2]))

        self.list.pop()
        self.list.pop()
        self.list.pop()
        with self.assertRaises(IndexError):
            self.list.pop()

    def test_remove_first(self):
        with self.assertRaises(ValueError):
            self.empty_list.remove_first(-1)
        with self.assertRaises(ValueError):
            self.list_length_1.remove_first(-1)
        with self.assertRaises(ValueError):
            self.range_list.remove_first(-1)
        with self.assertRaises(ValueError):
            self.list.remove_first(-1)

        self.list_length_1.remove_first(0)
        self.range_list.remove_first(1)
        self.range_list.remove_first(3)
        self.range_list.remove_first(0)
        self.list.remove_first(42)

        self.assertEqual(self.list_length_1, CircularDoublyLinkedList())
        self.assertEqual(self.range_list, CircularDoublyLinkedList([2]))
        self.assertEqual(self.list, CircularDoublyLinkedList([1, -3, 2, 42]))

        with self.assertRaises(ValueError):
            self.range_list.remove_first(1)
        self.list.remove_first(42)
        with self.assertRaises(ValueError):
            self.list.remove_first(42)

    def test_remove(self):
        with self.assertRaises(ValueError):
            self.empty_list.remove(-1)
        with self.assertRaises(ValueError):
            self.list_length_1.remove(-1)
        with self.assertRaises(ValueError):
            self.range_list.remove(-1)
        with self.assertRaises(ValueError):
            self.list.remove(-1)

        self.list_length_1.remove(0)
        self.range_list.remove(1)
        self.range_list.remove(3)
        self.range_list.remove(0)
        self.list.remove(42)

        self.assertEqual(self.list_length_1, CircularDoublyLinkedList())
        self.assertEqual(self.range_list, CircularDoublyLinkedList([2]))
        self.assertEqual(self.list, CircularDoublyLinkedList([1, -3, 2, 42]))

        with self.assertRaises(ValueError):
            self.range_list.remove(1)
        self.list.remove(42)
        with self.assertRaises(ValueError):
            self.list.remove(42)

    def test_remove_last(self):
        with self.assertRaises(ValueError):
            self.empty_list.remove_last(-1)
        with self.assertRaises(ValueError):
            self.list_length_1.remove_last(-1)
        with self.assertRaises(ValueError):
            self.range_list.remove_last(-1)
        with self.assertRaises(ValueError):
            self.list.remove_last(-1)

        self.list_length_1.remove_last(0)
        self.range_list.remove_last(1)
        self.range_list.remove_last(3)
        self.range_list.remove_last(0)
        self.list.remove_last(42)

        self.assertEqual(self.list_length_1, CircularDoublyLinkedList())
        self.assertEqual(self.range_list, CircularDoublyLinkedList([2]))
        self.assertEqual(self.list, CircularDoublyLinkedList([1, 42, -3, 2]))

        with self.assertRaises(ValueError):
            self.range_list.remove_last(1)
        self.list.remove_last(42)
        with self.assertRaises(ValueError):
            self.list.remove_last(42)


if __name__ == '__main__':
    # suite = unittest.TestSuite()
    # # suite.addTest(TestDoublyLinkedList())
    # # suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestLinkedList)
    # test_loader = unittest.defaultTestLoader
    # test_names = test_loader.getTestCaseNames(testcase_klass)
    # suite = unittest.TestSuite()
    # for name in testnames:
    #     suite.addTest(testcase_klass(name, param=param))
    #
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    unittest.main()
