# Sebastian Thomas (datascience at sebastianthomas dot de)

# copying objects
from copy import copy

# unit tests
import unittest

# custom modules
from datastructures.dictionary import *


class TestDictionary(unittest.TestCase):
    def __new__(cls, method_name, tested_class=None):
        if cls is TestDictionary:
            raise TypeError('Class TestDictionary may not be instantiated.')
        return super().__new__(cls)

    def __init__(self, method_name, tested_class=None):
        super().__init__(methodName=method_name)
        self.tested_class = tested_class

    def setUp(self):
        self.empty_dictionary = self.tested_class()
        self.dictionary_length_1 = self.tested_class.from_dictionary({None: 0})
        self.range_dictionary = self.tested_class.from_iterable(
            zip(['a', 'b', 'c', 'd'], range(4)))
        self.dictionary = self.tested_class.from_iterable(
            enumerate([1, 42, -3, 2, 42]))

    def test_from_dictionary(self):
        self.assertEqual(self.empty_dictionary,
                         self.tested_class.from_dictionary({}))
        self.assertEqual(self.dictionary_length_1,
                         self.tested_class.from_dictionary({None: 0}))
        self.assertEqual(self.range_dictionary,
                         self.tested_class.from_dictionary(
                             {'a': 0, 'b': 1, 'c': 2, 'd': 3}))
        self.assertEqual(self.dictionary,
                         self.tested_class.from_dictionary(
                             {0: 1, 1: 42, 2: -3, 3: 2, 4: 42}))

    def test_from_iterable(self):
        self.assertEqual(self.empty_dictionary,
                         self.tested_class.from_iterable([]))
        self.assertEqual(self.dictionary_length_1,
                         self.tested_class.from_iterable([(None, 0)]))
        self.assertEqual(self.range_dictionary,
                         self.tested_class.from_iterable(
                             [('a', 0), ('b', 1), ('c', 2), ('d', 3)]))
        self.assertEqual(self.dictionary,
                         self.tested_class.from_iterable(
                             [(0, 1), (1, 42), (2, -3), (3, 2), (4, 42)]))

    def test_eq(self):
        self.assertEqual(self.empty_dictionary, self.tested_class())
        self.assertEqual(self.dictionary_length_1,
                         self.tested_class.from_iterable(
                             zip({None}, range(1))))
        self.assertEqual(self.range_dictionary,
                         self.tested_class.from_iterable(
                             {(char, idx) for idx, char
                              in enumerate(['a', 'b', 'c', 'd'])}))
        self.assertEqual(self.dictionary,
                         self.tested_class.from_iterable(
                             ((0, 1), (1, 42), (2, -3), (3, 2), (4, 42))))
        self.assertNotEqual(self.empty_dictionary, self.dictionary_length_1)
        self.assertNotEqual(self.dictionary_length_1, self.range_dictionary)
        self.assertNotEqual(self.range_dictionary, self.dictionary)
        self.assertNotEqual(self.dictionary, self.empty_dictionary)
        self.assertNotEqual(self.empty_dictionary, {})
        self.assertNotEqual(self.dictionary_length_1, {0: 0})
        self.assertNotEqual(self.range_dictionary,
                            {'a': 0, 'b': 1, 'c': 2, 'd': 3})
        self.assertNotEqual(self.dictionary, {0: 1, 1: 42, 2: -3, 3: 2, 4: 42})

    def test_copy(self):
        self.assertEqual(copy(self.empty_dictionary), self.empty_dictionary)
        self.assertEqual(copy(self.dictionary_length_1),
                         self.dictionary_length_1)
        self.assertEqual(copy(self.range_dictionary), self.range_dictionary)
        self.assertEqual(copy(self.dictionary), self.dictionary)

    def test_iter(self):
        self.assertEqual(list(iter(self.empty_dictionary)), [])
        self.assertEqual(list(iter(self.dictionary_length_1)), [None])
        self.assertEqual(list(iter(self.range_dictionary)),
                         ['a', 'b', 'c', 'd'])
        self.assertEqual(list(iter(self.dictionary)), [0, 1, 2, 3, 4])

    def test_bool(self):
        self.assertFalse(bool(self.empty_dictionary))
        self.assertTrue(bool(self.dictionary_length_1))
        self.assertTrue(bool(self.range_dictionary))
        self.assertTrue(bool(self.dictionary))

    def test_len(self):
        self.assertEqual(len(self.empty_dictionary), 0)
        self.assertEqual(len(self.dictionary_length_1), 1)
        self.assertEqual(len(self.range_dictionary), 4)
        self.assertEqual(len(self.dictionary), 5)

    def test_repr(self):
        class_name = self.tested_class.__name__
        self.assertEqual(repr(self.empty_dictionary),
                         '{}({{}})'.format(class_name))
        self.assertEqual(repr(self.dictionary_length_1),
                         '{}({{None: 0}})'.format(class_name))
        self.assertEqual(repr(self.range_dictionary),
                         '{}({{\'a\': 0, \'b\': 1, \'c\': 2, '
                         '\'d\': 3}})'.format(class_name))
        self.assertEqual(repr(self.dictionary),
                         '{}({{0: 1, 1: 42, 2: -3, 3: 2, '
                         '...}})'.format(class_name))
        self.assertEqual(repr(self.tested_class.from_iterable(
            zip(range(10), range(10)))),
                         '{}({{0: 0, 1: 1, 2: 2, 3: 3, '
                         '...}})'.format(class_name))

    def test_str(self):
        self.assertEqual(str(self.empty_dictionary), '')
        self.assertEqual(str(self.dictionary_length_1), 'None: 0')
        self.assertEqual(str(self.range_dictionary),
                         'a: 0, b: 1, c: 2, d: 3')
        self.assertEqual(str(self.dictionary),
                         '0: 1, 1: 42, 2: -3, 3: 2, 4: 42')
        self.assertEqual(str(self.tested_class.from_iterable(
            zip(range(10), range(10)))),
            '0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, '
            '8: 8, 9: 9')

    def test_getitem(self):
        with self.assertRaises(KeyError):
            _ = self.empty_dictionary[0]

        # print(repr(self.dictionary_length_1))
        self.assertEqual(self.dictionary_length_1[None], 0)
        self.assertEqual(self.range_dictionary['a'], 0)
        self.assertEqual(self.range_dictionary['b'], 1)
        self.assertEqual(self.range_dictionary['c'], 2)
        self.assertEqual(self.range_dictionary['d'], 3)
        self.assertEqual(self.dictionary[0], 1)
        self.assertEqual(self.dictionary[1], 42)
        self.assertEqual(self.dictionary[2], -3)
        self.assertEqual(self.dictionary[3], 2)
        self.assertEqual(self.dictionary[4], 42)

    def test_set_item(self):
        with self.assertRaises(KeyError):
            self.empty_dictionary[0] = 0
        with self.assertRaises(KeyError):
            self.dictionary_length_1[0] = 1
        with self.assertRaises(KeyError):
            self.range_dictionary['e'] = 5
        with self.assertRaises(KeyError):
            self.dictionary[-1] = 43

        self.dictionary_length_1[None] = 1
        self.assertEqual(self.dictionary_length_1,
                         self.tested_class.from_dictionary({None: 1}))

        self.range_dictionary['a'] = 1
        self.range_dictionary['b'] = 2
        self.range_dictionary['c'] = 3
        self.range_dictionary['d'] = 4
        self.assertEqual(self.range_dictionary,
                         self.tested_class.from_dictionary(
                             {'a': 1, 'b': 2, 'c': 3, 'd': 4}))

    def test_del_item(self):
        with self.assertRaises(KeyError):
            del self.empty_dictionary[0]
        with self.assertRaises(KeyError):
            del self.dictionary_length_1[0]
        with self.assertRaises(KeyError):
            del self.range_dictionary['e']
        with self.assertRaises(KeyError):
            del self.range_dictionary[0]
        with self.assertRaises(KeyError):
            del self.dictionary[-1]

        del self.dictionary_length_1[None]
        self.assertEqual(self.dictionary_length_1, self.tested_class())

        del self.range_dictionary['b']
        self.assertEqual(self.range_dictionary,
                         self.tested_class.from_dictionary(
                             {'a': 0, 'c': 2, 'd': 3}))

        del self.range_dictionary['a']
        self.assertEqual(self.range_dictionary,
                         self.tested_class.from_dictionary({'c': 2, 'd': 3}))

        del self.range_dictionary['d']
        self.assertEqual(self.range_dictionary,
                         self.tested_class.from_dictionary({'c': 2}))

    def test_is_empty(self):
        self.assertTrue(self.empty_dictionary.is_empty())
        self.assertFalse(self.dictionary_length_1.is_empty())
        self.assertFalse(self.range_dictionary.is_empty())
        self.assertFalse(self.dictionary.is_empty())

    def test_insert(self):
        with self.assertRaises(KeyError):
            self.dictionary_length_1.insert(None, None)
        with self.assertRaises(KeyError):
            self.range_dictionary.insert('a', None)
        with self.assertRaises(KeyError):
            self.range_dictionary.insert('b', None)
        with self.assertRaises(KeyError):
            self.range_dictionary.insert('c', None)
        with self.assertRaises(KeyError):
            self.range_dictionary.insert('d', None)
        with self.assertRaises(KeyError):
            self.dictionary.insert(0, None)
        with self.assertRaises(KeyError):
            self.dictionary.insert(1, None)
        with self.assertRaises(KeyError):
            self.dictionary.insert(2, None)
        with self.assertRaises(KeyError):
            self.dictionary.insert(3, None)
        with self.assertRaises(KeyError):
            self.dictionary.insert(4, None)

        self.empty_dictionary.insert(True, None)
        self.dictionary_length_1.insert(0, 1)
        self.dictionary_length_1.insert(-1, 2)
        self.range_dictionary.insert(0, 3)
        self.range_dictionary.insert(-1, -1)
        self.range_dictionary.insert(-5, 42)
        self.dictionary.insert(5, 3)
        self.dictionary.insert(-1, -1)
        self.dictionary.insert(-5, 42)

        self.assertEqual(self.empty_dictionary,
                         self.tested_class.from_dictionary({True: None}))
        self.assertEqual(self.dictionary_length_1,
                         self.tested_class.from_dictionary(
                             {None: 0, -1: 2, 0: 1}))
        self.assertEqual(self.range_dictionary,
                         self.tested_class.from_dictionary(
                             {0: 3, -1: -1, -5: 42, 'a': 0, 'b': 1, 'c': 2,
                              'd': 3}))
        self.assertEqual(self.dictionary,
                         self.tested_class.from_dictionary(
                             {-5: 42, -1: -1, 0: 1, 1: 42, 2: -3, 3: 2, 4: 42,
                              5: 3}))

    def test_clear(self):
        self.empty_dictionary.clear()
        self.dictionary_length_1.clear()
        self.range_dictionary.clear()
        self.dictionary.clear()

        self.assertEqual(self.empty_dictionary, self.tested_class())
        self.assertEqual(self.dictionary_length_1, self.tested_class())
        self.assertEqual(self.range_dictionary, self.tested_class())
        self.assertEqual(self.dictionary, self.tested_class())

    def test_pop(self):
        with self.assertRaises(KeyError):
            self.empty_dictionary.pop(0)
        with self.assertRaises(KeyError):
            self.dictionary_length_1.pop(0)
        with self.assertRaises(KeyError):
            self.range_dictionary.pop('e')
        with self.assertRaises(KeyError):
            self.range_dictionary.pop(0)
        with self.assertRaises(KeyError):
            self.dictionary.pop(-1)

        self.assertEqual(self.dictionary_length_1.pop(None), 0)
        self.assertEqual(self.range_dictionary.pop('c'), 2)
        self.assertEqual(self.range_dictionary.pop('a'), 0)
        self.assertEqual(self.dictionary.pop(1), 42)
        self.assertEqual(self.dictionary.pop(3), 2)

        self.assertEqual(self.dictionary_length_1, self.tested_class())
        self.assertEqual(self.range_dictionary,
                         self.tested_class.from_dictionary({'b': 1, 'd': 3}))
        self.assertEqual(self.dictionary,
                         self.tested_class.from_dictionary(
                             {0: 1, 2: -3, 4: 42}))

    def test_keys(self):
        self.assertEqual(list(self.empty_dictionary.keys()), [])
        self.assertEqual(list(self.dictionary_length_1.keys()), [None])
        self.assertEqual(list(self.range_dictionary.keys()),
                         ['a', 'b', 'c', 'd'])
        self.assertEqual(list(self.dictionary.keys()), [0, 1, 2, 3, 4])

    def test_items(self):
        self.assertEqual(list(self.empty_dictionary.items()), [])
        self.assertEqual(list(self.dictionary_length_1.items()), [(None, 0)])
        self.assertEqual(list(self.range_dictionary.items()),
                         [('a', 0), ('b', 1), ('c', 2), ('d', 3)])
        self.assertEqual(list(self.dictionary.items()),
                         [(0, 1), (1, 42), (2, -3), (3, 2), (4, 42)])

    def test_values(self):
        self.assertEqual(list(self.empty_dictionary.values()), [])
        self.assertEqual(list(self.dictionary_length_1.values()), [0])
        self.assertEqual(list(self.range_dictionary.values()), [0, 1, 2, 3])
        self.assertEqual(list(self.dictionary.values()), [1, 42, -3, 2, 42])


