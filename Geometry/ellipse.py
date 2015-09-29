'''a pythonic Ellipse.

Super awesome.
'''

import math
from .point import Point
from .rectangle import Rectangle
from .triangle import Triangle
from .line import Line


class Ellipse(object):
    '''
    XXX Missing doc string
    '''

    def __init__(self,x_radius,y_radius,center=None):
        '''
        :param: x_radius  - float
        :param: y_radius  - float
        :param: center    - optional Point subclass initializer

        Returns an ellipse in the XY plane with the supplied radii.
        The default value for the center is the origin if it is not
        specified by the caller.

        '''
        self.x_radius = x_radius
        self.y_radius = y_radius
        self.center   = center

    @property
    def x_radius(self):
        '''
        The absolute value of the X ordinate of a point on the ellipse
        when y == 0, float.

        '''
        try:
            return self._x_radius
        except AttributeError:
            pass
        self._x_radius = 1
        return self._x_radius

    @x_radius.setter
    def x_radius(self,newValue):
        self._x_radius = float(newValue)

    @property
    def y_radius(self):
        '''
        The absolute value of the Y ordinate of a point on the ellipse
        when y == 0, float.

        '''
        try:
            return self._y_radius
        except AttributeError:
            pass
        self._y_radius = 1
        return self._y_radius

    @y_radius.setter
    def y_radius(self,newValue):
        self._y_radius = float(newValue)

    @property
    def center(self):
        '''
        Center point of the ellipse, equidistance from foci, Point subclass.
        Defaults to the origin.

        '''
        try:
            return self._center
        except AttributeError:
            pass
        self._center = Point()
        return self._center

    @center.setter
    def center(self,newCenter):
        self._center.xyz = newCenter

    @property
    def C(self):
        '''
        Shorthand notation for Center, Point subclass.

        '''
        return self.center

    @C.setter
    def C(self,newCenter):
        self.center.xyz = newCenter

    def __repr__(self):
        return '%s(%s,%s,%s,%s)'% (self.__class__.__name__,
                                   self.x_radius,
                                   self.y_radius,
                                   self.center)
        
    @property
    def majorRadius(self):
        '''
        The longest radius of the ellipse, float.

        '''
        return max(self.x_radius,self.y_radius)


    @property
    def minorRadius(self):
        '''
        The shortest radius of the ellipse, float.

        '''
        return min(self.x_radius,self.y_radius)

    @property
    def xAxisIsMajor(self):
        '''
        Returns True if the major axis is parallel to the X axis, boolean.
        '''
        return self.majorAxis == self.x_radius

    @property
    def xAxisIsMinor(self):
        '''
        Returns True if the minor axis is parallel to the X axis, boolean.
        '''
        return self.minorAxis == self.x_radius

    @property
    def yAxisIsMajor(self):
        '''
        Returns True if the major axis is parallel to the Y axis, boolean.
        '''
        return self.majorAxis == self.y_radius

    @property
    def yAxisIsMinor(self):
        '''
        Returns True if the minor axis is parallel to the Y axis, boolean.
        '''
        return self.minorAxis == self.y_radius

    @property
    def eccentricity(self):
        '''
        The ratio of the distance between the two foci to the length
        of the major axis, float.

        0 <= e <= 1

        An eccentricity of zero indicates the ellipse is a circle.

        As e tends towards 1, the ellipse elongates.  It tends to the
        shape of a line segment if the foci remain a finite distance
        apart and a parabola if one focus is kept fixed as the other
        is allowed to move arbitrarily far away.

        '''
        return math.sqrt(1-((self.minorRadius / self.majorRadius)**2))

    @property
    def e(self):
        '''
        Shorthand notation for eccentricity, float.

        '''
        return self.eccentricity

    @property
    def linearEccentricity(self):
        '''
        Distance between the center of the ellipse and a focus, float.

        '''
        a = (self.majorRadius*2)**2
        b = (self.minorRadius*2)**2
        return math.sqrt(a - b)

    @property
    def f(self):
        '''
        Shorthand notation for linearEccentricity, float.

        '''
        return self.linearEccentricity


    @property
    def a(self):
        '''
        Positive antipodal point on the major axis, Point subclass.

        '''
        a = Point(self.center)
        
        if self.xAxisIsMajor:
            a.x += self.majorRadius
        else:
            a.y += self.majorRadius
        
        return a


    @property
    def a_neg(self):
        '''
        Negative antipodal point on the major axis, Point subclass.
        
        '''
        na = Point(self.center)
        
        if self.xAxisIsMajor:
            na.x -= self.majorRadius
        else:
            na.y -= self.majorRadius
        return na

    @property
    def b(self):
        '''
        Positive antipodal point on the minor axis, Point subclass.

        '''
        b = Point(self.center)

        if self.xAxisIsMinor:
            b.x += self.minorRadius
        else:
            b.y += self.minorRadius
        return b


    @property
    def b_neg(self):
        '''
        Negative antipodal point on the minor axis, Point subclass.
        '''
        nb = Point(self.center)

        if self.xAxisIsMinor:
            b.x -= self.minorRadius
        else:
            b.y -= self.minorRadius

    @property
    def vertices(self):
        '''
        A list of four points where the axes intersect the ellipse, list.
        '''
        return [self.a,self.b,self.a_neg,self.b_neg]

    @property
    def focus0(self):
        '''
        First focus of the ellipse, Point subclass.

        '''
        f = Point(self.center)
        
        if self.xAxisIsMajor:
            f.x -= self.linearEccentricity
        else:
            f.y -= self.linearEccentricity
        return f
               
    @property
    def f0(self):
        '''
        Shorthand notation for focus0, Point subclass
        '''
        return self.focus0

    @property
    def focus1(self):
        '''
        Second focus of the ellipse, Point subclass.
        '''
        f = Point(self.center)

        if self.xAxisIsMajor:
            f.x += self.linearEccentricity
        else:
            f.y += self.linearEccentricity
        return f

    @property
    def f1(self):
        '''
        Shorthand notation for focus1, Point subclass
        '''
        return self.focus1

    @property
    def foci(self):
        '''
        A list containing the ellipse's foci, list.

        '''
        return [self.focus0,self.focus1]

    @property
    def majorAxis(self):
        '''
        A line coincident with the ellipse's major axis, Segment subclass.
        The major axis is the largest distance across an ellipse.

        '''
        return Segment(self.a_neg,self.a)

    @property
    def minorAxis(self):
        '''
        A line coincident with the ellipse' minor axis, Segment subclass.
        The minor axis is the smallest distance across an ellipse.

        '''
        return Segment(self.b_neg,self.b)

    @property
    def isCircle(self):
        '''
        Is true if the major and minor axes are equal, boolean.

        '''
        return self.x_radius == self.y_radius

    @property
    def isEllipse(self):
        '''
        Is true if the major and minor axes are not equal, boolean.

        '''
        return self.x_radius != self.y_radius



