# Sebastian Thomas (datascience at sebastianthomas dot de)

# custom modules
from datastructures.base import EmptyCollectionException
from datastructures.randomized_queue import *

# unit tests
import unittest


class TestRandomizedQueue(unittest.TestCase):
    def __new__(cls, method_name, tested_class=None):
        if cls is TestRandomizedQueue:
            raise TypeError('Class TestRandomizedQueue may not be '
                            'instantiated.')
        return super().__new__(cls)

    def __init__(self, method_name, tested_class=None):
        super().__init__(methodName=method_name)
        self.tested_class = tested_class

    def setUp(self):
        self.empty_queue = self.tested_class(random_state=0)

        self.queue_length_1 = self.tested_class(random_state=0)
        self.queue_length_1.enqueue(0)

        self.range_queue = self.tested_class(random_state=0)
        self.range_queue += range(4)

        self.queue = self.tested_class(random_state=0)
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

    def test_iter(self):
        self.assertEqual(set(iter(self.empty_queue)), set())
        self.assertEqual(set(iter(self.queue_length_1)), {0})
        self.assertEqual(set(iter(self.range_queue)), {0, 1, 2, 3})
        self.assertEqual(set(iter(self.queue)), {-3, 1, 2, 42})

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
        for _ in range(100):
            self.assertIn(self.range_queue.get(), {0, 1, 2, 3})
        for _ in range(100):
            self.assertIn(self.queue.get(), {-3, 1, 2, 42})

    def test_choice(self):
        with self.assertRaises(EmptyCollectionException):
            self.empty_queue.choice()

        self.assertEqual(self.queue_length_1.choice(), 0)
        for _ in range(100):
            self.assertIn(self.range_queue.choice(), {0, 1, 2, 3})
        for _ in range(100):
            self.assertIn(self.queue.choice(), {-3, 1, 2, 42})

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

        values = {0, 1, 2, 3}
        for _ in range(4):
            self.range_queue.delete()
            for value in self.range_queue:
                self.assertIn(value, values)
        with self.assertRaises(EmptyCollectionException):
            self.range_queue.delete()
        self.assertEqual(self.queue_length_1, queue)

        values = [1, 42, -3, 2, 42]
        for _ in range(5):
            self.queue.delete()
            for value in self.queue:
                self.assertIn(value, values)
        with self.assertRaises(EmptyCollectionException):
            self.queue.delete()
        self.assertEqual(self.queue_length_1, queue)

    def test_clear(self):
        self.empty_queue.clear()
        self.queue_length_1.clear()
        self.range_queue.clear()
        self.queue.clear()

        self.assertEqual(self.empty_queue, self.tested_class())
        self.assertEqual(self.queue_length_1, self.tested_class())
        self.assertEqual(self.range_queue, self.tested_class())
        self.assertEqual(self.queue, self.tested_class())

    def test_dequeue(self):
        with self.assertRaises(EmptyCollectionException):
            self.empty_queue.dequeue()

        self.assertEqual(self.queue_length_1.dequeue(), 0)
        queue = self.tested_class()
        self.assertEqual(self.queue_length_1, queue)

        values = {0, 1, 2, 3}
        for _ in range(4):
            value = self.range_queue.dequeue()
            self.assertIn(value, values)
            values.remove(value)
        with self.assertRaises(EmptyCollectionException):
            self.range_queue.dequeue()

        values = [1, 42, -3, 2, 42]
        for _ in range(5):
            value = self.queue.dequeue()
            self.assertIn(value, values)
            values.remove(value)
        with self.assertRaises(EmptyCollectionException):
            self.queue.dequeue()


