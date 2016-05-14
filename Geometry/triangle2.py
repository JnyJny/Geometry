import math
import collections
import itertools
from . import Polygon, Point, Segment, Circle
from .constants import Epsilon, Half_Pi, nearly_eq, Sqrt_3
from .exceptions import *


class Triangle(Polygon):

    @classmethod
    def withAngles(cls, origin=None, base=1, alpha=None,
                   beta=None, gamma=None, inDegrees=False):
        '''
        :origin: optional Point
        :alpha: optional float describing length of the side opposite A
        :beta: optional float describing length of the side opposite B
        :gamma: optional float describing length of the side opposite C
        :return: Triangle initialized with points comprising the triangle
                 with the specified angles.
        '''
        raise NotImplementedError("withAngles")

    @classmethod
    def withSides(cls, origin=None, a=1, b=1, c=1):
        '''
        :origin: optional Point
        :a: optional float describing length of the side opposite A
        :b: optional float describing length of the side opposite B
        :c: optional float describing length of the side opposite C
        :return: Triangle initialized with points comprising the triangle
                 with the specified side lengths.

        If only 'a' is specified, an equilateral triangle is returned.

        '''
        raise NotImplementedError("withSides") 
        

    def __init__(self, A=None, B=None, C=None):
        '''
        :args: iterable of Point or Point equivalents
        :kwds: named Points where recognized names are 'A', 'B' and 'C'.
        '''

        v = []
        if isinstance(A, collections.Iterable) and not issubclass(type(A),Point):
            v.extend(A)
        else:
            if not A:
                v.insert(0,Point())
            
            if not B:
                v.insert(1,Point(1,0))
            
            if not C:
                v.insert(2,Point(0,1))
            
        super().__init__(vertices=v)
            

    @property
    def AB(self):
        return self.pairs('AB')

    @AB.setter
    def AB(self, iterable):
        self.A, self.B = iterable

    @property
    def BA(self):
        return self.pairs('BA')

    @BA.setter
    def BA(self, iterable):
        self.B, self.A = iterable

    @property
    def BC(self):
        return self.pairs('BC')

    @BC.setter
    def BC(self, iterable):
        self.B, self.C = iterable

    @property
    def CB(self):
        return self.pairs('CB')

    @CB.setter
    def CB(self, iterable):
        self.C, self.B = iterable

    @property
    def AC(self):
        return self.pairs('AC')

    @AC.setter
    def AC(self, iterable):
        self.A, self.C = iterable

    @property
    def CA(self):
        return self.pairs('CA')

    @AC.setter
    def CA(self, iterable):
        self.C, self.A = iterable

    @property
    def ABC(self):
        return [self.A, self.B, self.C]

    @ABC.setter
    def ABC(self, iterable):
        self.A, self.B, self.C = iterable

    @property
    def ccw(self):
        '''
        Result of A.ccw(B,C), float.

        See Point.ccw

        '''
        return self.A.ccw(self.B, self.C)

    @property
    def isCCW(self):
        '''
        True if ABC has a counter-clockwise rotation, boolean.

        '''
        return self.A.isCCW(self.B,self.C)

    @property
    def area(self):
        '''
        Area of the triangle, float.

        Performance note: computed via Triangle.ccw (subtractions and
        multiplications and a divison).

        '''
        return abs(self.ccw) / 2

    @property
    def heronsArea(self):
        '''
        Heron's forumla for computing the area of a triangle, float.

        Performance note: contains a square root.

        '''
        s = self.semiperimeter

        return math.sqrt(s * ((s - self.a) * (s - self.b) * (s - self.c)))        

    @property
    def hypotenuse(self):
        '''
        The longest edge of the triangle, Segment.
        '''
        return max(self.edges,key=lambda s:s.length)

    @property
    def alpha(self):
        '''
        The angle described by angle CAB in radians, float.

        '''
        return Segment(self.CA).radiansBetween(Segment(self.BA))

    @property
    def beta(self):
        '''
        The angle described by angle ABC in radians, float.

        '''
        return Segment(self.AB).radiansBetween(Segment(self.CB))

    @property
    def gamma(self):
        '''
        The angle described by angle BCA in radians, float.

        '''
        return Segment(self.BC).radiansBetween(Segment(self.AC))

    @property
    def angles(self):
        '''
        A list of the interior angles of the triangle, list of floats.
        '''
        return [self.alpha, self.beta, self.gamma]

    @property
    def a(self):
        '''
        The length of line segment BC, opposite vertex A, float.

        '''
        return abs(self.B.distance(self.C))

    @property
    def b(self):
        '''
        The length of line segment AC, opposite vertex B, float.

        '''
        return abs(self.A.distance(self.C))

    @property
    def c(self):
        '''
        The length of line segment AB, opposite vertex C, float.

        '''
        return abs(self.A.distance(self.B))

    @property
    def sides(self):
        '''
        A list of edge lengths [a, b, c], list of floats.

        '''
        return [self.a, self.b, self.c]

    @property
    def altitudes(self):
        '''
        A list of the altitudes of each vertex [AltA, AltB, AltC], list of
        floats.

        An altitude is the shortest distance from a vertex to the side
        opposite of it.

        '''
        A = self.area * 2

        return [A / self.a, A / self.b, A / self.c]    

    
    
        
