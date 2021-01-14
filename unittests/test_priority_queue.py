# Sebastian Thomas (datascience at sebastianthomas dot de)

# copying objects
from copy import copy

# unit tests
import unittest

# custom modules
from datastructures.base import EmptyCollectionException
from datastructures.priority_queue import *


class TestPriorityQueue(unittest.TestCase):
    def __new__(cls, method_name, tested_class=None, extreme_key=None):
        if cls is TestPriorityQueue:
            raise TypeError('Class TestPriorityQueue may not be instantiated.')
        return super().__new__(cls)

    def __init__(self, method_name, tested_class=None, extreme_key=None):
        super().__init__(methodName=method_name)
        self._tested_class = tested_class
        self._extreme_key = extreme_key

    @property
    def _complementary_extreme_key(self):
        return MIN if self._extreme_key == MAX else MAX

    def _get_empty_instance(self):
        return self._tested_class(self._extreme_key)

    def _get_empty_complementary_instance(self):
        return self._tested_class(self._complementary_extreme_key)

    def setUp(self):
        self.empty_queue = self._get_empty_instance()

        self.queue_length_1 = self._get_empty_instance()
        self.queue_length_1.enqueue(0)

        self.range_queue = self._get_empty_instance()
        self.range_queue += range(4)

        self.queue = self._get_empty_instance()
        self.queue += [1, 42, -3, 2, 42]

    def test_eq(self):
        queue = self._get_empty_instance()
        self.assertEqual(self.empty_queue, queue)
        queue = self._get_empty_instance()
        queue += [0]
        self.assertEqual(self.queue_length_1, queue)
        queue = self._get_empty_instance()
        queue += [3, 2, 1, 0]
        self.assertEqual(self.range_queue, queue)
        queue = self._get_empty_instance()
        queue += [42, 2, -3, 42, 1]
        self.assertEqual(self.queue, queue)

        queue = self._get_empty_complementary_instance()
        self.assertNotEqual(self.empty_queue, queue)
        queue = self._get_empty_complementary_instance()
        queue += [0]
        self.assertNotEqual(self.queue_length_1, queue)
        queue = self._get_empty_complementary_instance()
        queue += [3, 2, 1, 0]
        self.assertNotEqual(self.range_queue, queue)
        queue = self._get_empty_complementary_instance()
        queue += [42, 2, -3, 42, 1]
        self.assertNotEqual(self.queue, queue)

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
        self.assertEqual(list(iter(self.range_queue)),
                         [3, 2, 1, 0] if self._extreme_key == MAX
                         else [0, 1, 2, 3])
        self.assertEqual(list(iter(self.queue)),
                         [42, 42, 2, 1, -3] if self._extreme_key == MAX
                         else [-3, 1, 2, 42, 42])

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
        class_name = self._tested_class.__name__
        self.assertEqual(repr(self.empty_queue), '{}([])'.format(class_name))
        self.assertEqual(repr(self.queue_length_1),
                         '{}([0])'.format(class_name))
        self.assertEqual(repr(self.range_queue),
                         '{}([{}])'.format(class_name,
                                           '3, 2, 1, 0'
                                           if self._extreme_key == MAX
                                           else '0, 1, 2, 3'))
        self.assertEqual(repr(self.queue),
                         '{}([{}])'.format(class_name,
                                           '42, 42, 2, 1, -3'
                                           if self._extreme_key == MAX
                                           else '-3, 1, 2, 42, 42'))

    def test_str(self):
        self.assertEqual(str(self.empty_queue), '')
        self.assertEqual(str(self.queue_length_1), '0')
        self.assertEqual(str(self.range_queue),
                         '3 2 1 0' if self._extreme_key == MAX else '0 1 2 3')
        self.assertEqual(str(self.queue),
                         '42 42 2 1 -3' if self._extreme_key == MAX
                         else '-3 1 2 42 42')

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

        with self.assertRaises(KeyError):
            _ = self.empty_queue[self._complementary_extreme_key]
        with self.assertRaises(KeyError):
            _ = self.queue_length_1[self._complementary_extreme_key]
        with self.assertRaises(KeyError):
            _ = self.range_queue[self._complementary_extreme_key]
        with self.assertRaises(KeyError):
            _ = self.queue[self._complementary_extreme_key]

        with self.assertRaises(EmptyCollectionException):
            _ = self.empty_queue[self._extreme_key]

        self.assertEqual(self.queue_length_1[self._extreme_key], 0)
        self.assertEqual(self.range_queue[self._extreme_key],
                         3 if self._extreme_key == MAX else 0)
        self.assertEqual(self.queue[self._extreme_key],
                         42 if self._extreme_key == MAX else -3)

    def test_delitem(self):
        with self.assertRaises(KeyError):
            del self.empty_queue[0]

        with self.assertRaises(KeyError):
            del self.empty_queue[self._complementary_extreme_key]
        with self.assertRaises(KeyError):
            del self.queue_length_1[self._complementary_extreme_key]
        with self.assertRaises(KeyError):
            del self.range_queue[self._complementary_extreme_key]
        with self.assertRaises(KeyError):
            del self.queue[self._complementary_extreme_key]

        with self.assertRaises(EmptyCollectionException):
            del self.empty_queue[self._extreme_key]

        del self.queue_length_1[self._extreme_key]
        queue = self._get_empty_instance()
        self.assertEqual(self.queue_length_1, queue)
        del self.range_queue[self._extreme_key]
        queue = self._get_empty_instance()
        queue += [2, 1, 0] if self._extreme_key == MAX else [1, 2, 3]
        self.assertEqual(self.range_queue, queue)
        del self.queue[self._extreme_key]
        queue = self._get_empty_instance()
        queue += [42, 2, 1, -3] if self._extreme_key == MAX else [1, 2, 42, 42]
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

        queue = self._get_empty_instance()
        queue += [0]
        self.assertEqual(self.empty_queue, queue)
        queue = self._get_empty_instance()
        queue += [3, 2, 1, 0, 0]
        self.assertEqual(self.queue_length_1, queue)
        queue = self._get_empty_instance()
        queue += [42, 42, 3, 2, 2, 1, 1, 0, -3]
        self.assertEqual(self.range_queue, queue)
        queue = self._get_empty_instance()
        queue += [42, 42, 2, 1, 0, -3]
        self.assertEqual(self.queue, queue)

        self.empty_queue += [-1, -1]
        with self.assertRaises(TypeError):
            self.queue_length_1 += tuple('queue')
        self.range_queue += (-1, -2, -3)
        self.queue += []

        self.assertEqual(id(self.empty_queue), id_empty_queue)
        self.assertEqual(id(self.queue_length_1), id_queue_length_1)
        self.assertEqual(id(self.range_queue), id_range_queue)
        self.assertEqual(id(self.queue), id_queue)
        queue = self._get_empty_instance()
        queue += [-1, -1, 0]
        self.assertEqual(self.empty_queue, queue)
        queue = self._get_empty_instance()
        queue += [-3, -3, -2, -1, 0, 1, 1, 2, 2, 3, 42, 42]
        self.assertEqual(self.range_queue, queue)
        queue = self._get_empty_instance()
        queue += [-3, 0, 1, 2, 42, 42]
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
        self.assertEqual(self.range_queue.get(),
                         3 if self._extreme_key == MAX else 0)
        self.assertEqual(self.queue.get(),
                         42 if self._extreme_key == MAX else -3)

    def test_peek(self):
        with self.assertRaises(EmptyCollectionException):
            self.empty_queue.peek()

        self.assertEqual(self.queue_length_1.peek(), 0)
        self.assertEqual(self.range_queue.peek(),
                         3 if self._extreme_key == MAX else 0)
        self.assertEqual(self.queue.peek(),
                         42 if self._extreme_key == MAX else -3)

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

        queue = self._get_empty_instance()
        queue += [-1]
        self.assertEqual(self.empty_queue, queue)
        queue = self._get_empty_instance()
        queue += [-2, -1, 0]
        self.assertEqual(self.queue_length_1, queue)
        queue = self._get_empty_instance()
        queue += [3, 2, 1, 0, -1, -2, -3]
        self.assertEqual(self.range_queue, queue)
        queue = self._get_empty_instance()
        queue += [-3, -3, -2, -1, 1, 2, 42, 42]
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

        queue = self._get_empty_instance()
        queue += [-1]
        self.assertEqual(self.empty_queue, queue)
        queue = self._get_empty_instance()
        queue += [-2, -1, 0]
        self.assertEqual(self.queue_length_1, queue)
        queue = self._get_empty_instance()
        queue += [3, 2, 1, 0, -1, -2, -3]
        self.assertEqual(self.range_queue, queue)
        queue = self._get_empty_instance()
        queue += [-3, -3, -2, -1, 1, 2, 42, 42]
        self.assertEqual(self.queue, queue)

    def test_delete(self):
        with self.assertRaises(EmptyCollectionException):
            self.empty_queue.delete()

        self.queue_length_1.delete()
        queue = self._get_empty_instance()
        self.assertEqual(self.queue_length_1, queue)
        self.range_queue.delete()
        queue = self._get_empty_instance()
        queue += [2, 1, 0] if self._extreme_key == MAX else [1, 2, 3]
        self.assertEqual(self.range_queue, queue)
        self.queue.delete()
        queue = self._get_empty_instance()
        queue += [42, 2, 1, -3] if self._extreme_key == MAX else [1, 2, 42, 42]
        self.assertEqual(self.queue, queue)

    def test_clear(self):
        self.empty_queue.clear()
        self.queue_length_1.clear()
        self.range_queue.clear()
        self.queue.clear()

        self.assertEqual(self.empty_queue, self._get_empty_instance())
        self.assertEqual(self.queue_length_1, self._get_empty_instance())
        self.assertEqual(self.range_queue, self._get_empty_instance())
        self.assertEqual(self.queue, self._get_empty_instance())

    def test_pop(self):
        with self.assertRaises(KeyError):
            self.empty_queue.pop(self._complementary_extreme_key)
        with self.assertRaises(KeyError):
            self.queue_length_1.pop(self._complementary_extreme_key)
        with self.assertRaises(KeyError):
            self.range_queue.pop(self._complementary_extreme_key)
        with self.assertRaises(KeyError):
            self.queue.pop(self._complementary_extreme_key)

        with self.assertRaises(EmptyCollectionException):
            self.empty_queue.pop(self._extreme_key)

        self.queue_length_1.pop(self._extreme_key)
        self.range_queue.pop(self._extreme_key)
        self.range_queue.pop(self._extreme_key)
        self.queue.pop(self._extreme_key)
        self.queue.pop(self._extreme_key)

        queue = self._get_empty_instance()
        self.assertEqual(self.queue_length_1, queue)
        queue = self._get_empty_instance()
        queue += [1, 0] if self._extreme_key == MAX else [2, 3]
        self.assertEqual(self.range_queue, queue)
        queue = self._get_empty_instance()
        queue += [2, 1, -3] if self._extreme_key == MAX else [2, 42, 42]
        self.assertEqual(self.queue, queue)

        self.queue.pop(self._extreme_key)
        self.queue.pop(self._extreme_key)
        self.queue.pop(self._extreme_key)
        with self.assertRaises(EmptyCollectionException):
            self.queue.pop(self._extreme_key)

    def test_dequeue(self):
        with self.assertRaises(EmptyCollectionException):
            self.empty_queue.dequeue()

        self.queue_length_1.dequeue()
        self.range_queue.dequeue()
        self.range_queue.dequeue()
        self.queue.dequeue()
        self.queue.dequeue()

        queue = self._get_empty_instance()
        self.assertEqual(self.queue_length_1, queue)
        queue = self._get_empty_instance()
        queue += [1, 0] if self._extreme_key == MAX else [2, 3]
        self.assertEqual(self.range_queue, queue)
        queue = self._get_empty_instance()
        queue += [2, 1, -3] if self._extreme_key == MAX else [2, 42, 42]
        self.assertEqual(self.queue, queue)

        self.queue.dequeue()
        self.queue.dequeue()
        self.queue.dequeue()
        with self.assertRaises(EmptyCollectionException):
            self.queue.dequeue()


