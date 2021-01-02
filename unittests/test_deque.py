# Sebastian Thomas (datascience at sebastianthomas dot de)

# copying objects
from copy import copy

# unit tests
import unittest

# custom modules
from datastructures.deque import *


class TestDeque(unittest.TestCase):
    def __new__(cls, method_name, tested_class=None):
        if cls is TestDeque:
            raise TypeError('Class TestDeque may not be instantiated.')
        return super().__new__(cls)

    def __init__(self, method_name, tested_class=None):
        super().__init__(methodName=method_name)
        self.tested_class = tested_class

    def setUp(self):
        self.empty_deque = self.tested_class()

        self.deque_length_1 = self.tested_class()
        self.deque_length_1.enqueue_rear(0)

        self.range_deque = self.tested_class()
        self.range_deque += range(4)

        self.deque = self.tested_class()
        self.deque += [1, 42, -3, 2, 42]

    def test_eq(self):
        deque = self.tested_class()
        self.assertEqual(self.empty_deque, deque)
        deque = self.tested_class()
        deque += [0]
        self.assertEqual(self.deque_length_1, deque)
        deque = self.tested_class()
        deque += range(4)
        self.assertEqual(self.range_deque, deque)
        deque = self.tested_class()
        deque += [1, 42, -3, 2, 42]
        self.assertEqual(self.deque, deque)

        self.assertNotEqual(self.empty_deque, self.deque_length_1)
        self.assertNotEqual(self.deque_length_1, self.range_deque)
        self.assertNotEqual(self.range_deque, self.deque)
        self.assertNotEqual(self.deque, self.empty_deque)
        self.assertNotEqual(self.empty_deque, [])
        self.assertNotEqual(self.deque_length_1, [0])
        self.assertNotEqual(self.range_deque, range(4))
        self.assertNotEqual(self.deque, [1, 42, -3, 2, 42])

    def test_iter(self):
        self.assertEqual(list(iter(self.empty_deque)), [])
        self.assertEqual(list(iter(self.deque_length_1)), [0])
        self.assertEqual(list(iter(self.range_deque)), [0, 1, 2, 3])
        self.assertEqual(list(iter(self.deque)), [1, 42, -3, 2, 42])

    def test_copy(self):
        self.assertEqual(copy(self.empty_deque), self.empty_deque)
        self.assertEqual(copy(self.deque_length_1), self.deque_length_1)
        self.assertEqual(copy(self.range_deque), self.range_deque)
        self.assertEqual(copy(self.deque), self.deque)

    def test_bool(self):
        self.assertFalse(bool(self.empty_deque))
        self.assertTrue(bool(self.deque_length_1))
        self.assertTrue(bool(self.range_deque))
        self.assertTrue(bool(self.deque))

    def test_len(self):
        self.assertEqual(len(self.empty_deque), 0)
        self.assertEqual(len(self.deque_length_1), 1)
        self.assertEqual(len(self.range_deque), 4)
        self.assertEqual(len(self.deque), 5)

    def test_repr(self):
        class_name = self.tested_class.__name__
        self.assertEqual(repr(self.empty_deque), '{}([])'.format(class_name))
        self.assertEqual(repr(self.deque_length_1),
                         '{}([0])'.format(class_name))
        self.assertEqual(repr(self.range_deque),
                         '{}([0, 1, 2, 3])'.format(class_name))
        self.assertEqual(repr(self.deque),
                         '{}([1, 42, -3, 2, 42])'.format(class_name))

    def test_str(self):
        self.assertEqual(str(self.empty_deque), '')
        self.assertEqual(str(self.deque_length_1), '0')
        self.assertEqual(str(self.range_deque), '0 1 2 3')
        self.assertEqual(str(self.deque), '1 42 -3 2 42')

    def test_contains(self):
        self.assertFalse(0 in self.empty_deque)
        self.assertTrue(0 in self.deque_length_1)
        self.assertFalse(1 in self.deque_length_1)
        self.assertFalse('0' in self.deque_length_1)
        self.assertTrue(0 in self.range_deque)
        self.assertTrue(1 in self.range_deque)
        self.assertTrue(2 in self.range_deque)
        self.assertTrue(3 in self.range_deque)
        self.assertFalse(-1 in self.range_deque)
        self.assertFalse(4 in self.range_deque)
        self.assertFalse('0' in self.range_deque)
        self.assertFalse('1' in self.range_deque)
        self.assertFalse('2' in self.range_deque)
        self.assertFalse('3' in self.range_deque)
        self.assertTrue(-3 in self.deque)
        self.assertTrue(1 in self.deque)
        self.assertTrue(2 in self.deque)
        self.assertTrue(42 in self.deque)
        self.assertFalse(0 in self.deque)
        self.assertFalse('-3' in self.deque)
        self.assertFalse('1' in self.deque)
        self.assertFalse('2' in self.deque)
        self.assertFalse('42' in self.deque)

    def test_iadd(self):
        with self.assertRaises(TypeError):
            self.empty_deque += 2
        with self.assertRaises(TypeError):
            self.deque_length_1 += 2.5
        with self.assertRaises(TypeError):
            self.range_deque += True
        with self.assertRaises(TypeError):
            self.deque += None

        id_empty_deque = id(self.empty_deque)
        id_deque_length_1 = id(self.deque_length_1)
        id_range_deque = id(self.range_deque)
        id_deque = id(self.deque)

        self.empty_deque += self.deque_length_1
        self.deque_length_1 += self.range_deque
        self.range_deque += self.deque
        self.deque += self.empty_deque

        self.assertEqual(id(self.empty_deque), id_empty_deque)
        self.assertEqual(id(self.deque_length_1), id_deque_length_1)
        self.assertEqual(id(self.range_deque), id_range_deque)
        self.assertEqual(id(self.deque), id_deque)

        deque = self.tested_class()
        deque += [0]
        self.assertEqual(self.empty_deque, deque)
        deque = self.tested_class()
        deque += [0, 0, 1, 2, 3]
        self.assertEqual(self.deque_length_1, deque)
        deque = self.tested_class()
        deque += [0, 1, 2, 3, 1, 42, -3, 2, 42]
        self.assertEqual(self.range_deque, deque)
        deque = self.tested_class()
        deque += [1, 42, -3, 2, 42, 0]
        self.assertEqual(self.deque, deque)

        self.empty_deque += [-1, -1]
        self.deque_length_1 += tuple('deque')
        self.range_deque += (-1, -2, -3)
        self.deque += []

        self.assertEqual(id(self.empty_deque), id_empty_deque)
        self.assertEqual(id(self.deque_length_1), id_deque_length_1)
        self.assertEqual(id(self.range_deque), id_range_deque)
        self.assertEqual(id(self.deque), id_deque)
        deque = self.tested_class()
        deque += [0, -1, -1]
        self.assertEqual(self.empty_deque, deque)
        deque = self.tested_class()
        deque += [0, 0, 1, 2, 3, 'd', 'e', 'q', 'u', 'e']
        self.assertEqual(self.deque_length_1, deque)
        deque = self.tested_class()
        deque += [0, 1, 2, 3, 1, 42, -3, 2, 42, -1, -2, -3]
        self.assertEqual(self.range_deque, deque)
        deque = self.tested_class()
        deque += [1, 42, -3, 2, 42, 0]
        self.assertEqual(self.deque, deque)

    def test_is_empty(self):
        self.assertTrue(self.empty_deque.is_empty())
        self.assertFalse(self.deque_length_1.is_empty())
        self.assertFalse(self.range_deque.is_empty())
        self.assertFalse(self.deque.is_empty())

    def test_peek_rear(self):
        with self.assertRaises(EmptyDequeException):
            self.empty_deque.peek_rear()

        self.assertEqual(self.deque_length_1.peek_rear(), 0)
        self.assertEqual(self.range_deque.peek_rear(), 3)
        self.assertEqual(self.deque.peek_rear(), 42)

    def test_peek_front(self):
        with self.assertRaises(EmptyDequeException):
            self.empty_deque.peek_front()

        self.assertEqual(self.deque_length_1.peek_front(), 0)
        self.assertEqual(self.range_deque.peek_front(), 0)
        self.assertEqual(self.deque.peek_front(), 1)

    def test_enqueue_rear(self):
        self.empty_deque.enqueue_rear(-1)
        self.deque_length_1.enqueue_rear(-1)
        self.deque_length_1.enqueue_rear(-2)
        self.range_deque.enqueue_rear(-1)
        self.range_deque.enqueue_rear(-2)
        self.range_deque.enqueue_rear(-3)
        self.deque.enqueue_rear(-1)
        self.deque.enqueue_rear(-2)
        self.deque.enqueue_rear(-3)

        deque = self.tested_class()
        deque += [-1]
        self.assertEqual(self.empty_deque, deque)
        deque = self.tested_class()
        deque += [0, -1, -2]
        self.assertEqual(self.deque_length_1, deque)
        deque = self.tested_class()
        deque += [0, 1, 2, 3, -1, -2, -3]
        self.assertEqual(self.range_deque, deque)
        deque = self.tested_class()
        deque += [1, 42, -3, 2, 42, -1, -2, -3]
        self.assertEqual(self.deque, deque)

    def test_enqueue_front(self):
        self.empty_deque.enqueue_front(-1)
        self.deque_length_1.enqueue_front(-1)
        self.deque_length_1.enqueue_front(-2)
        self.range_deque.enqueue_front(-1)
        self.range_deque.enqueue_front(-2)
        self.range_deque.enqueue_front(-3)
        self.deque.enqueue_front(-1)
        self.deque.enqueue_front(-2)
        self.deque.enqueue_front(-3)

        deque = self.tested_class()
        deque += [-1]
        self.assertEqual(self.empty_deque, deque)
        deque = self.tested_class()
        deque += [-2, -1, 0]
        self.assertEqual(self.deque_length_1, deque)
        deque = self.tested_class()
        deque += [-3, -2, -1, 0, 1, 2, 3]
        self.assertEqual(self.range_deque, deque)
        deque = self.tested_class()
        deque += [-3, -2, -1, 1, 42, -3, 2, 42]
        self.assertEqual(self.deque, deque)

    def test_dequeue_rear(self):
        with self.assertRaises(EmptyDequeException):
            self.empty_deque.dequeue_rear()

        self.deque_length_1.dequeue_rear()
        self.range_deque.dequeue_rear()
        self.range_deque.dequeue_rear()
        self.deque.dequeue_rear()
        self.deque.dequeue_rear()

        deque = self.tested_class()
        self.assertEqual(self.deque_length_1, deque)
        deque = self.tested_class()
        deque += [0, 1]
        self.assertEqual(self.range_deque, deque)
        deque = self.tested_class()
        deque += [1, 42, -3]
        self.assertEqual(self.deque, deque)

        self.deque.dequeue_rear()
        self.deque.dequeue_rear()
        self.deque.dequeue_rear()
        with self.assertRaises(EmptyDequeException):
            self.deque.dequeue_rear()

    def test_dequeue_front(self):
        with self.assertRaises(EmptyDequeException):
            self.empty_deque.dequeue_front()

        self.deque_length_1.dequeue_front()
        self.range_deque.dequeue_front()
        self.range_deque.dequeue_front()
        self.deque.dequeue_front()
        self.deque.dequeue_front()

        deque = self.tested_class()
        self.assertEqual(self.deque_length_1, deque)
        deque = self.tested_class()
        deque += [2, 3]
        self.assertEqual(self.range_deque, deque)
        deque = self.tested_class()
        deque += [-3, 2, 42]
        self.assertEqual(self.deque, deque)

        self.deque.dequeue_front()
        self.deque.dequeue_front()
        self.deque.dequeue_front()
        with self.assertRaises(EmptyDequeException):
            self.deque.dequeue_front()


