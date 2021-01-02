# Sebastian Thomas (datascience at sebastianthomas dot de)

# copying objects
from copy import copy

# unit tests
import unittest

# custom modules
from datastructures.stack import *


class TestStack(unittest.TestCase):
    def __new__(cls, method_name, tested_class=None):
        if cls is TestStack:
            raise TypeError('Class TestStack may not be instantiated.')
        return super().__new__(cls)

    def __init__(self, method_name, tested_class=None):
        super().__init__(methodName=method_name)
        self.tested_class = tested_class

    def setUp(self):
        self.empty_stack = self.tested_class()

        self.stack_length_1 = self.tested_class()
        self.stack_length_1.push(0)

        self.range_stack = self.tested_class()
        self.range_stack += range(4)

        self.stack = self.tested_class()
        self.stack += [1, 42, -3, 2, 42]

    def test_eq(self):
        stack = self.tested_class()
        self.assertEqual(self.empty_stack, stack)
        stack = self.tested_class()
        stack += [0]
        self.assertEqual(self.stack_length_1, stack)
        stack = self.tested_class()
        stack += range(4)
        self.assertEqual(self.range_stack, stack)
        stack = self.tested_class()
        stack += [1, 42, -3, 2, 42]
        self.assertEqual(self.stack, stack)

        self.assertNotEqual(self.empty_stack, self.stack_length_1)
        self.assertNotEqual(self.stack_length_1, self.range_stack)
        self.assertNotEqual(self.range_stack, self.stack)
        self.assertNotEqual(self.stack, self.empty_stack)
        self.assertNotEqual(self.empty_stack, [])
        self.assertNotEqual(self.stack_length_1, [0])
        self.assertNotEqual(self.range_stack, range(4))
        self.assertNotEqual(self.stack, [1, 42, -3, 2, 42])

    def test_copy(self):
        self.assertEqual(copy(self.empty_stack), self.empty_stack)
        self.assertEqual(copy(self.stack_length_1), self.stack_length_1)
        self.assertEqual(copy(self.range_stack), self.range_stack)
        self.assertEqual(copy(self.stack), self.stack)

    def test_iter(self):
        self.assertEqual(list(iter(self.empty_stack)), [])
        self.assertEqual(list(iter(self.stack_length_1)), [0])
        self.assertEqual(list(iter(self.range_stack)), [3, 2, 1, 0])
        self.assertEqual(list(iter(self.stack)), [42, 2, -3, 42, 1])

    def test_bool(self):
        self.assertFalse(bool(self.empty_stack))
        self.assertTrue(bool(self.stack_length_1))
        self.assertTrue(bool(self.range_stack))
        self.assertTrue(bool(self.stack))

    def test_len(self):
        self.assertEqual(len(self.empty_stack), 0)
        self.assertEqual(len(self.stack_length_1), 1)
        self.assertEqual(len(self.range_stack), 4)
        self.assertEqual(len(self.stack), 5)

    def test_repr(self):
        class_name = self.tested_class.__name__
        self.assertEqual(repr(self.empty_stack), '{}([])'.format(class_name))
        self.assertEqual(repr(self.stack_length_1),
                         '{}([0])'.format(class_name))
        self.assertEqual(repr(self.range_stack),
                         '{}([3, 2, 1, 0])'.format(class_name))
        self.assertEqual(repr(self.stack),
                         '{}([42, 2, -3, 42, 1])'.format(class_name))

    def test_str(self):
        self.assertEqual(str(self.empty_stack), '')
        self.assertEqual(str(self.stack_length_1), '0')
        self.assertEqual(str(self.range_stack), '3 2 1 0')
        self.assertEqual(str(self.stack), '42 2 -3 42 1')

    def test_contains(self):
        self.assertFalse(0 in self.empty_stack)
        self.assertTrue(0 in self.stack_length_1)
        self.assertFalse(1 in self.stack_length_1)
        self.assertFalse('0' in self.stack_length_1)
        self.assertTrue(0 in self.range_stack)
        self.assertTrue(1 in self.range_stack)
        self.assertTrue(2 in self.range_stack)
        self.assertTrue(3 in self.range_stack)
        self.assertFalse(-1 in self.range_stack)
        self.assertFalse(4 in self.range_stack)
        self.assertFalse('0' in self.range_stack)
        self.assertFalse('1' in self.range_stack)
        self.assertFalse('2' in self.range_stack)
        self.assertFalse('3' in self.range_stack)
        self.assertTrue(-3 in self.stack)
        self.assertTrue(1 in self.stack)
        self.assertTrue(2 in self.stack)
        self.assertTrue(42 in self.stack)
        self.assertFalse(0 in self.stack)
        self.assertFalse('-3' in self.stack)
        self.assertFalse('1' in self.stack)
        self.assertFalse('2' in self.stack)
        self.assertFalse('42' in self.stack)

    def test_iadd(self):
        with self.assertRaises(TypeError):
            self.empty_stack += 2
        with self.assertRaises(TypeError):
            self.stack_length_1 += 2.5
        with self.assertRaises(TypeError):
            self.range_stack += True
        with self.assertRaises(TypeError):
            self.stack += None

        id_empty_stack = id(self.empty_stack)
        id_stack_length_1 = id(self.stack_length_1)
        id_range_stack = id(self.range_stack)
        id_stack = id(self.stack)

        self.empty_stack += self.stack_length_1
        self.stack_length_1 += self.range_stack
        self.range_stack += self.stack
        self.stack += self.empty_stack

        self.assertEqual(id(self.empty_stack), id_empty_stack)
        self.assertEqual(id(self.stack_length_1), id_stack_length_1)
        self.assertEqual(id(self.range_stack), id_range_stack)
        self.assertEqual(id(self.stack), id_stack)

        stack = self.tested_class()
        stack += [0]
        self.assertEqual(self.empty_stack, stack)
        stack = self.tested_class()
        stack += [0, 3, 2, 1, 0]
        self.assertEqual(self.stack_length_1, stack)
        stack = self.tested_class()
        stack += [0, 1, 2, 3, 42, 2, -3, 42, 1]
        self.assertEqual(self.range_stack, stack)
        stack = self.tested_class()
        stack += [1, 42, -3, 2, 42, 0]
        self.assertEqual(self.stack, stack)

        self.empty_stack += [-1, -1]
        self.stack_length_1 += tuple('stack')
        self.range_stack += (-1, -2, -3)
        self.stack += []

        self.assertEqual(id(self.empty_stack), id_empty_stack)
        self.assertEqual(id(self.stack_length_1), id_stack_length_1)
        self.assertEqual(id(self.range_stack), id_range_stack)
        self.assertEqual(id(self.stack), id_stack)
        stack = self.tested_class()
        stack += [0, -1, -1]
        self.assertEqual(self.empty_stack, stack)
        stack = self.tested_class()
        stack += [0, 3, 2, 1, 0, 's', 't', 'a', 'c', 'k']
        self.assertEqual(self.stack_length_1, stack)
        stack = self.tested_class()
        stack += [0, 1, 2, 3, 42, 2, -3, 42, 1, -1, -2, -3]
        self.assertEqual(self.range_stack, stack)
        stack = self.tested_class()
        stack += [1, 42, -3, 2, 42, 0]
        self.assertEqual(self.stack, stack)

    def test_is_empty(self):
        self.assertTrue(self.empty_stack.is_empty())
        self.assertFalse(self.stack_length_1.is_empty())
        self.assertFalse(self.range_stack.is_empty())
        self.assertFalse(self.stack.is_empty())

    def test_peek(self):
        with self.assertRaises(EmptyStackException):
            self.empty_stack.peek()

        self.assertEqual(self.stack_length_1.peek(), 0)
        self.assertEqual(self.range_stack.peek(), 3)
        self.assertEqual(self.stack.peek(), 42)

    def test_push(self):
        self.empty_stack.push(-1)
        self.stack_length_1.push(-1)
        self.stack_length_1.push(-2)
        self.range_stack.push(-1)
        self.range_stack.push(-2)
        self.range_stack.push(-3)
        self.stack.push(-1)
        self.stack.push(-2)
        self.stack.push(-3)

        stack = self.tested_class()
        stack += [-1]
        self.assertEqual(self.empty_stack, stack)
        stack = self.tested_class()
        stack += [0, -1, -2]
        self.assertEqual(self.stack_length_1, stack)
        stack = self.tested_class()
        stack += [0, 1, 2, 3, -1, -2, -3]
        self.assertEqual(self.range_stack, stack)
        stack = self.tested_class()
        stack += [1, 42, -3, 2, 42, -1, -2, -3]
        self.assertEqual(self.stack, stack)

    def test_pop(self):
        with self.assertRaises(EmptyStackException):
            self.empty_stack.pop()

        self.stack_length_1.pop()
        self.range_stack.pop()
        self.range_stack.pop()
        self.stack.pop()
        self.stack.pop()

        stack = self.tested_class()
        self.assertEqual(self.stack_length_1, stack)
        stack = self.tested_class()
        stack += [0, 1]
        self.assertEqual(self.range_stack, stack)
        stack = self.tested_class()
        stack += [1, 42, -3]
        self.assertEqual(self.stack, stack)

        self.stack.pop()
        self.stack.pop()
        self.stack.pop()
        with self.assertRaises(EmptyStackException):
            self.stack.pop()

    def test_clear(self):
        self.empty_stack.clear()
        self.stack_length_1.clear()
        self.range_stack.clear()
        self.stack.clear()

        self.assertEqual(self.empty_stack, self.tested_class())
        self.assertEqual(self.stack_length_1, self.tested_class())
        self.assertEqual(self.range_stack, self.tested_class())
        self.assertEqual(self.stack, self.tested_class())


