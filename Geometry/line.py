'''a pythonic Line

It's awesome.
'''

from .point import Point
from .exceptions import *

class Line(object):
    vertexNames = 'AB'
    vertexNameA = vertexNames[0]
    vertexNameB = vertexNames[1]
    
    '''
    A line with infinite length defined by two points; A and B.

    Usage:
    >>> a = Line() 
    ...
    >>> b = Line((0,0),(1,1))
    >>> c = Line(Point(),{'y':1,'x':1])
    >>> b == c
    True
    >>> 
    '''
    
    @classmethod
    def fromSegment(cls,segment):
        '''
        :param: segment - Segment subclass
        :return: Line

        Returns a coincident Line object.
        '''
        return cls(segment.A,segment.B)

    @classmethod
    def fromRay(cls,ray):
        '''
        :param: ray - Ray subclass
        :return: Line

        Returns a coincident Line object.
        '''
        return cls(ray.A,ray.B)


    def __init__(self,A=None,B=None):
        '''
        '''
        self.A = A

        if B is None:
            B = [1,1]
        self.B = B

    @property
    def A(self):
        '''
        A point on the line, Point subclass.
        '''
        try:
            return self._A
        except AttributeError:
            pass
        self._A = Point()
        return self._A
    
    @A.setter
    def A(self,newA):
        self.A.xyz = newA

    @property
    def B(self):
        '''
        A point on the line, Point subclass.
        '''
        try:
            return self._B
        except AttributeError:
            pass
        self._B = Point()
        return self._B
    
    @B.setter
    def B(self,newB):
        self.B.xyz = newB

    @property
    def AB(self):
        '''
        '''
        return [self.A,self.B]
    
    @AB.setter
    def AB(self,iterable):
        try:
            self.A,self.B = iterable
        except ValueError:
            self.A, = iterable
    
    @property
    def m(self):
        '''
        Slope parameter, Point(B - A).
        '''
        return self.B - self.A

    @property
    def mapping(self):
        return {self.vertexNameA:self.A.__class__(self.A),
                self.vertexNameB:self.B.__class__(self.B)}
    
    def pointAt(self,t):
        '''
        :param: t - float
        :return: Point subclass

        Varying 't' will produce a new point along this line.

        t = 0 -> point A
        t = 1 -> point B
        '''
        # <xyz> = <x0y0z0> + t<mxmymz>
        return self.A + (t * self.m)

    def __str__(self):
        return 'A=({A}), B=({B})'.format(**self.mapping)

    def __repr__(self):
        '''
        Returns a representation string of this instance.
        '''

        return '{klass}({args})'.format(klass=self.__class__.__name__,
                                        args=str(self))
    
    def __len__(self):
        '''
        Treat a line as a two item container with length '2'.
        '''
        return 2

    def __getitem__(self,key):
        '''
        line[0] retrieves A
        line[1] retrieves B
        '''
        key = int(key)
        if key == 0:
            return self.A
        if key == 1:
            return self.B
        raise IndexError('index %d out of range %s only have two items' %(key))

    def __setitem__(self,key,value):
        '''
        line[0] == line.A
        line[1] == line.B

        '''
        key = int(key)
        if key == 0:
            self.A = value
        if key == 1:
            self.B = value
        raise IndexError('index %d out of range %s only have two items' %(key))

    def __contains__(self,point):
        '''
        p in l

        Returns True iff p is collinear with l.A and l.B.

        '''
        return self.A.isCollinear(point,self.B)

    @property
    def length(self):
        '''
        Raises InfiniteLength exception.
        '''
        raise InfiniteLength()

    def flip(self):
        '''
        :returns: None

        Swaps the positions of A and B.
        '''
        tmp = self.A.xyz
        self.A = self.B
        self.B = tmp

    def doesIntersect(self,other):
        '''
        :param: other - Line subclass
        :return: boolean

        Returns True iff:
           ccw(self.A,self.B,other.A) * ccw(self.A,self.B,other.B) <= 0
           and
           ccw(other.A,other.B,self.A) * ccw(other.A,other.B,self.B) <= 0

        '''
        if self.A.ccw(self.B,other.A) * self.A.ccw(self.B,other.B) > 0:
            return False

        if other.A.ccw(other.B,self.A) * other.A.ccw(other.B,self.B) > 0:
            return False

        return True

    def intersection(self,other):
        '''
        :param: other - Line subclass
        :return: Point subclass

        Returns a Point object with the coordinates of the intersection
        between the current line and the other line. 

        Will raise Parallel() if the two lines are parallel or coincident.
        '''

        if self == other:
            return False

        d0 = self.a - self.b
        d1 = other.a - other.b
        
        denominator = (d0.x * d1.y) - (d0.y * d1.x)
        
        if denominator == 0:
            msg = '%s and %s are parallel or coincident'
            raise Parallel(msg % (self,other))

        cp0 = self.a.cross(self.b)
        cp1 = other.a.cross(other.b)
        
        x_num = (cp0 * d1.x) - (d0.x * cp1)
        y_num = (cp0 * d1.y) - (d0.y * cp1)

        p = Point( x_num / denominator, y_num / denominator)

        if p in self and p in other:
            return p
        
        raise Parallel("Didn't I already check this?") # XXX bug?
    
    def distanceFromPoint(self,point):
        '''
        :param: point - Point subclass
        :return: float

        Distance from the line to the given point.
        '''
        d = self.B - self.A
        n = (d.y*point.x) - (d.x*point.y) + self.A.cross(self.B)
        return n / self.length

    @property
    def normal(self):
        '''
        :return: Line
    
        Returns a line normal (perpendicular) to this line.
        '''
        
        d = self.B - self.A

        return Line([-d.y,d.x],[d.y,-d.x])

    def isNormal(self,other):
        '''
        :param: other - Line subclass
        :return: boolean

        Returns True if this line is perpendicular to the other line.
        '''
        raise NotImplemented('isNormal')
    
    