class TestArrayRandomizedQueue(TestRandomizedQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name,
                         tested_class=ArrayRandomizedQueue)

    def test_init(self):
        self.assertEqual(self.empty_queue._values, [])
        self.assertEqual(self.queue_length_1._values, [0])
        self.assertEqual(self.range_queue._values, [0, 1, 2, 3])
        self.assertEqual(self.queue._values, [1, 42, -3, 2, 42])

    def test_iter(self):
        super().test_iter()

        self.assertEqual(list(iter(self.range_queue)), [1, 2, 3, 0])
        self.assertEqual(list(iter(self.queue)), [-3, 42, 1, 42, 2])

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

    def test_choice(self):
        super().test_choice()

        self.assertEqual(self.range_queue.choice(), 2)
        self.assertEqual(self.queue.choice(), -3)

    def test_dequeue(self):
        super().test_dequeue()

        self.setUp()

        self.assertEqual(self.range_queue.dequeue(), 3)
        self.assertEqual(self.range_queue.dequeue(), 2)
        self.assertEqual(self.range_queue.dequeue(), 1)
        self.assertEqual(self.range_queue.dequeue(), 0)

        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), -3)
        self.assertEqual(self.queue.dequeue(), 42)
        self.assertEqual(self.queue.dequeue(), 1)
        self.assertEqual(self.queue.dequeue(), 42)


class TestLinkedRandomizedQueue(TestRandomizedQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name,
                         tested_class=LinkedRandomizedQueue)

    def test_init(self):
        self.assertEqual(self.empty_queue._front, None)

        self.assertEqual(self.queue_length_1._front.value, 0)
        self.assertEqual(self.queue_length_1._front.successor, None)

        self.assertEqual(self.range_queue._front.value, 3)
        self.assertEqual(self.range_queue._front.successor.value, 2)
        self.assertEqual(self.range_queue._front.successor.successor.value, 1)
        self.assertEqual(self.range_queue._front.successor.successor.successor
                         .value, 0)
        self.assertEqual(self.range_queue._front.successor.successor.successor
                         .successor, None)

        self.assertEqual(self.queue._front.value, 42)
        self.assertEqual(self.queue._front.successor.value, 2)
        self.assertEqual(self.queue._front.successor.successor.value, -3)
        self.assertEqual(self.queue._front.successor.successor.successor.value,
                         42)
        self.assertEqual(self.queue._front.successor.successor.successor
                         .successor.value, 1)
        self.assertEqual(self.queue._front.successor.successor.successor
                         .successor.successor, None)

    def test_iter(self):
        super().test_iter()

        self.assertEqual(list(iter(self.range_queue)), [1, 0, 3, 2])
        self.assertEqual(list(iter(self.queue)), [-3, 42, 1, 42, 2])

    def test_repr(self):
        class_name = self.tested_class.__name__
        self.assertEqual(repr(self.empty_queue), '{}([])'.format(class_name))
        self.assertEqual(repr(self.queue_length_1),
                         '{}([0])'.format(class_name))
        self.assertEqual(repr(self.range_queue),
                         '{}([3, 2, 1, 0])'.format(class_name))
        self.assertEqual(repr(self.queue),
                         '{}([42, 2, -3, 42, 1])'.format(class_name))

    def test_str(self):
        self.assertEqual(str(self.empty_queue), '')
        self.assertEqual(str(self.queue_length_1), '0')
        self.assertEqual(str(self.range_queue), '3 2 1 0')
        self.assertEqual(str(self.queue), '42 2 -3 42 1')

    def test_choice(self):
        super().test_choice()

        self.assertEqual(self.range_queue.choice(), 1)
        self.assertEqual(self.queue.choice(), -3)

    def test_dequeue(self):
        super().test_dequeue()

        self.setUp()

        self.assertEqual(self.range_queue.dequeue(), 0)
        self.assertEqual(self.range_queue.dequeue(), 1)
        self.assertEqual(self.range_queue.dequeue(), 2)
        self.assertEqual(self.range_queue.dequeue(), 3)

        self.assertEqual(self.queue.dequeue(), 42)
        self.assertEqual(self.queue.dequeue(), -3)
        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), 42)
        self.assertEqual(self.queue.dequeue(), 1)


