""" Stack Implementation
Using lists in python to implement stack data structure
Main functions : LIFO (Last In First Out) | like a stack of plates
- pop, empty, peek, push, size
"""

new_stack = [1, 2, 3, 4, 5]

# Popping the last element
new_stack.pop()

# Checking if a stack is empty
print(not new_stack)

# Peeking the last element
new_stack[-1]

# Pushing an element on top
new_stack.append(6)

# Getting the size of the stack
len(new_stack)


print(new_stack)

"""
Implementation of stack using a linked list
"""
class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class Stack:
    def __init__(self):
        self.head = None   # head is the top
        self._size = 0

    def push(self, val):
        self.head = Node(val, self.head)
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        val = self.head.val
        self.head = self.head.next
        self._size -= 1
        return val

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.head.val

    def is_empty(self):
        return self.head is None

    def __len__(self):
        return self._size