class Segment(Line):
    '''
    A Line subclass with finite length.
    '''

    @classmethod
    def fromLine(cls,line):
        '''
        :param: line - Line subclass
        :return: Segment

        Returns a coincident Segment object.
        '''
        return cls(line.A,line.B)

    @classmethod
    def fromRay(cls,ray):
        '''
        :param: ray - Ray subclass
        :return: Segment

        Returns a coincident Segment object.
        '''
        return cls(ray.A,ray.B)

    @property
    def length(self):
        '''
        The scalar distance between A and B, float.
        '''
        return self.A.distance(self.B)

    @property
    def midpoint(self):
        '''
        The point between A and B, Point subclass.
        '''
        return self.A.midpoint(self.B)

    def __eq__(self,other):
        '''
        x == y iff:
         ((x.A == y.A) and (x.B == y.B)) 
           or 
         ((x.A == y.B) and (x.B == y.A))
        '''
        if (self.A == other.A) and (self.B == other.B):
            return True
        return (self.A == other.B) and (self.B == other.A)
        
    def __contains__(self,point):
        '''
        p in s
        Returns True iff:
               A,point,B are collinear and A.xyz <= point.xyz <= B.xyz
        '''
        if not super(self.__class__,self).__contains__(point):
            return False
        return point.isBetween(self.A,self.B)

    @property
    def normal(self):
        '''
        :return: Segment
    
        Returns a segment normal (perpendicular) to this segment.
        '''
        return Segment.fromLine(super(Segment,self).normal)
    
    
class Ray(Line):
    '''
    Rays have head and tail vertices with an infinite length in the
    direction of the head vertex.
    '''

    @classmethod
    def fromLine(cls,line):
        '''
        :param: line - Line subclass
        :return: Ray

        Returns a coincident Ray object.
        '''
        return cls(line.A,line.B)

    @classmethod
    def fromSegment(cls,segment):
        '''
        :param: segment - Segment subclass
        :return: Ray

        Returns a coincident Ray object.
        '''        
        return cls(segment.A,segment.B)
    
    @property
    def tail(self):
        '''
        The start of the ray, Point subclass.
        '''
        return self.A

    @tail.setter
    def tail(self,newValue):
        self.A = newValue

    @property
    def head(self):
        '''
        A in the infinite direction of the ray, Point subclass.
        '''
        return self.B

    @head.setter
    def head(self,newValue):
        self.B = newValue


    def __contains__(self,point):
        '''
        point in Ray
        '''
        raise NotImplemented('__contains__')

        # probably ccw magic that will tell us the answer
        
    @property
    def alpha(self):
        '''
        Angle in radians relative to the X axis.
        '''
        raise NotImplemented('alpha')


    @property
    def beta(self):
        '''
        Angle in radians relative to the Y axis.
        '''
        raise NotImplemented('beta')

    @property
    def gamma(self):
        '''
        Angle in radians relative to the Z axis.
        '''
        raise NotImplemented('gamma')

    @property
    def normal(self):
        '''
        :return: Ray
    
        Returns a ray normal (perpendicular) to this segment.
        '''
        return Ray.fromLine(super(Ray,self).normal)

    # rays can be treated much like vectors so many of the point operations
    # can be reused here

    