class Circle(Ellipse):
    '''
    XXX missing doc string
    '''

    @classmethod
    def inscribedInRectangle(cls,rectangle):
        raise NotImplemented('inscribedInRectangle')

    @classmethod
    def inscribedInTriangle(cls,triangle):
        raise NotImplemented('inscribedInTriangle')
        pass

    @classmethod
    def circumscribingRectangle(cls,rectangle):
        raise NotImplemented('circumscribingRectangle')

    @classmethod
    def circumscribingTriangle(cls,triangle):
        raise NotImplemented('circumscribingTriangle')


    @classmethod
    def circumscribingPoints(cls,points):
        '''
        :param: points - list of at least two Point subclasses
        :return: Circle

        '''
        raise NotImplemented('circumscribingPoints')
    

    def __init__(self,radius=1.0,origin=None):
        '''
        :param: radius - float 
        :param: origin - Point subclass initializer

        Returns a circle in the XY plane.

        '''
        self.radius = radius
        self.origin = origin

    @property
    def origin(self):
        '''
        The origin of the circle, Point subclass.
        
        Defaults to (0,0).
        '''
        return self.center

    @origin.setter
    def origin(self,newValue):
        self.center = newValue
        
    '''
    Shorthand notation for origin, Point subclass.
    '''
    @property
    def O(self):
        return self.origin

    @O.setter
    def O(self,newValue):
        self.center = newValue
        
    @property
    def radius(self):
        '''
        The circle's radius, float.

        Defaults to 1.0.
        '''
        return self.x_radius

    @radius.setter
    def radius(self,newValue):
        self.x_radius = newValue
        self.y_radius = newValue

    @property
    def r(self):
        '''
        Shorthand notation for radius, float.
        '''
        return self.x_radius

    @r.setter
    def r(self,newValue):
        self.radius = newValue

    @property
    def diameter(self):
        '''
        The circle's diameter, float.
        '''
        return self.radius * 2

    @property
    def circumfrence(self):
        '''
        The circle's circumfrence, float.
        '''
        return 2 * math.pi * self.radius

    @property
    def area(self):
        '''
        The circle's area, float.
        '''
        return  math.pi * (self.radius**2)

    @property
    def volume(self):
        '''
        The circle's volume, float.
        '''
        return (4./3.) * math.pi * (self.radius**3)
        

    def __eq__(self,other):
        '''
        :param: other - Circle subclass
        :return: boolean

        True if self.origin == other.origin 
                and 
                self.radius == other.radius.
        '''
        if self.radius != other.radius:
            return False
        
        return self.origin == other.origin

    def __hash__(self):
        '''
        '''
        # this will cause circles to hash to points
        return hash(self.origin)
        

    def __contains__(self,point):
        '''
        :param: Point subclass
        :return: boolean

        Returns True if the distance from the origin to the point
        is less than or equal to the radius.
        '''
        return point.distance(self.origin) <= self.radius

    def __repr__(self):
        '''
        Representative string for a circle instance.
        '''
        return '%s(%s,%.2f' % (self.__class__.__name,
                               str(self.origin),
                               self.radius)


    def __add__(self,other):
        '''
        x + y => Circle(x.radius+y.radius,x.origin.midpoint(y.origin))
        
        Returns a new Circle object.
        '''

        try:
            return Circle(self.radius+other.radius,
                          self.origin.midpoint(other.origin))
        except AttributeError:
            return self.__radd__(other)

    def __radd__(self,other):
        '''
        x + y => Circle(x.radius+y,x.origin)

        Returns a new Circle object.
        '''
        # other isn't a circle
        return Circle(self.radius+other,self.origin)

    def __iadd__(self,other):
        '''
        x += y => 
          x.origin += y.origin
          x.origin /= 2
          x.radius += y.radius

        Updates the current object.
        '''
        try:
            self.origin += other.origin
            self.origin /= 2.
            self.radius += other.radius
        except AttributeError:
            self.radius += other
        return self


    def __sub__(self,other):
        '''
        x - y => 

        Returns a new Circle object.
        '''
        raise NotImplemented('__sub__')

    def __rsub__(self,other):
        '''
        x - y => 

        Returns a new Circle object.
        '''
        raise NotImplemented('__rsub__')

    def __isub__(self,other):
        '''
        x -= y

        Updates the current object.
        '''
        raise NotImplemented('__isub__')

    def __mul__(self,other):
        '''
        x * y => 

        Returns a new Circle object.
        '''
        raise NotImplemented('__mul__')

    def __rmul__(self,other):
        '''
        x * y => 

        Returns a new Circle object.
        '''
        raise NotImplemented('__rmul__')

    def __imul__(self,other):
        '''
        x *= y

        Returns a new Circle object
        Updates the current object..
        '''
        raise NotImplemented('__imul__')

    def __floordiv__(self,other):
        '''
        x // y =>

        Returns a new Circle object.
        '''
        raise NotImplemented('__floordiv__')
    
    def __rfloordiv__(self,other):
        '''
        x // y =>

        Returns a new Circle object.
        '''  
        raise NotImplemented('__rfloordiv__')
    
    def __ifloordiv__(self,other):
        '''
        x //= y

        Updates the current object.
        '''
        raise NotImplemented('__rfloordiv__')

    def __truediv__(self,other):
        '''
        x / y =>

        Returns a new Circle object.
        '''
        raise NotImplemented('__truediv__')
    
    def __rtruediv__(self,other):
        '''
        x / y =>

        Returns a new Circle object.
        '''  
        raise NotImplemented('__rtruediv__')
    
    def __itruediv__(self,other):
        '''
        x /= y

        Updates the current object.
        '''
        raise NotImplemented('__rtruediv__')

    def __mod__(self,other):
        '''
        x % y 

        Returns a new Circle object
        '''
        raise NotImplemented('__mod__')
    
    def __rmod__(self,other):
        '''
        x % y 

        Returns a new Circle object
        '''
        raise NotImplemented('__rmod__')

    def __imod__(self,other):
        '''
        x %= y 

        Updates the current object.
        '''
        raise NotImplemented('__imod__')

    def __pow__(self,other):
        '''
        x ** y 

        Returns a new Circle object
        '''
        raise NotImplemented('__pow__')
    
    def __rpow__(self,other):
        '''
        x ** y 

        Returns a new Circle object
        '''
        raise NotImplemented('__rpow__')

    def __ipow__(self,other):
        '''
        x **= y 

        Updates the current object.
        '''
        raise NotImplemented('__ipow__')

    def __neg__(self):
        '''
        -x

        '''
        raise NotImplemented('__neg__')

    def __pos__(self):
        '''
        +x

        '''
        raise NotImplemented('__pos__')    

    def doesIntersect(self,other):
        '''
        :param: other - Circle subclass

        Returns True iff:
          self.orgin.distance(other.origin) <= self.radius+other.radius

        '''
        return self.origin.distance(other.origin) <= (self.radius+other.radius)
        