class TestArrayPriorityQueue(TestPriorityQueue):
    def __new__(cls, method_name, tested_class=None, extreme_key=None):
        if cls is TestArrayPriorityQueue:
            raise TypeError('Class TestArrayPriorityQueue may not be '
                            'instantiated.')
        return super().__new__(cls, method_name, tested_class=tested_class,
                               extreme_key=extreme_key)

    def __init__(self, method_name, tested_class=None, extreme_key=None):
        super().__init__(method_name, tested_class=tested_class,
                         extreme_key=extreme_key)

    def test_init(self):
        self.assertEqual(self.empty_queue._values, [])
        self.assertEqual(self.queue_length_1._values, [0])
        self.assertEqual(self.range_queue._values, [0, 1, 2, 3])
        self.assertEqual(self.queue._values, [1, 42, -3, 2, 42])


class TestArrayPriorityQueueMIN(TestArrayPriorityQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name,
                         tested_class=ArrayPriorityQueue, extreme_key=MIN)


class TestArrayPriorityQueueMAX(TestArrayPriorityQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name,
                         tested_class=ArrayPriorityQueue, extreme_key=MAX)


class TestArrayMinPriorityQueue(TestPriorityQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name,
                         tested_class=ArrayMinPriorityQueue, extreme_key=MIN)

    def _get_empty_instance(self):
        return self._tested_class()

    def _get_empty_complementary_instance(self):
        return ArrayMaxPriorityQueue()


