# Sebastian Thomas (datascience at sebastianthomas dot de)

# custom modules
from lists import *

# unit tests
from unittests.general_tests import *


def test_linked_list(debug=False):
    successes = 0
    failures = 0

    # test LinkedList.Node.__init__
    node1 = LinkedList.Node(1)
    node2 = LinkedList.Node(2, node1)
    node3 = LinkedList.Node(3, node2)
    for passed in [test_equality(node1.value, 1, debug=debug),
                   test_equality(node1.successor, None, debug=debug),
                   test_equality(node2.value, 2, debug=debug),
                   test_equality(node2.successor, node1, debug=debug),
                   test_equality(node3.value, 3, debug=debug),
                   test_equality(node3.successor, node2, debug=debug)]:
        if passed:
            successes += 1
        else:
            failures += 1
    
    return successes, failures


tests = [test_linked_list]
