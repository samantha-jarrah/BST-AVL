# Name: Samantha Jarrah
# OSU Email: jarrahs@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 5/21/23
# Description: Contains AVLNode class which inherits from BSTNode. Also, contains AVL class with all the necessary
# methods to add and remove nodes, keeping the tree balanced after every change.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    print("is_valid_avl failed")
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        print("is_valid_avl failed")
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        print("is_valid_avl failed")
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new AVLNode with the passed value
        No duplicates allowed
        Handles all necessary rotations for self-balancing
        Time Complexity: O(log n)
        """
        parent = None
        current_node = self._root

        # searches for the new node's position
        while current_node is not None:
            parent = current_node
            # no duplicates allowed
            if value == current_node.value:
                return
            elif value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # AVL is empty
        if parent is None:
            new_node = AVLNode(value)
            self._root = new_node

        # insert left
        elif value < parent.value:
            new_node = AVLNode(value)
            parent.left = new_node
            new_node.parent = parent

        # insert right
        else:
            new_node = AVLNode(value)
            parent.right = new_node
            new_node.parent = parent

        while parent is not None:
            self._rebalance(parent)
            parent = parent.parent

    def remove(self, value: object) -> bool:
        """
        TODO: Write your implementation
        """
        parent = None
        current_node = self._root

        # node to remove is root
        if current_node.value == value:
            # root has 2 subtrees
            if current_node.left and current_node.right:
                pass
            # root has 1 subtree
            elif current_node.left or current_node.right:
                # left subtree
                if current_node.left:
                    self._root = current_node.left
                    self._root.left = None
                    self._root.right = None
                    self._root.parent = None
                # right subtree
                if current_node.right:
                    self._root = current_node.right
                    self._root.left = None
                    self._root.right = None
                    self._root.parent = None
            # root has 0 subtrees
            else:
                self.make_empty()
            return True

    # Experiment and see if you can use the optional                         #
    # subtree removal methods defined in the BST here in the AVL.            #
    # Call normally using self -> self._remove_no_subtrees(parent, node)     #
    # You need to override the _remove_two_subtrees() method in any case.    #
    # Remove these comments.                                                 #
    # Remove these method stubs if you decide not to use them.               #
    # Change this method in any way you'd like.                              #

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        TODO: Write your implementation
        """
        pass

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Returns the balance factor of the passed node
        Time Complexity: O(1)
        """
        if node.right is None:
            r_height = -1
        else:
            r_height = node.right.height

        if node.left is None:
            l_height = -1
        else:
            l_height = node.left.height
        return r_height - l_height

    def _get_height(self, node: AVLNode) -> int:
        """
        Returns the height of the passed node
        Time Complexity: O(1)
        """
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Rotates left around the passed node
        Returns either self._root or the child of the passed node
        Time Complexity:O(1)
        """

        if node == self._root:
            self._root = node.right
            node.right = self._root.left
            if self._root.left:
                self._root.left.parent = node
            self._root.left = node
            self._root.left.parent = node
            node.parent = self._root
            self._update_height(node)
            self._update_height(self._root)
            return self._root

        else:
            child = node.right
            node.right = child.left
            if node.right:
                node.right.parent = node
            child.left = node
            node.parent = child
            self._update_height(node)
            self._update_height(child)
            return child

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Rotates right around the passed node
        Returns either self._root or the child of the passed node
        Time Complexity:O(1)
        """

        if node == self._root:
            self._root = node.left
            node.left = self._root.right
            if self._root.right:
                self._root.right.parent = node
            self._root.right = node
            node.parent = self._root
            self._update_height(node)
            self._update_height(self._root)
            return self._root

        else:
            child = node.left
            node.left = child.right
            if node.left:
                node.left.parent = node
            child.right = node
            node.parent = child
            self._update_height(node)
            self._update_height(child)
            return child

    def _update_height(self, node: AVLNode, ) -> None:
        """
        Updates the height of the passed node
        Time Complexity: O(1)
        """
        if node.left:
            lHeight = node.left.height
        else:
            lHeight = -1

        if node.right:
            rHeight = node.right.height
        else:
            rHeight = -1
        # calculate and set new height
        node.height = max(lHeight, rHeight) + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        Traverse through node's parents and determine if any nodes are unbalanced
        If nodes are unbalanced, determine the correct rotations necessary
        Time Complexity: O(n)
        """
        bal_fac = self._balance_factor(node)
        # subtree is unbalanced
            # if bal_fac < -1 or bal_fac > 1:
            #     # L-L
            #     if bal_fac < -1 and self._balance_factor(node.left) < 0:
            #         self._rotate_right(node)
            #     # R-R
            #     elif bal_fac > 1 and self._balance_factor(node.right) > 0:
            #         self._rotate_left(node)
            #     # L-R
            #     elif bal_fac < -1 and self._balance_factor(node.left) > 0:
            #         self._rotate_left(node.right)
            #         self._rotate_right(node)
            #     # R-L
            #     else:
            #         #TODO: check that this is the right nodes to be passing
            #         self._rotate_right(node.left)
            #         self._rotate_left(node)
        if bal_fac < -1:
            # L-R imbalance
            if self._balance_factor(node.left) > 0:
                node.left = self._rotate_left(node.left)
                node.left.parent = node
            node_par = node.parent
            # if node_par is not None:
            #     node_par.right = None   # JUST ADDED
            new_subtree_root = self._rotate_right(node)
            new_subtree_root.parent = node_par
            if node_par:
                if new_subtree_root.value < node_par.value:
                    node_par.left = new_subtree_root
                else:
                    node_par.right = new_subtree_root

        elif bal_fac > 1:
            # R-L imbalance
            if self._balance_factor(node.right) < 0:
                node.right = self._rotate_right(node.right)
                node.right.parent = node
            node_par = node.parent
            # if node_par is not None:
            #     node_par.left = None  # JUST ADDED
            new_subtree_root = self._rotate_left(node)
            new_subtree_root.parent = node_par
            if node_par:
                if new_subtree_root.value < node_par.value:
                    node_par.left = new_subtree_root
                else:
                    node_par.right = new_subtree_root
        else:
            self._update_height(node)

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':
    #
    # print("\nPDF - method add() example 1")
    # print("----------------------------")
    # test_cases = (
    #     (50, 40, 60, 30, 70, 20), #LL-not root
    #     # (50, 40, 60, 70, 80), #RR-not root
    #     # (1, 3, 6, 9, 12, 15, 18, 21, 24, 27),
    #     # (1, 2, 3),  # RR - root
    #     # (3, 2, 1),  # LL - root
    #     #  (1, 3, 2),  # RL
    #     # (3, 1, 2),  # LR
    # )
    # for case in test_cases:
    #     tree = AVL(case)
    #     print(tree)

    # print("\nPDF - method add() example 2")
    # print("----------------------------")
    # test_cases = (
        # (10, 20, 30, 40, 50),   # RR, RR
        # (10, 20, 30, 50, 40),   # RR, RL
        # (30, 20, 10, 5, 1),     # LL, LL
        # (30, 20, 10, 1, 5),     # LL, LR
        # (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        # (range(0, 30, 3)),
        # (range(0, 31, 3)),
        # (range(0, 34, 3)),
        # (range(10, -10, -2)),
        # ('A', 'B', 'C', 'D', 'E'),
        # (1, 1, 1, 1),    #repeated values
    # )
    # for case in test_cases:
    #     tree = AVL(case)
    #     print('INPUT  :', case)
    #     print('RESULT :', tree)

    # print("\nPDF - method add() example 3")
    # print("----------------------------")
    # for _ in range(100):
    #     # case = list(set(random.randrange(1, 101) for _ in range(10)))
    #     case = [65, 97, 8, 76, 15, 82, 20, 86, 26]
    #     print(case)
    #     tree = AVL()
    #     for value in case:
    #         tree.add(value)
    #     print(tree)
        # if not tree.is_valid_avl():
        #     raise Exception("PROBLEM WITH ADD OPERATION")
    # print('add() stress test finished')
    #
    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        # ((1,), 1),  #remove root which is only node
        # ((1, 2), 1),   #remove root with right subtree
        # ((3, 2), 3),  # remove root with left subtree
        # ((1, 2, 3), 1),  # no AVL rotation
        # ((1, 2, 3), 2),  # no AVL rotation
        # ((1, 2, 3), 3),  # no AVL rotation
        # ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        # ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        # ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        # ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
    #
    # print("\nPDF - method remove() example 2")
    # print("-------------------------------")
    # test_cases = (
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
    #     ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
    #     ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
    #     ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    # )
    # for case, del_value in test_cases:
    #     tree = AVL(case)
    #     print('INPUT  :', tree, "DEL:", del_value)
    #     tree.remove(del_value)
    #     print('RESULT :', tree)
    #
    # print("\nPDF - method remove() example 3")
    # print("-------------------------------")
    # case = range(-9, 16, 2)
    # tree = AVL(case)
    # for del_value in case:
    #     print('INPUT  :', tree, del_value)
    #     tree.remove(del_value)
    #     print('RESULT :', tree)
    #
    # print("\nPDF - method remove() example 4")
    # print("-------------------------------")
    # case = range(0, 34, 3)
    # tree = AVL(case)
    # for _ in case[:-2]:
    #     root_value = tree.get_root().value
    #     print('INPUT  :', tree, root_value)
    #     tree.remove(root_value)
    #     print('RESULT :', tree)
    #
    # print("\nPDF - method remove() example 5")
    # print("-------------------------------")
    # for _ in range(100):
    #     case = list(set(random.randrange(1, 20000) for _ in range(900)))
    #     tree = AVL(case)
    #     for value in case[::2]:
    #         tree.remove(value)
    #     if not tree.is_valid_avl():
    #         raise Exception("PROBLEM WITH REMOVE OPERATION")
    # print('remove() stress test finished')
    #
    # print("\nPDF - method contains() example 1")
    # print("---------------------------------")
    # tree = AVL([10, 5, 15])
    # print(tree.contains(15))
    # print(tree.contains(-10))
    # print(tree.contains(15))
    #
    # print("\nPDF - method contains() example 2")
    # print("---------------------------------")
    # tree = AVL()
    # print(tree.contains(0))
    #
    # print("\nPDF - method inorder_traversal() example 1")
    # print("---------------------------------")
    # tree = AVL([10, 20, 5, 15, 17, 7, 12])
    # print(tree.inorder_traversal())
    #
    # print("\nPDF - method inorder_traversal() example 2")
    # print("---------------------------------")
    # tree = AVL([8, 10, -4, 5, -1])
    # print(tree.inorder_traversal())
    #
    # print("\nPDF - method find_min() example 1")
    # print("---------------------------------")
    # tree = AVL([10, 20, 5, 15, 17, 7, 12])
    # print(tree)
    # print("Minimum value is:", tree.find_min())
    #
    # print("\nPDF - method find_min() example 2")
    # print("---------------------------------")
    # tree = AVL([8, 10, -4, 5, -1])
    # print(tree)
    # print("Minimum value is:", tree.find_min())
    #
    # print("\nPDF - method find_max() example 1")
    # print("---------------------------------")
    # tree = AVL([10, 20, 5, 15, 17, 7, 12])
    # print(tree)
    # print("Maximum value is:", tree.find_max())
    #
    # print("\nPDF - method find_max() example 2")
    # print("---------------------------------")
    # tree = AVL([8, 10, -4, 5, -1])
    # print(tree)
    # print("Maximum value is:", tree.find_max())
    #
    # print("\nPDF - method is_empty() example 1")
    # print("---------------------------------")
    # tree = AVL([10, 20, 5, 15, 17, 7, 12])
    # print("Tree is empty:", tree.is_empty())
    #
    # print("\nPDF - method is_empty() example 2")
    # print("---------------------------------")
    # tree = AVL()
    # print("Tree is empty:", tree.is_empty())
    #
    # print("\nPDF - method make_empty() example 1")
    # print("---------------------------------")
    # tree = AVL([10, 20, 5, 15, 17, 7, 12])
    # print("Tree before make_empty():", tree)
    # tree.make_empty()
    # print("Tree after make_empty(): ", tree)
    #
    # print("\nPDF - method make_empty() example 2")
    # print("---------------------------------")
    # tree = AVL()
    # print("Tree before make_empty():", tree)
    # tree.make_empty()
    # print("Tree after make_empty(): ", tree)