class TestLinkedDictionary(TestDictionary):
    def __init__(self, method_name):
        super().__init__(method_name=method_name,
                         tested_class=LinkedDictionary)

    def test_init(self):
        self.assertEqual(self.empty_dictionary._head, None)
        self.assertEqual(len(self.empty_dictionary), 0)

        self.assertEqual(self.dictionary_length_1._head.key, None)
        self.assertEqual(self.dictionary_length_1._head.value, 0)
        self.assertEqual(self.dictionary_length_1._head.successor, None)
        self.assertEqual(len(self.dictionary_length_1), 1)

        self.assertEqual(self.range_dictionary._head.key, 'a')
        self.assertEqual(self.range_dictionary._head.value, 0)
        self.assertEqual(self.range_dictionary._head.successor.key, 'b')
        self.assertEqual(self.range_dictionary._head.successor.value, 1)
        self.assertEqual(self.range_dictionary._head.successor.successor.key,
                         'c')
        self.assertEqual(self.range_dictionary._head.successor.successor.value,
                         2)
        self.assertEqual(self.range_dictionary._head.successor.successor
                         .successor.key, 'd')
        self.assertEqual(self.range_dictionary._head.successor.successor
                         .successor.value, 3)
        self.assertEqual(self.range_dictionary._head.successor.successor
                         .successor.successor, None)
        self.assertEqual(len(self.range_dictionary), 4)

        self.assertEqual(self.dictionary._head.key, 0)
        self.assertEqual(self.dictionary._head.value, 1)
        self.assertEqual(self.dictionary._head.successor.key, 1)
        self.assertEqual(self.dictionary._head.successor.value, 42)
        self.assertEqual(self.dictionary._head.successor.successor.key, 2)
        self.assertEqual(self.dictionary._head.successor.successor.value, -3)
        self.assertEqual(self.dictionary._head.successor.successor.successor
                         .key, 3)
        self.assertEqual(self.dictionary._head.successor.successor.successor
                         .value, 2)
        self.assertEqual(self.dictionary._head.successor.successor.successor
                         .successor.key, 4)
        self.assertEqual(self.dictionary._head.successor.successor.successor
                         .successor.value, 42)
        self.assertEqual(self.dictionary._head.successor.successor.successor
                         .successor.successor, None)
        self.assertEqual(len(self.dictionary), 5)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # add test methods as separate tests to test suite
    for test_case in [TestLinkedDictionary]:
        for name in unittest.defaultTestLoader.getTestCaseNames(test_case):
            suite.addTest(test_case(name))

    # run the tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