class TestArrayMaxPriorityQueue(TestPriorityQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name,
                         tested_class=ArrayMaxPriorityQueue, extreme_key=MAX)

    def _get_empty_instance(self):
        return self._tested_class()

    def _get_empty_complementary_instance(self):
        return ArrayMinPriorityQueue()


class TestOrderedArrayPriorityQueueMIN(TestArrayPriorityQueue):
    def __init__(self, method_name):
        super().__init__(method_name, tested_class=OrderedArrayPriorityQueue,
                         extreme_key=MIN)

    def test_init(self):
        self.assertEqual(self.empty_queue._values, [])
        self.assertEqual(self.queue_length_1._values, [0])
        self.assertEqual(self.range_queue._values, [3, 2, 1, 0])
        self.assertEqual(self.queue._values, [42, 42, 2, 1, -3])


class TestOrderedArrayPriorityQueueMAX(TestArrayPriorityQueue):
    def __init__(self, method_name):
        super().__init__(method_name, tested_class=OrderedArrayPriorityQueue,
                         extreme_key=MAX)

    def test_init(self):
        self.assertEqual(self.empty_queue._values, [])
        self.assertEqual(self.queue_length_1._values, [0])
        self.assertEqual(self.range_queue._values, [0, 1, 2, 3])
        self.assertEqual(self.queue._values, [-3, 1, 2, 42, 42])