class TestDoublyLinkedRandomizedQueue(TestRandomizedQueue):
    def __init__(self, method_name):
        super().__init__(method_name=method_name,
                         tested_class=DoublyLinkedRandomizedQueue)

    def test_init(self):
        self.assertEqual(self.empty_queue._current_node, None)

        self.assertEqual(self.queue_length_1._current_node.value, 0)
        self.assertEqual(self.queue_length_1._current_node.predecessor,
                         self.queue_length_1._current_node)
        self.assertEqual(self.queue_length_1._current_node.successor,
                         self.queue_length_1._current_node)

        self.assertEqual(self.range_queue._current_node.value, 3)
        self.assertEqual(self.range_queue._current_node.predecessor.value, 0)
        self.assertEqual(self.range_queue._current_node.successor.value, 2)
        self.assertEqual(self.range_queue._current_node.successor.predecessor
                         .value, 3)
        self.assertEqual(self.range_queue._current_node.successor.successor
                         .value, 1)
        self.assertEqual(self.range_queue._current_node.successor.successor
                         .predecessor.value, 2)
        self.assertEqual(self.range_queue._current_node.successor.successor
                         .successor.value, 0)
        self.assertEqual(self.range_queue._current_node.successor.successor
                         .successor.predecessor.value, 1)
        self.assertEqual(self.range_queue._current_node.successor.successor
                         .successor.successor, self.range_queue._current_node)

        self.assertEqual(self.queue._current_node.value, 42)
        self.assertEqual(self.queue._current_node.predecessor.value, 1)
        self.assertEqual(self.queue._current_node.successor.value, 2)
        self.assertEqual(self.queue._current_node.successor.predecessor.value,
                         42)
        self.assertEqual(self.queue._current_node.successor.successor.value,
                         -3)
        self.assertEqual(self.queue._current_node.successor.successor
                         .predecessor.value, 2)
        self.assertEqual(self.queue._current_node.successor.successor
                         .successor.value, 42)
        self.assertEqual(self.queue._current_node.successor.successor.successor
                         .predecessor.value, -3)
        self.assertEqual(self.queue._current_node.successor.successor.successor
                         .successor.value, 1)
        self.assertEqual(self.queue._current_node.successor.successor.successor
                         .successor.predecessor.value, 42)
        self.assertEqual(self.queue._current_node.successor.successor.successor
                         .successor.successor, self.queue._current_node)

    def test_iter(self):
        super().test_iter()

        self.assertEqual(list(iter(self.range_queue)), [1, 0, 3, 2])
        self.assertEqual(list(iter(self.queue)), [2, -3, 42, 1, 42])

    def test_repr(self):
        class_name = self.tested_class.__name__
        self.assertEqual(repr(self.empty_queue), '{}([])'.format(class_name))
        self.assertEqual(repr(self.queue_length_1),
                         '{}([0])'.format(class_name))
        self.assertEqual(repr(self.range_queue),
                         '{}([3, 2, 1, 0])'.format(class_name))
        self.assertEqual(repr(self.queue),
                         '{}([42, 2, -3, 42, 1])'.format(class_name))

    def test_str(self):
        self.assertEqual(str(self.empty_queue), '')
        self.assertEqual(str(self.queue_length_1), '0')
        self.assertEqual(str(self.range_queue), '3 2 1 0')
        self.assertEqual(str(self.queue), '42 2 -3 42 1')

    def test_choice(self):
        super().test_choice()

        self.assertEqual(self.range_queue.choice(), 3)
        self.assertEqual(self.queue.choice(), 1)

    def test_dequeue(self):
        super().test_dequeue()

        self.setUp()

        self.assertEqual(self.range_queue.dequeue(), 0)
        self.assertEqual(self.range_queue.dequeue(), 1)
        self.assertEqual(self.range_queue.dequeue(), 2)
        self.assertEqual(self.range_queue.dequeue(), 3)

        self.assertEqual(self.queue.dequeue(), 42)
        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), 1)
        self.assertEqual(self.queue.dequeue(), 42)
        self.assertEqual(self.queue.dequeue(), -3)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # add test methods as separate tests to test suite
    for test_case in [TestArrayRandomizedQueue, TestLinkedRandomizedQueue,
                      TestDoublyLinkedRandomizedQueue]:
        for name in unittest.defaultTestLoader.getTestCaseNames(test_case):
            suite.addTest(test_case(name))

    # run the tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
