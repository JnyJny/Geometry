'''
'''

from .Exceptions import *
from .Point import Point

class Line(object):
    
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
    
    '''
    A Line defined by two Points; A and B.
    '''
    def __init__(self,A,B):
        '''
        :param: A - Point subclass or Point initializer
        :param: B - Point subclass or Point initializer
        '''
        self.A = A
        self.B = B

    @property
    def A(self):
        '''
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
    
    def point(self,t):
        '''
        :param: t - float
        :return: Point along the line at parameter 't'

        Varying t will produce a new point along the line.

        t = 0 -> point A
        t = 1 -> point B
        '''
        # <xyz> = <x0y0z0> + t<mxmymz>
        return self.A + (t * self.m)

    def __repr__(self):
        '''
        Returns a representation string of this instance.
        '''
        fmt = '%s(A=%s,B=%s)'
        return fmt % (self.__class__.__name__,self.A,self.B)
    
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
        tmp = Point(self.A)
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

        Can raise the Parallel() if the two lines are parallel.

        XXX Can also raise NoIntersection() 
            but honestly I think it might be a bug.
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
        
        raise NoIntersection('%s and %s do not intesect' %(self,other))
    
    def distanceFromPoint(self,point):
        '''
        :param: point - Point subclass
        :return: float

        '''
        d = self.B - self.A

        n = (d.y*point.x) - (d.x*point.y) + self.A.cross(self.B)
        return n / self.length

    def normal(self):
        '''
        :return: Line
    
        Returns a line normal to this line.
        '''
        
        d = self.B - self.A

        return Line([-d.y,d.x],[d.y,-d.x])

    def isNormal(self,other):
        '''
        :param: other - Line subclass
        :return: boolean

        Returns True if this line is normal to the other line.
        '''
        raise NotImplemented('isNormal')
    
    
class Segment(Line):
    '''
    A Line subclass with a finite length.
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
        
    def normal(self):
        '''
        :return: Segment
    
        Returns a segment normal to this segment.
        '''
        return Segment.fromLine(super(Segment,self).normal())

    
    
class Ray(Line):
    '''
    Rays have an origin vertex and an infinite length in the direction of
    the second vertex 'B'.
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
    def origin(self):
        '''
        The start of the ray, Point subclass.
        '''
        return self.A

    @origin.setter
    def origin(self,newValue):
        self.A = newValue

    @property
    def O(self):
        '''
        Shorthand notation for origin, Point subclass.
        '''
        return self.A

    @O.setter
    def O(self,newValue):
        self.A = newValue

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

    def normal(self):
        '''
        :return: Ray
    
        Returns a ray normal to this segment.
        '''
        return Ray.fromLine(super(Segment,self).normal())

    # rays can be treated much like vectors so many of the point operations
    # can be reused here
