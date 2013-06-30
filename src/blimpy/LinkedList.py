'''
Lists Module
A basic linked list implementation conforming to the Python list API.
It can be used as a drop-in replacement for the built-in list class.
Created on Jan 29, 2012
'''

__version__    = '1.0.0'
__author__     = 'Ted Ralphs, Aykut Bulut (ted@lehigh.edu, ayb211@lehigh.edu)'
__license__    = 'BSD'
__maintainer__ = 'Aykut Bulut'
__email__      = 'ayb211@lehigh.edu'
__url__        = None
__title__      = 'Linked list data structure'

from copy import deepcopy

class Node(object):
    ''' Basic data type that LinkedList will contain
    pre: data that node will contain
    post: Node type object
    '''
    def __init__(self, initdata, nextNode = None):
        '''constructor of Node class
        pre: Node class object (self), initial data (initdata)'''
        self.data = initdata
        self.nextNode = nextNode

    def getData(self):
        ''' class method that returns to data
        pre: self
        post: data of the Node'''
        return self.data

    def getNext(self):
        return self.nextNode

    def setData(self, newdata):
        ''' class method that sets data
        pre: self, new data'''
        self.data = newdata

    def setNext(self, newnext):
        ''' class method that changes the next Node
        pre: self, new next'''
        self.nextNode = newnext

    def __repr__(self):
        return 'Node instance, data:%s, nextNode:%s' %(self.getData(), self.getNext())

    def __str__(self):
        return str(self.data)


class LinkedList(object):
    '''implementation of link list data structure.
    The behavior is designed to be the same as a Python list.
    For efficiency when using the list as a stack, the list is stored
    such that the last item in the list is the head node. Thus, the
    append, push, pop, and most other methods are efficient, but
    forward iteration is not. Reverse iteration is efficient, however,
    pre:  Node is the head node of a linked list and length is the length of
          that list
    post: creates a LinkedList type object
    '''

    def __init__(self, Node=None, length = 0):
        ''' constructor method of the class
        pre: self'''
        self.head = Node
        self.length = length

    def __contains__(self, item):
        ''' sequential search method
        pre: self, item to be searched
        post: True if list contains the item, False otherwise'''
        current = self.head
        while current != None:
            if current.getData() == item:
                return True
            else:
                current = current.getNext()
        return False

    def remove(self, item):
        ''' class method that removes the first occurrence of the given item
        if there is one
        pre: self, item '''
        current = self.head
        previous = None
        found = False
        while not found and current != None:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()

        if not found:
            return False
        elif previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())
        self.length -= 1
        return True

    def __delitem__(self, item):
        if not self.remove(item):
            raise KeyError, "Key not found in list"

    def insert(self, position, item):
        ''' class method that inserts item to the given position
        pre: self, position, item
        position should not be greater than length of the list'''
        previous = None
        current = self.head
        for i in range(self.length - position):
            previous = current
            current = current.getNext()
        tmp = Node(item, current)
        if previous == None:
            self.head = tmp
        else:
            previous.setNext(tmp)
        self.length += 1

    def peek(self, index = None):
        ''' class method that retrieves, but does not remove,
        the head (first element) of this list
        pre: self
        post: the data of the head of the list or None if the list is empty'''
        if self.head == None:
            return None
        elif index == None:
            return self.head.getData()
        else:
            return self[index]

    def pop(self, index = None):
        ''' class method that removes the item at the given position
        in the list, and returns it. If no index is specified
        removes and returns the last item in the list
        pre: self, position (optional), position should be less than length
        of the list, list should not be empty
        post: return the item at given index or last item if not specified'''
        previous = None
        current = self.head
        if index == None:
            current = self.head
            self.head = self.head.getNext()
        else:
            for i in range(self.length - index - 1):
                previous = current
                current = current.getNext()
            if previous == None:
                self.head = current.getNext()
            else:
                previous.setNext(current.getNext())
        self.length -= 1
        return current.data

    def __len__(self):
        ''' class method that returns the number of items in the list
        pre: self
        post: returns number of items in the list'''
        return self.length

    def append(self, item):
        ''' class method that appends the given item at the end of the list
        pre: self, item'''
        current = self.head
        self.head = Node(item)
        self.head.nextNode = current
        self.length += 1

    def extend(self, otherLinkedList):
        ''' class method that extends the list by adding otherLinkedList at the
         end of the self
         pre: self, otherLinkedList'''
        #if self.head==None:
        #    self.head = otherLinkedList.head
        #    return
        #if otherLinkedList.head==None:
        #    return
        for item in otherLinkedList:
            self.append(item)

    def index(self, item):
        ''' class method that returns the index of the first occurance of
        item, returns None if there is no any item.
        pre: self, item
        post: item index or None'''
        current = self.head
        for index in range(self.length, 0 , -1):
            if current == None:
                break
            if current.getData() == item:
                return index
            current = current.getNext()
        return None

    def count(self, item):
        ''' class method that counts the number of occurances of item
         in the list
        pre: self, item
        post: number of occurances of item in the list'''
        count = 0
        current = self.head
        while current != None:
            if current.getData() == item:
                count += 1
        return count

    def __getitem__ (self, index):
        ''' replace built-in class method that returns the item for the given
         index
        pre: self, index, index should be less than length of list, list
        should not be empty
        post: return item for the given index'''
        if isinstance(index, slice):
            if index.start == None or index.start < 0:
                start = 0
            else:
                start = index.start
            if index.stop == None or index.stop > self.length:
                stop = self.length
            else:
                stop = index.stop
            current = self.head
            for i in range(self.length - stop):
                current = current.getNext()
            newHead = Node(deepcopy(current.data))
            previous = newHead
            for i in range(stop - start -1):
                if current.getNext() == None:
                    break
                current = current.getNext()
                previous.setNext(Node(deepcopy(current.data)))
                previous = previous.getNext()
            return LinkedList(newHead, stop - start)
        else:
            current = self.head
            if index < 0:
                if -index > self.length:
                    raise IndexError
                return self[self.length+index]
            else:
                i = self.length - 1
                while True:
                    if current == None:
                        raise IndexError
                    if i <= index:
                        break
                    current = current.getNext()
                    i -= 1
                return current.getData()

    def __iter__(self):
        ''' built-in class method, makes LinkedList objects iterable
        pre: self
        post: self.head, first Node on the list'''
        return self.forward()

    def __reversed__(self):
        ''' built-in class method, makes LinkedList objects reverse iterable
        pre: self
        post: self.head, first Node on the list'''
        return self.backward()

    def __repr__(self):
        s = ']'
        current = self.head
        while current != None:
            if current.getNext() == None:
                s = s+str(current.getData())+'['
                return s[::-1]
            s += str(current.getData())+' ,'
            current = current.getNext()
        return '[]'

    def forward(self):
        for i in range(self.length):
            yield self[i]

    def backward(self):
        current = self.head
        while current != None:
            yield current.getData()
            current = current.getNext()

    def __add__(self, otherLinkedList):
        new_list = self.__class__()
        new_list.extend(self)
        new_list.extend(otherLinkedList)
        return new_list


if __name__ == '__main__':
    o = LinkedList()
    for i in range(100):
        o.append(i)

    for i in reversed(o):
        print i
    print 100000 in o

    print o.pop()
    print o.pop(0)
    o.insert(0, 'a')
    print o.pop(0)

    a = o[:50]
    for i in a:
        print i
    a = o[50:]
    for i in a:
        print i