class TestOrderedArrayMinPriorityQueue(TestPriorityQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name,
                         tested_class=ArrayMinPriorityQueue, extreme_key=MIN)

    def _get_empty_instance(self):
        return self._tested_class()

    def _get_empty_complementary_instance(self):
        return OrderedArrayMaxPriorityQueue()


class TestOrderedArrayMaxPriorityQueue(TestPriorityQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name,
                         tested_class=ArrayMaxPriorityQueue, extreme_key=MAX)

    def _get_empty_instance(self):
        return self._tested_class()

    def _get_empty_complementary_instance(self):
        return OrderedArrayMinPriorityQueue()


class TestHeapPriorityQueueMIN(TestArrayPriorityQueue):
    def __init__(self, method_name):
        super().__init__(method_name, tested_class=HeapPriorityQueue,
                         extreme_key=MIN)

    def test_init(self):
        self.assertEqual(self.empty_queue._values, [None])
        self.assertEqual(self.queue_length_1._values, [None, 0])
        self.assertEqual(self.range_queue._values, [None, 0, 1, 2, 3])
        self.assertEqual(self.queue._values, [None, -3, 2, 1, 42, 42])


class TestHeapPriorityQueueMAX(TestArrayPriorityQueue):
    def __init__(self, method_name):
        super().__init__(method_name, tested_class=HeapPriorityQueue,
                         extreme_key=MAX)

    def test_init(self):
        self.assertEqual(self.empty_queue._values, [None])
        self.assertEqual(self.queue_length_1._values, [None, 0])
        self.assertEqual(self.range_queue._values, [None, 3, 2, 1, 0])
        self.assertEqual(self.queue._values, [None, 42, 42, -3, 1, 2])


class TestHeapMinPriorityQueue(TestPriorityQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name,
                         tested_class=HeapMinPriorityQueue, extreme_key=MIN)

    def _get_empty_instance(self):
        return self._tested_class()

    def _get_empty_complementary_instance(self):
        return HeapMaxPriorityQueue()


class TestHeapMaxPriorityQueue(TestPriorityQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name,
                         tested_class=HeapMaxPriorityQueue, extreme_key=MAX)

    def _get_empty_instance(self):
        return self._tested_class()

    def _get_empty_complementary_instance(self):
        return HeapMinPriorityQueue()


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # add test methods as separate tests to test suite
    for test_case in [TestArrayPriorityQueueMIN, TestArrayPriorityQueueMAX,
                      TestArrayMinPriorityQueue, TestArrayMaxPriorityQueue,
                      TestOrderedArrayPriorityQueueMIN,
                      TestOrderedArrayPriorityQueueMAX,
                      TestOrderedArrayMinPriorityQueue,
                      TestOrderedArrayMaxPriorityQueue,
                      TestHeapPriorityQueueMIN, TestHeapPriorityQueueMAX,
                      TestHeapMinPriorityQueue, TestHeapMaxPriorityQueue
    ]:
        for name in unittest.defaultTestLoader.getTestCaseNames(test_case):
            suite.addTest(test_case(name))

    # run the tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
