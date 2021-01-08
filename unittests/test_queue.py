# Sebastian Thomas (datascience at sebastianthomas dot de)

# copying objects
from copy import copy

# unit tests
import unittest

# custom modules
from datastructures.base import EmptyCollectionException
from datastructures.queue import *


class TestQueue(unittest.TestCase):
    def __new__(cls, method_name, tested_class=None):
        if cls is TestQueue:
            raise TypeError('Class TestQueue may not be instantiated.')
        return super().__new__(cls)

    def __init__(self, method_name, tested_class=None):
        super().__init__(methodName=method_name)
        self.tested_class = tested_class

    def setUp(self):
        self.empty_queue = self.tested_class()

        self.queue_length_1 = self.tested_class()
        self.queue_length_1.enqueue(0)

        self.range_queue = self.tested_class()
        self.range_queue += range(4)

        self.queue = self.tested_class()
        self.queue += [1, 42, -3, 2, 42]

    def test_eq(self):
        queue = self.tested_class()
        self.assertEqual(self.empty_queue, queue)
        queue = self.tested_class()
        queue += [0]
        self.assertEqual(self.queue_length_1, queue)
        queue = self.tested_class()
        queue += range(4)
        self.assertEqual(self.range_queue, queue)
        queue = self.tested_class()
        queue += [1, 42, -3, 2, 42]
        self.assertEqual(self.queue, queue)

        self.assertNotEqual(self.empty_queue, self.queue_length_1)
        self.assertNotEqual(self.queue_length_1, self.range_queue)
        self.assertNotEqual(self.range_queue, self.queue)
        self.assertNotEqual(self.queue, self.empty_queue)
        self.assertNotEqual(self.empty_queue, [])
        self.assertNotEqual(self.queue_length_1, [0])
        self.assertNotEqual(self.range_queue, range(4))
        self.assertNotEqual(self.queue, [1, 42, -3, 2, 42])

    def test_copy(self):
        self.assertEqual(copy(self.empty_queue), self.empty_queue)
        self.assertEqual(copy(self.queue_length_1), self.queue_length_1)
        self.assertEqual(copy(self.range_queue), self.range_queue)
        self.assertEqual(copy(self.queue), self.queue)

    def test_iter(self):
        self.assertEqual(list(iter(self.empty_queue)), [])
        self.assertEqual(list(iter(self.queue_length_1)), [0])
        self.assertEqual(list(iter(self.range_queue)), [0, 1, 2, 3])
        self.assertEqual(list(iter(self.queue)), [1, 42, -3, 2, 42])

    def test_bool(self):
        self.assertFalse(bool(self.empty_queue))
        self.assertTrue(bool(self.queue_length_1))
        self.assertTrue(bool(self.range_queue))
        self.assertTrue(bool(self.queue))

    def test_len(self):
        self.assertEqual(len(self.empty_queue), 0)
        self.assertEqual(len(self.queue_length_1), 1)
        self.assertEqual(len(self.range_queue), 4)
        self.assertEqual(len(self.queue), 5)

    def test_repr(self):
        class_name = self.tested_class.__name__
        self.assertEqual(repr(self.empty_queue), '{}([])'.format(class_name))
        self.assertEqual(repr(self.queue_length_1),
                         '{}([0])'.format(class_name))
        self.assertEqual(repr(self.range_queue),
                         '{}([0, 1, 2, 3])'.format(class_name))
        self.assertEqual(repr(self.queue),
                         '{}([1, 42, -3, 2, 42])'.format(class_name))

    def test_str(self):
        self.assertEqual(str(self.empty_queue), '')
        self.assertEqual(str(self.queue_length_1), '0')
        self.assertEqual(str(self.range_queue), '0 1 2 3')
        self.assertEqual(str(self.queue), '1 42 -3 2 42')

    def test_contains(self):
        self.assertFalse(0 in self.empty_queue)
        self.assertTrue(0 in self.queue_length_1)
        self.assertFalse(1 in self.queue_length_1)
        self.assertFalse('0' in self.queue_length_1)
        self.assertTrue(0 in self.range_queue)
        self.assertTrue(1 in self.range_queue)
        self.assertTrue(2 in self.range_queue)
        self.assertTrue(3 in self.range_queue)
        self.assertFalse(-1 in self.range_queue)
        self.assertFalse(4 in self.range_queue)
        self.assertFalse('0' in self.range_queue)
        self.assertFalse('1' in self.range_queue)
        self.assertFalse('2' in self.range_queue)
        self.assertFalse('3' in self.range_queue)
        self.assertTrue(-3 in self.queue)
        self.assertTrue(1 in self.queue)
        self.assertTrue(2 in self.queue)
        self.assertTrue(42 in self.queue)
        self.assertFalse(0 in self.queue)
        self.assertFalse('-3' in self.queue)
        self.assertFalse('1' in self.queue)
        self.assertFalse('2' in self.queue)
        self.assertFalse('42' in self.queue)

    def test_getitem(self):
        with self.assertRaises(KeyError):
            _ = self.empty_queue[0]

        with self.assertRaises(EmptyCollectionException):
            _ = self.empty_queue[FRONT]

        self.assertEqual(self.queue_length_1[FRONT], 0)
        self.assertEqual(self.range_queue[FRONT], 0)
        self.assertEqual(self.queue[FRONT], 1)

    def test_delitem(self):
        with self.assertRaises(KeyError):
            del self.empty_queue[0]

        with self.assertRaises(EmptyCollectionException):
            del self.empty_queue[FRONT]

        del self.queue_length_1[FRONT]
        queue = self.tested_class()
        self.assertEqual(self.queue_length_1, queue)
        del self.range_queue[FRONT]
        queue = self.tested_class()
        queue += [1, 2, 3]
        self.assertEqual(self.range_queue, queue)
        del self.queue[FRONT]
        queue = self.tested_class()
        queue += [42, -3, 2, 42]
        self.assertEqual(self.queue, queue)

    def test_iadd(self):
        with self.assertRaises(TypeError):
            self.empty_queue += 2
        with self.assertRaises(TypeError):
            self.queue_length_1 += 2.5
        with self.assertRaises(TypeError):
            self.range_queue += True
        with self.assertRaises(TypeError):
            self.queue += None

        id_empty_queue = id(self.empty_queue)
        id_queue_length_1 = id(self.queue_length_1)
        id_range_queue = id(self.range_queue)
        id_queue = id(self.queue)

        self.empty_queue += self.queue_length_1
        self.queue_length_1 += self.range_queue
        self.range_queue += self.queue
        self.queue += self.empty_queue

        self.assertEqual(id(self.empty_queue), id_empty_queue)
        self.assertEqual(id(self.queue_length_1), id_queue_length_1)
        self.assertEqual(id(self.range_queue), id_range_queue)
        self.assertEqual(id(self.queue), id_queue)

        queue = self.tested_class()
        queue += [0]
        self.assertEqual(self.empty_queue, queue)
        queue = self.tested_class()
        queue += [0, 0, 1, 2, 3]
        self.assertEqual(self.queue_length_1, queue)
        queue = self.tested_class()
        queue += [0, 1, 2, 3, 1, 42, -3, 2, 42]
        self.assertEqual(self.range_queue, queue)
        queue = self.tested_class()
        queue += [1, 42, -3, 2, 42, 0]
        self.assertEqual(self.queue, queue)

        self.empty_queue += [-1, -1]
        self.queue_length_1 += tuple('queue')
        self.range_queue += (-1, -2, -3)
        self.queue += []

        self.assertEqual(id(self.empty_queue), id_empty_queue)
        self.assertEqual(id(self.queue_length_1), id_queue_length_1)
        self.assertEqual(id(self.range_queue), id_range_queue)
        self.assertEqual(id(self.queue), id_queue)
        queue = self.tested_class()
        queue += [0, -1, -1]
        self.assertEqual(self.empty_queue, queue)
        queue = self.tested_class()
        queue += [0, 0, 1, 2, 3, 'q', 'u', 'e', 'u', 'e']
        self.assertEqual(self.queue_length_1, queue)
        queue = self.tested_class()
        queue += [0, 1, 2, 3, 1, 42, -3, 2, 42, -1, -2, -3]
        self.assertEqual(self.range_queue, queue)
        queue = self.tested_class()
        queue += [1, 42, -3, 2, 42, 0]
        self.assertEqual(self.queue, queue)

    def test_is_empty(self):
        self.assertTrue(self.empty_queue.is_empty())
        self.assertFalse(self.queue_length_1.is_empty())
        self.assertFalse(self.range_queue.is_empty())
        self.assertFalse(self.queue.is_empty())

    def test_get(self):
        with self.assertRaises(EmptyCollectionException):
            self.empty_queue.get()

        self.assertEqual(self.queue_length_1.get(), 0)
        self.assertEqual(self.range_queue.get(), 0)
        self.assertEqual(self.queue.get(), 1)

    def test_peek(self):
        with self.assertRaises(EmptyCollectionException):
            self.empty_queue.peek()

        self.assertEqual(self.queue_length_1.peek(), 0)
        self.assertEqual(self.range_queue.peek(), 0)
        self.assertEqual(self.queue.peek(), 1)

    def test_insert(self):
        with self.assertRaises(KeyError):
            self.empty_queue.insert(0, 1)

        self.empty_queue.insert(REAR, -1)
        self.queue_length_1.insert(REAR, -1)
        self.queue_length_1.insert(REAR, -2)
        self.range_queue.insert(REAR, -1)
        self.range_queue.insert(REAR, -2)
        self.range_queue.insert(REAR, -3)
        self.queue.insert(REAR, -1)
        self.queue.insert(REAR, -2)
        self.queue.insert(REAR, -3)

        queue = self.tested_class()
        queue += [-1]
        self.assertEqual(self.empty_queue, queue)
        queue = self.tested_class()
        queue += [0, -1, -2]
        self.assertEqual(self.queue_length_1, queue)
        queue = self.tested_class()
        queue += [0, 1, 2, 3, -1, -2, -3]
        self.assertEqual(self.range_queue, queue)
        queue = self.tested_class()
        queue += [1, 42, -3, 2, 42, -1, -2, -3]
        self.assertEqual(self.queue, queue)

    def test_post(self):
        self.empty_queue.post(-1)
        self.queue_length_1.post(-1)
        self.queue_length_1.post(-2)
        self.range_queue.post(-1)
        self.range_queue.post(-2)
        self.range_queue.post(-3)
        self.queue.post(-1)
        self.queue.post(-2)
        self.queue.post(-3)

        queue = self.tested_class()
        queue += [-1]
        self.assertEqual(self.empty_queue, queue)
        queue = self.tested_class()
        queue += [0, -1, -2]
        self.assertEqual(self.queue_length_1, queue)
        queue = self.tested_class()
        queue += [0, 1, 2, 3, -1, -2, -3]
        self.assertEqual(self.range_queue, queue)
        queue = self.tested_class()
        queue += [1, 42, -3, 2, 42, -1, -2, -3]
        self.assertEqual(self.queue, queue)

    def test_enqueue(self):
        self.empty_queue.enqueue(-1)
        self.queue_length_1.enqueue(-1)
        self.queue_length_1.enqueue(-2)
        self.range_queue.enqueue(-1)
        self.range_queue.enqueue(-2)
        self.range_queue.enqueue(-3)
        self.queue.enqueue(-1)
        self.queue.enqueue(-2)
        self.queue.enqueue(-3)

        queue = self.tested_class()
        queue += [-1]
        self.assertEqual(self.empty_queue, queue)
        queue = self.tested_class()
        queue += [0, -1, -2]
        self.assertEqual(self.queue_length_1, queue)
        queue = self.tested_class()
        queue += [0, 1, 2, 3, -1, -2, -3]
        self.assertEqual(self.range_queue, queue)
        queue = self.tested_class()
        queue += [1, 42, -3, 2, 42, -1, -2, -3]
        self.assertEqual(self.queue, queue)

    def test_delete(self):
        with self.assertRaises(EmptyCollectionException):
            self.empty_queue.delete()

        self.queue_length_1.delete()
        queue = self.tested_class()
        self.assertEqual(self.queue_length_1, queue)
        self.range_queue.delete()
        queue = self.tested_class()
        queue += [1, 2, 3]
        self.assertEqual(self.range_queue, queue)
        self.queue.delete()
        queue = self.tested_class()
        queue += [42, -3, 2, 42]
        self.assertEqual(self.queue, queue)

    def test_clear(self):
        self.empty_queue.clear()
        self.queue_length_1.clear()
        self.range_queue.clear()
        self.queue.clear()

        self.assertEqual(self.empty_queue, self.tested_class())
        self.assertEqual(self.queue_length_1, self.tested_class())
        self.assertEqual(self.range_queue, self.tested_class())
        self.assertEqual(self.queue, self.tested_class())

    def test_pop(self):
        with self.assertRaises(EmptyCollectionException):
            self.empty_queue.pop()

        self.queue_length_1.pop()
        self.range_queue.pop()
        self.range_queue.pop()
        self.queue.pop()
        self.queue.pop()

        queue = self.tested_class()
        self.assertEqual(self.queue_length_1, queue)
        queue = self.tested_class()
        queue += [2, 3]
        self.assertEqual(self.range_queue, queue)
        queue = self.tested_class()
        queue += [-3, 2, 42]
        self.assertEqual(self.queue, queue)

        self.queue.pop()
        self.queue.pop()
        self.queue.pop()
        with self.assertRaises(EmptyCollectionException):
            self.queue.pop()

    def test_dequeue(self):
        with self.assertRaises(EmptyCollectionException):
            self.empty_queue.dequeue()

        self.queue_length_1.dequeue()
        self.range_queue.dequeue()
        self.range_queue.dequeue()
        self.queue.dequeue()
        self.queue.dequeue()

        queue = self.tested_class()
        self.assertEqual(self.queue_length_1, queue)
        queue = self.tested_class()
        queue += [2, 3]
        self.assertEqual(self.range_queue, queue)
        queue = self.tested_class()
        queue += [-3, 2, 42]
        self.assertEqual(self.queue, queue)

        self.queue.dequeue()
        self.queue.dequeue()
        self.queue.dequeue()
        with self.assertRaises(EmptyCollectionException):
            self.queue.dequeue()