class TestArrayStack(TestStack):
    def __init__(self, method_name):
        super().__init__(method_name=method_name, tested_class=ArrayStack)

    def test_init(self):
        self.assertEqual(self.empty_stack._values, [])
        self.assertEqual(self.stack_length_1._values, [0])
        self.assertEqual(self.range_stack._values, [0, 1, 2, 3])
        self.assertEqual(self.stack._values, [1, 42, -3, 2, 42])


class TestLinkedStack(TestStack):
    def __init__(self, method_name):
        super().__init__(method_name=method_name, tested_class=LinkedStack)

    def test_init(self):
        self.assertEqual(self.empty_stack._top, None)

        self.assertEqual(self.stack_length_1._top.value, 0)
        self.assertEqual(self.stack_length_1._top.successor, None)

        self.assertEqual(self.range_stack._top.value, 3)
        self.assertEqual(self.range_stack._top.successor.value, 2)
        self.assertEqual(self.range_stack._top.successor.successor.value, 1)
        self.assertEqual(self.range_stack._top.successor.successor.successor
                         .value, 0)
        self.assertEqual(self.range_stack._top.successor.successor.successor
                         .successor, None)

        self.assertEqual(self.stack._top.value, 42)
        self.assertEqual(self.stack._top.successor.value, 2)
        self.assertEqual(self.stack._top.successor.successor.value, -3)
        self.assertEqual(self.stack._top.successor.successor.successor.value,
                         42)
        self.assertEqual(self.stack._top.successor.successor.successor
                         .successor.value, 1)
        self.assertEqual(self.stack._top.successor.successor.successor
                         .successor.successor, None)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # add test methods as separate tests to test suite
    for test_case in [TestArrayStack, TestLinkedStack]:
        for name in unittest.defaultTestLoader.getTestCaseNames(test_case):
            suite.addTest(test_case(name))

    # run the tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
