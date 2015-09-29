'''
'''

from .Exceptions import *
from .Point import Point

class Line(object):
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

    def __str__(self):
        return repr(self)
        
    def __repr__(self):
        fmt = '<%s(A=%s,B=%s)>'
        return fmt % (self.__class__.__name__,self.A,self.B)
    
    def __len__(self):
        return 2

    def __getitem__(self,key):
        key = int(key)
        if key == 0:
            return self.A
        if key == 1:
            return self.B
        raise IndexError('index %d out of range %s only have two items' %(key))

    def __setitem__(self,key,value):
        key = int(key)
        if key == 0:
            self.A = value
        if key == 1:
            self.B = value
        raise IndexError('index %d out of range %s only have two items' %(key))

    def __contains__(self,point):
        '''
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
        '''
        tmp = Point(self.A)
        self.A = self.B
        self.B = tmp
    
class Segment(Line):
    '''
    A Line subclass.
    '''

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
        point in segment
        Returns True iff:
               A,point,B are collinear and A.xyz <= point.xyz <= B.xyz
        '''
        if not super(self.__class__,self).__contains__(point):
            return False
        return point.isBetween(self.A,self.B)

    def doesIntersect(self,other):
        '''
        :param: other - Segment or Line subclass
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
        :param: other - Segment subclass
        :return: Point subclass

        Returns a Point object with the coordinates of the intersection
        between the current segment and the other segment. 

        Can raise the Parallel() if the two segments are parallel.

        Can also raise NoIntersection() but honestly I think it might be a bug.
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

        
    def normalSegment(self):
        '''
        :return: Segment
    
        Returns a line segment normal to this segment.
        '''
        
        d = self.B - self.A

        return Segment([-d.y,d.x],[d.y,-d.x])