class TestArrayQueue(TestQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name, tested_class=ArrayQueue)

    def test_init(self):
        self.assertEqual(self.empty_queue._values, [])
        self.assertEqual(self.queue_length_1._values, [0])
        self.assertEqual(self.range_queue._values, [0, 1, 2, 3])
        self.assertEqual(self.queue._values, [1, 42, -3, 2, 42])


class TestLinkedQueue(TestQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name, tested_class=LinkedQueue)

    def test_init(self):
        self.assertEqual(self.empty_queue._front, None)
        self.assertEqual(self.empty_queue._rear, None)

        self.assertEqual(self.queue_length_1._front, self.queue_length_1._rear)
        self.assertEqual(self.queue_length_1._rear.value, 0)
        self.assertEqual(self.queue_length_1._rear.successor, None)

        self.assertEqual(self.range_queue._front.value, 0)
        self.assertEqual(self.range_queue._front.successor.value, 1)
        self.assertEqual(self.range_queue._front.successor.successor.value, 2)
        self.assertEqual(self.range_queue._front.successor.successor.successor,
                         self.range_queue._rear)
        self.assertEqual(self.range_queue._rear.value, 3)
        self.assertEqual(self.range_queue._rear.successor, None)

        self.assertEqual(self.queue._front.value, 1)
        self.assertEqual(self.queue._front.successor.value, 42)
        self.assertEqual(self.queue._front.successor.successor.value, -3)
        self.assertEqual(self.queue._front.successor.successor.successor.value,
                         2)
        self.assertEqual(self.queue._front.successor.successor.successor
                         .successor, self.queue._rear)
        self.assertEqual(self.queue._rear.value, 42)
        self.assertEqual(self.queue._rear.successor, None)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # add test methods as separate tests to test suite
    for test_case in [TestArrayQueue, TestLinkedQueue]:
        for name in unittest.defaultTestLoader.getTestCaseNames(test_case):
            suite.addTest(test_case(name))

    # run the tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
