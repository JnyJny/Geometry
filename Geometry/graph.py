'''a broken pythonic Graph

Nodes and edges, not pretty colors and pitchers.
'''

import math

from .point import Point
from .line import Segment
from .exceptions import *

class Edge(Segment):
    pass

class Node(Point):
    
    @property
    def neighbors(self):
        try:
            return self._neighbors
        except AttributeError:
            self._neighbors = []
        return self._neighbors

    @property
    def edges(self):
        e = []
        for neighbor in self.neighbors:
            e.append((self,neighbor))
        return e

    def addNeighbor(self,target):
        if target is self:
            return
        if target in self.neighbors:
            return
        self.neighbors.append(target)

    def addNeighbors(self,targets):
        for target in targets:
            self.addNeighbor(target)

    def disconnect(self,target=None):
        if target:
            self.neighbors.remove(target)
            return
        self.neighbors.clear()
        

    def weighted_edges(self,weightFunc=None):
        if not weightFunc:
            weightFunc = lambda a,b: a.distance(b)
        return dict([weightFunc(a,b) for a,b in self.edges])

    def connected(self,target,visited=None):
        if visited is None:
            visited = []
        else:
            if self in visited:
                raise GraphCycleDetected(self,target,visited)

        visited.append(self)
            
        if target in self.neighbors:
            return True

        for neighbor in self.neighbors:
            if self.neighbor.connected(target,visited):
                return True
        return False


class Graph(object):
    
    @classmethod
    def randomGraph(cls,radius,nodes,origin=None):

        if origin is None:
            origin = Point()

        graph = cls()

        while len(graph) < nodes:
            try:
                graph.addNode(Node.randomLocation(radius,origin))
            except ValueError:
                pass

        return graph
    
    def __init__(self,points=None):
        self.nodes = []
        try:
            for point in points:
                self.addNode(point,skipSort=True)
        except TypeError:
            pass
        self.edges = []

    def __len__(self):
        return len(self.nodes)

    def __str__(self):
        s = []
        s.append(repr(self))
        s.extend(['\t'+repr(n) for n in self.nodes])
        s.extend(['\t'+repr(e) for e in self.edges])
        return '\n'.join(s)

    def __repr__(self):
        fmt = '<%s(nodes=[%d nodes],edges=[%d edges])>'
        return fmt % ( self.__class__.__name__,len(self.nodes),len(self.edges))

    @property
    def sorted(self):
        try:
            return self._sorted
        except AttributeError:
            pass
        self._sorted = False
        return self._sorted

    @sorted.setter
    def sorted(self,newValue):
        self._sorted = newValue

    def sortNodes(self,func=None):
        if func is None:
            func = lambda x:x.distanceSquared(self.cg)
        self.nodes.sort(key=func)
        self.sorted = True

    def addNode(self,node,skipSorting=False):
        '''
        '''
        if isinstance(node,Point):
            node = Node(node)
        # assert type(node) == type(Node)
        if node in self.nodes:
            raise ValueError('duplicate node %s' % (node))
        
        self.nodes.append(node)
        self.sorted = False
        
    @property
    def cg(self):
        '''
        Center of gravity, Node.
        '''
        return Node(sum(self.nodes) // len(self.nodes))

    def __eq__(self,other):
        '''
        x == y iff:
          len(x) == len(y) 
          all nodes of x are in y
        '''

        if len(self) != len(other):
            return False
        
        return self in other

    def __contains__(self,other):
        otherType = type(other)
        
        if issubtype(otherType,Node):
            for node in self.nodes:
                if node == other:
                    return True
            return False

        if issubtype(otherType,Graph):
            # graphs need to match nodes AND edges

            if len(self.edges) != len(other.edges):
                return False

            for node in self.nodes:
                if node in other:
                    pass
                
        return True
    
    def disconnect(self):
        '''
        '''
        self.edges.clear()
        
    def connect(self,doDisconnect=True):
        '''
        '''
        if doDisconnect:
            self.disconnect()
        
        self.sortNodes()
        
        for A in self.nodes:
            for B in self.nodes:
                if A is B:
                    continue
                self.edges.append(Edge(A,B))

    def drawNodes(self,surface,color):
        for node in self.nodes:
            node.draw(surface,color)

    def drawEdges(self,surface,color):
        for edge in self.edges:
            edge.draw(surface,color)

    def draw(self,surface,nodeColor=(0,255,0),edgeColor=(0,0,255),cg=True):

        self.drawEdges(surface,edgeColor)
        self.drawNodes(surface,nodeColor)

        if cg:
            self.cg.draw(surface,(255,0,0))
