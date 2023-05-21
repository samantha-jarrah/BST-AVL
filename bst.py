# Name: Samantha Jarrah
# OSU Email: jarrahs@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 5/22/23
# Description: Contains BST node class as well as BST class which has the following methods: _str_helper(), get_root(),
# is_valid_bst(), add(), remove(), _remove_no_subtrees(), _remove_one_subtree(), _remove_two_subtrees(), _find_inorder_successor(),
# contains(), inorder_traversal(), _helper_traversal(), find_min(), find_max(), is_empty(), make_empty()

import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new node with passed value to a BST
        If BST is empty, the root is set to the new node
        Duplicate values are added to the right subtree of its duplicate node
        Time Complexity: O(n)
        """
        parent = None
        current_node = self._root

        # searches for the new node's position
        while current_node is not None:
            parent = current_node
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # BST is empty
        if parent is None:
            self._root = BSTNode(value)
        elif value < parent.value:
            parent.left = BSTNode(value)
        else:
            parent.right = BSTNode(value)

    def remove(self, value: object) -> bool:
        """
        Removes the first node with the passed value
        Handles removing a node with 0, 1, and 2 subtrees
        If BST is empty, returns False
        Time Complexity: O(n)
        """
        current_node, parent_node = self._root, self._root

        # BST is empty
        if self._root is None:
            return False

        #TODO: see if we can simplify
        # if self._root.value == value:
        #     self._remove_root()
        #     return True
            # # root was only node
            # if self._root.right is None and self._root.left is None:
            #     self._root = None
            #     return True
            # # no right subtree
            # elif self._root.right is None:
            #     self._root = self._root.left
            #     return True
            # # no left subtree
            # elif self._root.left is None:
            #     new_root = self._root.right
            #     self._root = new_root
            #     self._root.left, self._root.right = new_root.left, new_root.right
            #     return True
            # # both right and left subtrees
            # else:
            #     inorder_successor, inorder_parent = self._root.right, self._root
            #
            #     while inorder_successor.left is not None:
            #         inorder_successor = inorder_successor.left
            #         if inorder_parent == self._root:
            #             inorder_parent = inorder_parent.right
            #         else:
            #             inorder_parent = inorder_parent.left
            #
            #     # replace root node with inorder successor
            #     inorder_parent.left = inorder_successor.right
            #     inorder_successor.right, inorder_successor.left = self._root.right, self._root.left
            #     self._root = inorder_successor
            #     return True
        # find node with value to be removed and its parent
        while current_node.value != value:
            # value is less, move left
            if value < current_node.value:
                parent_node, current_node = current_node, current_node.left
                # did not find value
                if current_node is None:
                    return False
            # value is greater, move right
            else:
                parent_node, current_node = current_node, current_node.right
                # did not find value
                if current_node is None:
                    return False

        # two subtrees exist
        if current_node.left and current_node.right:
            self._remove_two_subtrees(parent_node, current_node)
            return True
        # 1 subtree exists
        elif current_node.left or current_node.right:
            self._remove_one_subtree(parent_node, current_node)
            return True
        # no subtrees
        else:
            self._remove_no_subtrees(parent_node, current_node)
            return True

    # def _remove_root(self):
    #     # root is only node
    #     if self._root.right is None and self._root.left is None:
    #         self._root = None
    #     # no right subtree
    #     elif self._root.right is None:
    #         self._root = self._root.left
    #     # no left subtree
    #     elif self._root.left is None:
    #         new_root = self._root.right
    #         self._root = new_root
    #         self._root.left, self._root.right = new_root.left, new_root.right
    #     # both right and left subtrees
    #     else:
    #         inorder_successor, inorder_parent = self._root.right, self._root
    #
    #         while inorder_successor.left is not None:
    #             inorder_successor = inorder_successor.left
    #             if inorder_parent == self._root:
    #                 inorder_parent = inorder_parent.right
    #             else:
    #                 inorder_parent = inorder_parent.left
    #
    #         # replace root node with inorder successor
    #         inorder_parent.left = inorder_successor.right
    #         inorder_successor.right, inorder_successor.left = self._root.right, self._root.left
    #         self._root = inorder_successor

    def _remove_no_subtrees(self, parent_node: BSTNode, remove_node: BSTNode) -> None:
        """
        Remove a node that has no subtrees
        Time Complexity: O(1)
        """
        # check if node being removed is root
        if remove_node == self._root:
            self.make_empty()
        # check if the node was the parent's left or right child, then remove it
        elif parent_node.left == remove_node:
            parent_node.left = None
        else:
            parent_node.right = None

    def _remove_one_subtree(self, parent_node: BSTNode, remove_node: BSTNode) -> None:
        """
        Remove node that has a left or right tree but not both
        Time Complexity: O(1)
        """
        # remove_node is root
        if remove_node == self._root:
            if remove_node.right:
                self._root = remove_node.right
            else:
                self._root = remove_node.left

        # remove_node is a left child
        elif parent_node.left == remove_node:
            # is there a left or right subtree
            if remove_node.left:
                parent_node.left = remove_node.left
            else:
                parent_node.left = remove_node.right

        # remove_node is a right child
        else:
            # is there a left or right subtree
            if remove_node.left:
                parent_node.right = remove_node.left
            else:
                parent_node.right = remove_node.right

    def _remove_two_subtrees(self, parent_node: BSTNode, remove_node: BSTNode) -> None:
        """
        Remove node that has two subtrees
        Must find the inorder successor and inorder successor parent
        Time Complexity:O(n)
        """
        if remove_node.right.left is None:
            inorder_successor, inorder_parent = remove_node.right, remove_node
        else:
            inorder_successor, inorder_parent = self._find_inorder_successor(remove_node)

        # is remove_node a left or right child
        if parent_node.left == remove_node:
            # replace remove_node with inorder successor and update pointers
            if inorder_parent == remove_node:
                inorder_successor.left, parent_node.left = remove_node.left, inorder_successor
            else:
                inorder_parent.left = inorder_successor.right
                inorder_successor.right, inorder_successor.left = remove_node.right, remove_node.left
                parent_node.left = inorder_successor

        # handles remove_node being root or right child
        else:
            # replace remove_node with inorder_successor and update pointers
            if remove_node == self._root:
                if inorder_parent == remove_node:
                    inorder_successor.left, self._root = self._root.left, inorder_successor
                else:
                    inorder_successor.left, inorder_parent.left = self._root.left, inorder_successor.right
                    inorder_successor.right = self._root.right
                    self._root = inorder_successor
            elif inorder_parent == remove_node:
                inorder_successor.left, parent_node.right = remove_node.left, inorder_successor
            else:
                inorder_parent.left = inorder_successor.right
                inorder_successor.left, inorder_successor.right = remove_node.left, remove_node.right
                parent_node.right = inorder_successor

    def _find_inorder_successor(self, remove_node):
        """
        Finds and returns the inorder_successor and inorder successors' parent of passed remove node
        Time Complexity: O(n)
        """
        inorder_successor, inorder_parent = remove_node.right.left, remove_node.right
        while inorder_successor.left is not None:
            inorder_successor = inorder_successor.left
            inorder_parent = inorder_parent.left
        return inorder_successor, inorder_parent

    def contains(self, value: object) -> bool:
        """
        Returns True if BST contains the passed value, otherwise False
        Time Complexity: O(n)
        """
        current_node = self._root

        # searches for node containing passed value
        while current_node is not None:
            if current_node.value == value:
                return True
            elif value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right
        # value was not found
        return False

    def inorder_traversal(self) -> Queue:
        """
        Performs an inorder traversal of a BST
        Returns a queue object with the values of the visited nodes
        Returns an empty queue is BST is empty
        Time Complexity: O(n)
        """
        current_node = self._root
        tree_queue = Queue()
        if current_node is None:
            return tree_queue
        self._helper_traversal(current_node, tree_queue)
        return tree_queue

    def _helper_traversal(self, current_node, queue):
        """
        Recursive method to traverse and fill a queue with the inorder nodes' values
        Time Complexity: O(n)
        """
        # base case
        if current_node is None:
            return

        self._helper_traversal(current_node.left, queue)
        queue.enqueue(current_node.value)
        self._helper_traversal(current_node.right, queue)

    # def inorder_traversal(self) -> Queue:
    #     """
    #         TODO: Write your implementation
    #         """
    #     # temp_stack will keep track of the nodes that have been visited already
    #     temp_stack = Stack()
    #
    #     # queue will hold node values after in-order traversal
    #     tree_queue = Queue()
    #
    #     current_node = self._root
    #     if current_node is None:
    #         return tree_queue
    #
    #     self.helper_traversal(current_node, temp_stack, tree_queue)
    #     return tree_queue
    #
    # def helper_traversal(self, node, stack, queue):
    #     """
    #
    #     """
    #     # traverse left
    #     while node.left is not None:
    #         stack.push(node)
    #         node = node.left
    #
    #     # once you have gone as far left as possible, add the node to the queue
    #     queue.enqueue(node.value)
    #
    #     # processing while there are nodes in the stack
    #     while stack.is_empty() is False:
    #         if node.right is not None:
    #             node = node.right
    #             return self.helper_traversal(node, stack, queue)
    #         elif stack.is_empty() is False:
    #             node = stack.pop()
    #             queue.enqueue(node.value)
    #
    #     # check if there is a branch to the right
    #     if node.right is None:
    #         return queue
    #     else:
    #         node = node.right
    #         return self.helper_traversal(node, stack, queue)

    def find_min(self) -> object:
        """
        Returns the node with the minimum value by traversing as far left as possible
        Time Complexity: O(n)
        """
        if self._root is None:
            return None
        current_node = self._root

        while current_node.left is not None:
            current_node = current_node.left

        return current_node.value

    def find_max(self) -> object:
        """
        Returns the node with the maximum value by traversing as far right as possible
        Time Complexity: O(n)
        """
        if self._root is None:
            return None

        current_node = self._root

        while current_node.right is not None:
            current_node = current_node.right

        return current_node.value

    def is_empty(self) -> bool:
        """
        Returns True if the BST is empty, otherwise False
        Time Complexity: O(1)
        """
        if self.get_root() is None:
            return True
        return False

    def make_empty(self) -> None:
        """
        Empties a BST by setting the root to None
        Time Complexity: O(1)
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        # ((1, 2, 3), 1),
        # ((1, 2, 3), 2),
        # ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 50),
        # ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        # ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        # ((50, 40, 60, 30, 70, 20, 80, 45), 30),
        # ((-95, -91, 81, 50, -45, 84, -42, -6, -4, -67), -95),
        # ((-95, -91, 81, 50, -45, 84, -42, -6, -4, -67), 81),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        # ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        # ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        # ((50, 40, 60, 30, 70, 20, 80, 35), 20),
         ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((-61, -58, -21, -45, -42, 26, 91, 29), -61),
        ((-58, -21, -45, -42, 26, 91, 29), -21),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    # tree = BST([-46748, -69908, -69908, -59039, -69908, -69908, -58342, 87908, -38954, -46748, -46748, -46748, 16439, -38954, 87908, 98584])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
