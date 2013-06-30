'''
This module implements a Queue class, a simple list-based queue data structure
and a PriorityQueue class, which is a heap-based priority queue data structure.
'''

__version__    = '1.0.0'
__author__     = 'Aykut Bulut, Ted Ralphs (ayb211@lehigh.edu,ted@lehigh.edu)'
__license__    = 'BSD'
__maintainer__ = 'Aykut Bulut'
__email__      = 'ayb211@lehigh.edu'
__url__        = None
__title__      = 'Queue data structure'

from LinkedList import LinkedList

class Queue(object):
    '''
    A queue data structure built on top of a linked list
    attributes:
        items:    A list that holds objects in the queue
                  type: LinkedList
    methods:
        __init__(self):        constructor of the class
        isEmpty(self):         returns True if the queue instance is empty
        push(self,item):       inserts item to the queue
        pop(self,item):        removes first item in the queue if no item is
                               specified removes the given item if item is
                               specified
        size(self):            returns the size of the queue
    '''
    def __init__(self):
        self.items = LinkedList()

    def isEmpty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.insert(0,item)

    def push(self, item):
        self.enqueue(item)

    def dequeue(self, item = None):
        if item == None:
            return self.items.pop()
        else:
            self.items.remove(item)
            return item

    def remove(self, item = None):
        self.dequeue(item)

    def pop(self, item = None):
        return self.dequeue(item)

    def peek(self, item = None):
        if item == None:
            return self.items[len(self.items)-1]
        else:
            for i in self.items:
                if i == item:
                    return i
        return None

    def size(self):
        return len(self.items)

import itertools, heapq

class PriorityQueue(object):
    '''
    A priority queue based on a heap.
    attributes:
        heap:                  A heap-ordered list that holds objects in the
                               queue
                               type: list
        entry_finder:          A (map) dictionary for finding items in the heap
        counter:               A unique sequence generator
        size:                  Number of items in the queue
    methods:
        __init__(self):        constructor of the class
        isEmpty(self):         returns True if the queue is empty, False
                               otherwise
        push(self,item,priority): inserts item with given priority in to the
                               queue
        pop(self,item):        removes item with highest priority in the queue
                               if no item is specified or removes the given
                               item if item is specified
        size(self):            returns the size of the queue
    '''
    def __init__(self, aList = None):
        if aList == None:
            self.heap = []
        else:
            self.heap = aList
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = itertools.count()     # unique sequence count
        self.size = len(self.heap)

    def isEmpty(self):
        return self.size == 0

    def heapify(self):
        heapq.heapify(self.heap)

    def pop(self, item = None):
        '''
        Remove and return the lowest priority task. Raise KeyError if empty.
        '''
        if item == None:
            while self.size:
                entry = heapq.heappop(self.heap)
                if entry[-1] is not self.REMOVED:
                    del self.entry_finder[entry[-1]]
                    self.size -= 1
                    return entry[-1]
            raise KeyError('pop from an empty priority queue')
        else:
            self.remove(item)

    def peek(self, item = None):
        if item == None:
            while self.size:
                if self.heap[0][-1] is not self.REMOVED:
                    return self.heap[0][-1]
                else:
                    heapq.heappop(self.heap)
            raise KeyError('peek at an empty priority queue')
        try:
            return self.entry_finder[item][-1]
        except KeyError:
            return None

    def get_priority(self, item):
        try:
            return self.entry_finder[item][0]
        except KeyError:
            return None

    def push(self, item, priority = 0):
        '''
        Add to the heap or update the priority of an existing task.
        '''
        if item in self.entry_finder:
            self.remove(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.entry_finder[item] = entry
        self.size += 1
        heapq.heappush(self.heap, entry)

    def remove(self, item):
        '''
        Mark an existing task as REMOVED.  Raise KeyError if not found.
        '''
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED
        self.size -= 1