class TestArrayDeque(TestDeque):
    def __init__(self, method_name):
        super().__init__(method_name=method_name, tested_class=ArrayDeque)

    def test_init(self):
        self.assertEqual(self.empty_deque._values, [])
        self.assertEqual(self.deque_length_1._values, [0])
        self.assertEqual(self.range_deque._values, [0, 1, 2, 3])
        self.assertEqual(self.deque._values, [1, 42, -3, 2, 42])


class TestLinkedDeque(TestDeque):
    def __init__(self, method_name):
        super().__init__(method_name=method_name, tested_class=LinkedDeque)

    def test_init(self):
        self.assertEqual(self.empty_deque._front, None)
        self.assertEqual(self.empty_deque._rear, None)

        self.assertEqual(self.deque_length_1._front, self.deque_length_1._rear)
        self.assertEqual(self.deque_length_1._rear.value, 0)
        self.assertEqual(self.deque_length_1._rear.successor, None)

        self.assertEqual(self.range_deque._front.value, 0)
        self.assertEqual(self.range_deque._front.predecessor, None)
        self.assertEqual(self.range_deque._front.successor.value, 1)
        self.assertEqual(self.range_deque._front.successor.predecessor.value,
                         0)
        self.assertEqual(self.range_deque._front.successor.successor.value, 2)
        self.assertEqual(self.range_deque._front.successor.successor
                         .predecessor.value, 1)
        self.assertEqual(self.range_deque._front.successor.successor
                         .successor, self.range_deque._rear)
        self.assertEqual(self.range_deque._rear.value, 3)
        self.assertEqual(self.range_deque._rear.predecessor.value, 2)
        self.assertEqual(self.range_deque._rear.successor, None)

        self.assertEqual(self.deque._front.value, 1)
        self.assertEqual(self.deque._front.predecessor, None)
        self.assertEqual(self.deque._front.successor.value, 42)
        self.assertEqual(self.deque._front.successor.predecessor.value, 1)
        self.assertEqual(self.deque._front.successor.successor.value, -3)
        self.assertEqual(self.deque._front.successor.successor.predecessor
                         .value, 42)
        self.assertEqual(self.deque._front.successor.successor.successor.value,
                         2)
        self.assertEqual(self.deque._front.successor.successor.successor
                         .predecessor.value, -3)
        self.assertEqual(self.deque._front.successor.successor.successor
                         .successor, self.deque._rear)
        self.assertEqual(self.deque._rear.value, 42)
        self.assertEqual(self.deque._rear.predecessor.value, 2)
        self.assertEqual(self.deque._rear.successor, None)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # add test methods as separate tests to test suite
    for test_case in [TestArrayDeque, TestLinkedDeque]:
        for name in unittest.defaultTestLoader.getTestCaseNames(test_case):
            suite.addTest(test_case(name))

    # run the tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
