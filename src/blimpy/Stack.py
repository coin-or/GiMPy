'''
A basic stack implementation using a linked list.
'''

__version__    = '1.0.0'
__author__     = 'Aykut Bulut, Ted Ralphs (ayb211@lehigh.edu,ted@lehigh.edu)'
__license__    = 'BSD'
__maintainer__ = 'Aykut Bulut'
__email__      = 'ayb211@lehigh.edu'
__url__        = None
__title__      = 'Stack data structure'

from LinkedList import LinkedList

class Stack(object):
    '''
    This stack class is built on top of a linked list data structure.
    '''
    def __init__(self):
        self.items = LinkedList()

    def isEmpty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self, item = None):
        if item == None:
            return self.items.pop()
        else:
            self.items.remove(item)
            return item

    def remove(self, item):
        self.items.remove(item)

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


if __name__ == '__main__':

    s = Stack()

    for i in range(10):
        s.push(i)

    print s.pop()
