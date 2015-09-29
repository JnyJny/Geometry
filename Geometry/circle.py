'''a pythonic Circle

Super awesome.
'''

import math
from .point import Point
from .rectangle import Rectangle
from .triangle import Triangle

class Circle(object):

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
        self.origin = origin
        self.radius = radius

    @property
    def origin(self):
        '''
        The origin of the circle, Point subclass.
        
        Defaults to (0,0).
        '''
        try:
            return self._origin
        except AttributeError:
            pass
        self._origin = Point()
        return self._origin

    @origin.setter
    def origin(self,initializer):
        self._origin = Point(initializer)
        
    '''
    Shorthand notation for origin, Point subclass.
    '''
    @property
    def O(self):
        return self.origin

    @O.setter
    def O(self,newValue):
        self.origin = newValue
        
    @property
    def radius(self):
        '''
        The circle's radius, float.

        Defaults to 1.0.
        '''
        
        try:
            return self._radius
        except AttributeError:
            pass
        self._radius = 1.0
        return self._radius

    @radius.setter
    def radius(self,newValue):
        self._radius = float(newValue)

    @property
    def r(self):
        '''
        Shorthand notation for radius, float.
        '''
        return self.radius

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
        
