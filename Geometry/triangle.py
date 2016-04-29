''' a pythonic Triangle
'''

import math
from . import Point
from . import Segment
from .exceptions import *


class Triangle(object):
    '''a pythonic Triangle

    Implements a Triangle object in the XY plane having three
    non-coincident vertices and three intersecting edges.

    Vertices are labeled 'A', 'B' and 'C'.
    Edges are labeled 'AB', 'BC' and 'AC'.

    The length of each edge is labeled 'ab', 'bc' and 'ac'.

    Angles in radians are labeled:
      'alpha' for CAB
      'beta'  for ABC
      'gamma' for BCA

    Usage:

    >>> a = Triangle()
    >>> b = Triangle(A,B,C)
    >>> c = Triangle([p,q,r])
    >>> d = Triangle([x,y,z],[x,y,z],[x,y,z])
    >>> e = Triangle(A=p0,B=p1,C=p2)
    '''

    vertexNames = 'ABC'
    vertexNameA = vertexNames[0]
    vertexNameB = vertexNames[1]
    vertexNameC = vertexNames[2]
    edgeNames = [vertexNameA + vertexNameB,
                 vertexNameB + vertexNameC,
                 vertexNameA + vertexNameC]
    edgeNameAB = edgeNames[0]
    edgeNameBC = edgeNames[1]
    edgeNameAC = edgeNames[2]

    @classmethod
    def randomXY(cls, origin=None, radius=1):
        '''
        :param: radius - float
        :param: origin - optional Point subclass
        :return: Triangle

        Creates a triangle with random coordinates in the circle
        described by (origin,radius).  If origin is unspecified, (0,0)
        is assumed.
        '''

        pts = set()
        while len(pts) < 3:
            p = Point.randomXY(origin, radius)
            pts.add(p)

        return cls(pts)

    @classmethod
    def unit(cls):
        '''
        XXX missing doc string
        '''
        return cls(Point.units())

    def __init__(self, *args, **kwds):

        self(*args, **kwds)

    def __call__(self, *args, **kwds):

        if len(args) == 0 and len(kwds) == 0:
            return

        if len(args) == 1:
            self.ABC = args[0]
        else:
            self.ABC = args

        for name in self.vertexNames:
            try:
                setattr(self, name, kwds[name])
            except:
                pass

    @property
    def A(self):
        '''
        Vertex of triangle, Point subclass.
        '''
        try:
            return self._A
        except AttributeError:
            pass
        self._A = Point()
        return self._A

    @A.setter
    def A(self, newValue):
        self.A.xyz = newValue

    @property
    def B(self):
        '''
        Vertex of triangle, Point subclass.
        '''
        try:
            return self._B
        except AttributeError:
            pass
        self._B = Point(1, 0)
        return self._B

    @B.setter
    def B(self, newValue):
        self.B.xyz = newValue

    @property
    def C(self):
        '''
        Vertex of triangle, Point subclass.
        '''
        try:
            return self._C
        except AttributeError:
            pass
        self._C = Point(0, 1)
        return self._C

    @C.setter
    def C(self, newValue):
        self.C.xyz = newValue

    @property
    def ABC(self):
        '''
        A list of the triangle's vertices, list.
        '''
        try:
            return self._ABC
        except AttributeError:
            pass
        self._ABC = [self.A, self.B, self.C]
        return self._ABC

    @ABC.setter
    def ABC(self, iterable):
        self.A, self.B, self.C = iterable

    @property
    def AB(self):
        '''
        List of vertices A and B, list.
        '''
        try:
            return self._AB
        except AttributeError:
            pass
        self._AB = [self.A, self.B]
        return self._AB

    @AB.setter
    def AB(self, iterable):
        self.A, self.B = iterable

    @property
    def AC(self):
        '''
        List of verticies A and C, list.
        '''
        try:
            return self._AC
        except AttributeError:
            pass
        self._AC = [self.A, self.C]
        return self._AC

    @AC.setter
    def AC(self, iterable):
        self.A, self.C = iterable

    @property
    def BC(self):
        '''
        Line segment with endpoints B and C, Segment subclass.
        '''
        try:
            return self._BC
        except AttributeError:
            pass
        self._BC = [self.B, self.C]
        return self._BC

    @BC.setter
    def BC(self, iterable):
        self.B, self.C = iterable

    @property
    def vertices(self):
        '''
        Alias for property "ABC", list.
        '''
        return self.ABC

    @property
    def sides(self):
        '''
        Dictionary of line segments, dict.

        '''
        try:
            return self._sides
        except AttributeError:
            pass

        self._sides = {'AB': self.AB, 'BC': self.BC, 'AC': self.AC}

        return self._sides

    @property
    def hypotenuse(self):
        '''
        The longest side of the triangle.

        '''
        return max(self.ab, self.bc, self.ac)

    @property
    def alpha(self):
        '''
        The angle described by CAB in radians, float.

        '''
        return Segment(self.C, self.A).radiansBetween(Segment(self.A, self.B))

    @property
    def beta(self):
        '''
        The angle described by ABC in radians, float.

        '''
        return Segment(self.A, self.B).radiansBetween(Segment(self.B, self.C))

    @property
    def gamma(self):
        '''
        The angle described by BCA in radians, float.

        '''

        return Segment(self.B, self.C).radiansBetween(Segment(self.C, self.A))

    @property
    def angles(self):
        '''
        '''
        return [self.alpha, self.beta, self.gamma]

    @property
    def ab(self):
        '''
        The length of line segment AB, float.

        '''
        return self.A.distance(self.B)

    @property
    def bc(self):
        '''
        The length of line segment BC, float.

        '''
        return self.B.distance(self.C)

    @property
    def ac(self):
        '''
        The length of line segment AC, float.

        '''
        return self.A.distance(self.C)

    @property
    def isCCW(self):
        '''
        Returns True if ABC has a counter-clockwise rotation, boolean.

        '''
        return self.A.isCCW(self.B, self.C)

    @property
    def ccw(self):
        '''
        Result of ccw(A,B,C), float.

        '''
        return self.A.ccw(self.B, self.C)

    @property
    def area(self):
        '''
        Area of the triangle, float.

        '''
        return abs(self.ccw) / 2

    @property
    def semiperimeter(self):
        '''
        semiperimeter = (|AB|+|BC|+|AC|) / 2

        '''
        return sum([self.ab, self.bc, self.ac]) / 2

    @property
    def isEquilateral(self):
        '''
        Returns true if all sides are the same length.
        '''

        ab, bc, ac = self.ab, self.bc, self.ac

        return (ab == bc) and (bc == ac)

    @property
    def isIsosceles(self):
        '''
        Returns true if two sides are the same length.
        '''
        ab, bc, ac = self.ab, self.bc, self.ac

        if ab == bc:
            return True

        if ab == ac:
            return True

        return bc == ac

    @property
    def isScalene(self):
        '''
        Returns true if all sides are unequal in length.
        '''

        ab, bc, ac = self.ab, self.bc, self.ac

        return (ab != bc) and (ab != ac) and (bc != ac)

    @property
    def isRight(self):
        '''
        Returns true if one angle in the triangle is a 90 degree (Pi/2
        rad) angle.
        '''
        half_pi = math.pi / 2
        for a in self.angles:
            if a == half_pi:    # epsilon check?
                return True
        return False

    @property
    def isObtuse(self):
        '''
        Returns true if one angle in the triangle is greater than 90
        degrees (Pi/2 radians).

        '''
        half_pi = math.pi / 2

        for a in self.angles:
            if a > half_pi:    # epsilon check?
                return True
        return False

    @property
    def isAcute(self):
        '''
        Returns true if all angles are less than 90 degrees ( Pi/2 radians).
        '''

        half_pi = math.pi / 2
        for a in self.angles:
            if a >= half_pi:    # epsilon check?
                return False
        return True

    def __str__(self):
        return 'A=({t.A!s}), B=({t.B!s}), C=({t.C!s})'.format(t=self)

    def __repr__(self):
        return '{o.__class__.__name__}({o!s})'.format(o=self)

    def __eq__(self, other):
        '''
        x == y

        Iff len(set(x.vertices).difference(set(y.vertices))) == 0

        '''
        a = set(self.vertices)
        b = set(other.vertices)
        return len(a.difference(b)) == 0

    def __contains__(self, point):
        '''
        :param: point - Point subclass
        :return: boolean

        Returns True if point is inside the triangle or
        lies on any of it's sides.
        '''
        try:
            r = [self.A.ccw(self.B, point),
                 self.B.ccw(self.C, point),
                 self.C.ccw(self.A, point)]
        except CollinearPoints:
            # point is on the lines AB, BC, or CA and that counts.
            return True

        return not (any([x > 0 for x in r]) and any([x < 0 for x in r]))

    def altitude(self, side='AB'):
        '''
        :side: optional string
        :return: float

        The shortest distance from the specified side to the opposite point.

        '''
        s = self.semiperimeter

        num = 2 * math.sqrt(s * (s - self.ab) * (s - self.bc) * (s - self.ac))

        try:
            div = {'AB': self.ab, 'AC': self.ac, 'BC': self.bc}[side]
            return num / div
        except IndexError:
            pass

        msg = "expecting 'AB', 'BC' or 'AC', got '{side}'"

        raise ValueError(msg.format(side=side))

    def flip(self, side='AB'):
        '''
        :param: side - optional string
        :return: self

        The optional side paramater should have one of three values:
        AB, BC, or AC.

        Changes the order of the triangle's points, swapping the
        specified points. Doing so will change the results of isCCW
        and ccw.

        '''

        if side == 'AB':
            tmp = Point(self.A)
            self.A = self.B
            self.B = tmp
            return self

        if side == 'BC':
            tmp = Point(self.B)
            self.B = self.C
            self.C = tmp
            return self

        if side == 'AC':
            tmp = Point(self.A)
            self.A = self.C
            self.C = tmp
            return self

        msg = "expecting 'AB', 'BC' or 'AC', got '{side}'"

        raise ValueError(msg.format(side=side))

    def doesIntersect(self, other):
        '''
        :param: other - Triangle subclass
        :return: boolean

        Returns True iff:
           Any side in self intersects any side in other.

        '''

        otherType = type(other)
        if issubclass(otherType, Triangle):
            for s in self.sides.values():
                for q in other.sides.values():
                    if s.doesIntersect(q):
                        return True
            return False

        if issubclass(otherType, Line):
            for s in self.sides.values():
                if s.doesIntersect(other):
                    return True
            return False

        msg = "expecting Line or Triangle subclasses, got '{type}'"

        raise TypeError(msg.format(type=otherType))
