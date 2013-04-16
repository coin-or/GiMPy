'''
disjoint_set.py
Module that has DisjointSet class, which is built on top of Graph class.
'''

class DisjointSet(Graph):
    def __init__(self, optimize = True, **attrs):
        attrs['type'] = DIRECTED_GRAPH
        Graph.__init__(self, **attrs)
        self.sizes = {}
        self.optimize = optimize

    def add(self, aList):
        self.add_node(aList[0])
        for i in range(1, len(aList)):
            self.add_edge(aList[i], aList[0])
        self.sizes[aList[0]] = len(aList)

    def union(self, i, j):
        roots = (self.find(i), self.find(j))
        if roots[0] == roots[1]:
            return False
        if self.sizes[roots[0]] <= self.sizes[roots[1]] or not self.optimize:
            self.add_edge(roots[0], roots[1])
            self.sizes[roots[1]] += self.sizes[roots[0]]
            return True
        else:
            self.add_edge(roots[1], roots[0])
            self.sizes[roots[0]] += self.sizes[roots[1]]
            return True

    def find(self, i):
        current = i
        edge_list = []
        while len(self.get_neighbors(current)) != 0:
            successor = self.get_neighbors(current)[0]
            edge_list.append((current, successor))
            current = successor
        if self.optimize:
            for e in edge_list:
                if e[1] != current:
                    self.del_edge((e[0], e[1]))
                    self.add_edge(e[0], current)
        return current

if __name__ == '__main__':
   pass
