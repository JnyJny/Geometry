'''a pythonic Point

It's three dimensional and super flexible. 
The foundation of Euclidean space.

This one is badass.
'''

import random
import math
import hashlib

from .constants import *
from .exceptions import *

class Point(object):
    ordinateNamesAll = 'xyzw'
    ordinateNamesXYZ = 'xyz'
    ordinateNamesXY = 'xy'
    ordinateNamesYZ = 'yz'
    ordinateNamesXZ = 'xz'
    ordinateNameX = 'x'
    ordinateNameY = 'y'
    ordinateNameZ = 'z'
    ordinateNameW = 'w'

    
    

    @classmethod
    def gaussian(cls,mu=0,sigma=1):
        '''
        :param: mu    - mean
        :param: sigma - standard deviation

        Returns a point whose coordinates were picked from a Gaussian
        distribution with mean 'mu' and standard deviation 'sigma'.

        '''
        return cls(random.gauss(mu,sigma),
                   random.gauss(mu,sigma),
                   random.gauss(mu,sigma))
        
    @classmethod
    def randomLocationInRectangle(cls,width,height,origin=None,depth=0):
        '''
        :param: width  - integer describing max X coordinate relative to origin
        :param: height - integer describing max Y coordinate relative to origin
        :param: origin - Point subclass specifying origin of rectangle
        :param: depth  - integer describing max Z coordinate relative to origin
        :return: Point subclass initialized with random X,Y and optionally Z

        If the caller does not supply an origin paramter, (0,0) is assumed.

        If the caller supplies a dimension as zero, that coordinate is not
        randomized and is set to zero.

        e.g:

        p = Point.randomLocation(width=0,height=20,depth=10)

        The point 'p' will have coordinates in the YZ plane:
          x : 0
          y : origin.y <= y <= origin.y + height
          z : origin.z <= z <= origin.z + depth
        
        The default signature supports creating rectangles in the XY plane.

        '''
        if origin is None:
            origin = cls()

        O = cls()
        O += origin             # this will typically be a no-op

        x,y,z = 0,0,0

        if width:
            x = random.randint(O.x,O.x+width)
            
        if height:
            y = random.randint(O.y,O.y+height)
            
        if depth:
            z = random.randint(O.z,O.z+depth)
            
        return cls(x,y,z)
    
    @classmethod
    def randomLocation(cls,radius,origin=None):
        '''
        :param: radius - float
        :param: origin - optional Point subclass
        :return: Point sublcass

        Returns a point with random x,y coordinates within the circle
        determined (origin, radius).
        
        If origin is not supplied, (0,0) is assumed.
        '''
        
        if origin is None:
            origin = cls()

        O = cls()
        O += origin

        
        t = 2.0 * math.pi * random.random()
        r = random.random() * random.random()
        if r > 1:
            r = 2 - r
            
        x = int(radius * r * math.cos(t) + O.x)
        y = int(radius * r * math.sin(t) + O.y)
        
        return cls(x,y)
    
    def __init__(self,*args,**kwds):
        '''
        Called with no arguments will return an object initialized with zeros.

        Note: Subclasses should always return an object initialized
              with origin coordinates if called with no arguments.
              If not, things will break.

        You can initialize this thing practically any way that makes sense!

        	a = Point()
                b = Point(None)
        	c = Point(x)
        	d = Point(x,y)
        	e = Point(x,y,z)
        	f = Point([x])
        	g = Point([x,y])
        	h = Point([x,y,z])
                i = Point({'x':x,'y':y,'z':z})
        	j = Point(Point(...))
        	k = Point(x=x,y=y,z=z)
                l = Point(<some object that has x,y,z attributes>)

        Origins:
               Point()
               Point(None)
               Point([])
               Point({})
               Point(<any initializer composed of zeros>)

        '''

        nargs = len(args)
        
        if nargs == 0 and len(kwds) == 0:
            return

        if nargs == 1:
            if args[0] is None:
                return
            self.xyz = args[0]
            
        if nargs > 1:
            self.xyz = args

        self.xyz = kwds

    @property
    def x(self):
        '''
        X axis ordinate, float.
        '''
        try:
            return self._x
        except AttributeError:
            self._x = 0.
        return self._x

    @x.setter
    def x(self,newValue):

        try:
            self._x = float(newValue)
            return
        except TypeError:
            pass
        
        try:
            self._x = float(newValue[0])
            return
        except (KeyError,TypeError):
            pass
        
        try:
            self._x = float(newValue[self.__class__.ordinateNameX])
            return
        except KeyError:
            return
        except TypeError:
            pass

        try:
            self._x = float(getattr(newValue,self.__class__.ordinateNameX))
            return
        except AttributeError:
            pass

        raise UngrokkableObject(newValue)

    @property
    def y(self):
        '''
        Y axis ordinate, float.
        '''
        try:
            return self._y
        except AttributeError:
            self._y = 0.
        return self._y

    @y.setter
    def y(self,newValue):

        try:
            self._y = float(newValue)
            return
        except TypeError:
            pass

        try:
            self._y = float(newValue[0])
            return
        except (KeyError,TypeError):
            pass

        try:
            self._y = float(newValue[self.__class__.ordinateNameY])
            return
        except KeyError:
            return
        except TypeError:
            pass        

        try:
            self._y = float(getattr(newValue,self.__class__.ordinateNameY))
            return
        except AttributeError:
            pass
        raise UngrokkableObject(newValue)



    @property
    def z(self):
        '''
        Z axis ordinate, float.
        '''
        try:
            return self._z
        except AttributeError:
            self._z = 0.0
        return self._z

    @z.setter
    def z(self,newValue):
        
        try:
            self._z = float(newValue)
            return
        except TypeError:
            pass

        try:
            self._z = float(newValue[0])
            return
        except (KeyError,TypeError):
            pass

        try:
            self._z = float(newValue[self.__class__.ordinateNameZ])
            return
        except KeyError:
            return
        except TypeError:
            pass        

        try:
            self._z = float(getattr(newValue,self.__class__.ordinateNameZ))
            return
        except AttributeError:
            pass

        raise UngrokkableObject(newValue)
        

    @property
    def w(self):
        '''
        W parameter to make square matrices.
        '''
        return 1.0

    @property
    def xyz(self):
        '''
        Returns an array [x,y,z].
        '''
        return [self.x,self.y,self.z]

    @xyz.setter
    def xyz(self,iterable):
        '''
        Set the values of x, y and z with obj, where obj can be:
        1. an iterable with 1, 2 or 3 items
        2. an object defining x, y, or z attributes 
        3. a dictionary with x, y, or z keys
        4. a scalar float, only sets x

        '''

        if self._complex_setter(iterable,self.__class__.ordinateNamesXYZ):
            return
        
        # straight iteration, hope for three items
        try:
            self.x,self.y,self.z = iterable[:3]
            return
        except (TypeError,ValueError):
            # not iterable
            # unpack error, not enough values to unpack
            pass
        
        # hand off to xy.setter
        self.xy = iterable


    @property
    def xyzw(self):
        '''
        Returns an array of [x,y,z,1]
        '''
        return [self.x,self.y,self.z,self.w]
    
    @xyzw.setter
    def xyzw(self,iterable):
        '''
        Set the values of x, y and z. Values for w are ignored.
        '''
        self.xyz = iterable

    @property
    def xy(self):
        '''
        Returns an array of [x,y]
        '''
        return [self.x,self.y]

    @xy.setter
    def xy(self,iterable):
        '''
        Set the values of x and z with an iterable.
        '''

        if self._complex_setter(iterable,self.__class__.ordinateNamesXY):
            return

        try:
            self.x,self.y = iterable
            return
        except (ValueError,TypeError):
            pass
        
        self.x = iterable

    @property
    def yz(self):
        '''
        Returns an array of [y,z]
        '''
        return [self.y,self.z]

    @yz.setter
    def yz(self,iterable):
        '''
        Set the values of y and z with an iterable.
        '''

        if self._complex_setter(iterable,self.__class__.ordinateNamesYZ):
            return

        try:
            self.y,self.z = iterable
            return
        except (ValueError,TypeError):
            pass

        self.y = iterable

    @property
    def xz(self):
        '''
        Returns an array of [x,z]
        '''
        return [self.x,self.z]

    @xz.setter
    def xz(self,iterable):
        '''
        Set the values of x and z with an iterable.
        '''

        if self._complex_setter(iterable,self.__class__.ordinateNamesXZ):
            return
        
        try:
            self.x,self.z = iterable
            return
        except (ValueError,TypeError):
            pass
        
        self.x = iterable

    @property
    def bytes(self):
        '''
        A bytes buffer of repr(self) encoded with utf-8.
        '''
        return bytes(repr(self),'utf-8')
    

    def __str__(self):
        return '(%s)' %(','.join([str(v) for v in self.xyz]))

    def __repr__(self):
        '''
        :return: string

        String representation of the current instance.
        '''
        return '%s%s' % (self.__class__.__name__,str(self))


    def __hash__(self):
        '''
        :return: integer

        Hash function is hashlib.sha1 and the text is the bytes property.
        '''
        return int(hashlib.sha1(self.bytes).hexdigest(),16)

    
    def _vfunc(self,iterable,func):
        '''
        :param: iterable - something that iterates
        :param: func     - function that takes a list as an argument 
        :return: list

        Zips self with iterable and applies func to each pair, returning
        a list of results for each func invocation.
        '''
        return [func(v) for v in zip(self,iterable)]

    def _ifunc(self,other,func):
        '''
        :param: other - scalar or iterable or object 
        :return: None

        Applies func to self to implement incremental operators.
        '''
        for index,name in enumerate(self.__class__.ordinateNamesXYZ): 
            current = getattr(self,name)
            try:
                operand = getattr(other,name)
            except AttributeError:
                try:
                    operand = other[index]
                except TypeError:
                    operand = other
                except IndexError:
                    return
            setattr(self,name,func((current,operand)))    

    def __eq__(self,other):
        '''
        a.x == b.x and a.y == b.y and a.z == b.z
        
        Returns boolean.
        '''
        return all(self._vfunc(other,lambda p:p[0] == p[1]))

    def __add__(self,other):
        '''
        a.x + b.x, a.y + b.y, a.z + b.z

        Returns a new object.
        '''
        try:
            return Point(self.x+other.x,self.y+other.y,self.z+other.z)
        except AttributeError:
            return self.__radd__(other)

    def __radd__(self,iterable):
        '''
        a.x + b[0], a.y + b[1], a.z + b[2]

        or 

        a.x + b, a.y + b, a.z + b  if b does not support iteration

        Returns a new object.
        '''
        
        try:
            return Point(self._vfunc(iterable,lambda p:p[0]+p[1]))
        except TypeError:
            return Point(self.x+iterable,self.y+iterable,self.z+iterable)

    def __iadd__(self,iterable):
        '''
        a.x += b.x || a.x += b[0] || a.x += b
        a.y += b.y || a.y += b[1] || a.y += b
        a.z += b.z || a.z += b[2] || a.z += b
        
        Updates self.
        '''
        self._ifunc(iterable,lambda p:p[0]+p[1])
        return self

    def __sub__(self,other):
        '''
        a.x - b.x, a.y - b.y, a.z - b.z

        Returns a new object.
        '''
        try:
            return Point(self.x-other.x,self.y-other.y,self.z-other.z)
        except AttributeError:
            return self.__rsub__(other)

    def __rsub__(self,iterable):
        '''
        a.x - b, a.y - b, a.z - b

        Returns a new object.
        '''
        try:
            return Point(self._vfunc(iterable,lambda p:p[0]-p[1]))
        except TypeError:
            return Point(self.x-iterable,self.y-iterable,self.z-iterable)

    def __isub__(self,iterable):
        '''
        a.x -= b.x || a.x -= b[0] || a.x -= b
        a.y -= b.y || a.y -= b[1] || a.y -= b
        a.z -= b.z || a.z -= b[2] || a.z -= b

        Updates self.
        '''
        self._ifunc(iterable,lambda p:p[0]-p[1])
        return self
    
    def __mul__(self,other):
        '''
        a.x * b.x, a.y * b.y, a.z * b.z

        Returns a new object.
        '''
        try:
            return Point(self.x * other.x,self.y * other.y,self.z * other.z)
        except AttributeError:
            return self.__rmul__(other)

    def __rmul__(self,iterable):
        '''
        a.x * b, a.y * b, a.z * b

        Returns a new object.
        '''
        try:
            return Point(self._vfunc(iterable,lambda p:p[0]*p[1]))
        except TypeError:
            return Point(self.x*iterable,self.y*iterable,self.z*iterable)

    def __imul__(self,iterable):
        '''
        a.x *= b.x || a.x *= b[0] || a.x *= b
        a.y *= b.y || a.y *= b[1] || a.y *= b
        a.z *= b.z || a.z *= b[2] || a.z *= b

        Updates self.
        '''
        self._ifunc(iterable,lambda p:p[0] * p[1])
        return self

    def __truediv__(self,other):
        '''
        a.x / b.x, a.y / b.y, a.z / b.z

        Returns a new object.
        '''
        try:
            try:
                return Point(self.x / other.x,self.y / other.y,self.z / other.z)
            except AttributeError:
                self.__rtruediv__(other)
        except ZeroDivisionError:
            pass
        
        raise ZeroDivisionError('zero present in %s' %(other))
                

    def __rtruediv__(self,other):
        '''
        a.x / b, a.y / b, a.z / b

        Returns a new object.
        '''
        try:
            return Point(self._vfunc(other,lambda p:p[0]/p[1]))
        except TypeError:
            return Point(self.x / other,self.y / other,self.z / other)

    def __itruediv__(self,iterable):
        '''
        a.x /= b.x || a.x /= b[0] || a.x /= b
        a.y /= b.y || a.y /= b[1] || a.y /= b
        a.z /= b.z || a.z /= b[2] || a.z /= b

        Updates self.
        '''
        try:
            self._ifunc(iterable,lambda p:p[0] / p[1])
            return self
        except ZeroDivisionError:
            pass

        raise ZeroDivisionError('zero present in %s' %(iterable))

    def __floordiv__(self,other):
        '''
        a.x // b.x, a.y // b.y, a.z // b.z

        Returns a new object.
        '''
        try:
            try:
                return Point(self.x // other.x,
                             self.y // other.y,
                             self.z // other.z)
            except AttributeError:
                return self.__rfloordiv__(other)
        except ZeroDivisionError:
            pass
        raise ZeroDivisionError('zero present in %s' %(iterable))

    def __rfloordiv__(self,other):
        '''
        a.x // b, a.y // b, a.z // b

        Returns a new object.
        '''
        try:
            try:
                return Point(self._vfunc(other,lambda p:p[0]//p[1]))
            except TypeError:
                return Point(self.x // other,self.y // other,self.z // other)
        except ZeroDivisionError:
            pass
        
        raise ZeroDivisionError('zero present in %s' %(iterable))

    def __ifloordiv__(self,iterable):
        '''
        a.x //= b.x || a.x //= b[0] || a.x //= b
        a.y //= b.y || a.y //= b[1] || a.y //= b
        a.z //= b.z || a.z //= b[2] || a.z //= b

        Updates self.

        Tip: p //= 1 is a quick way to floor all coordinates.
        '''
        try:
            self._ifunc(iterable,lambda p:p[0] // p[1])
            return self
        except ZeroDivisionError:
            pass
        raise ZeroDivisionError('zero present in %s' %(iterable))
            
    def __mod__(self,other):
        '''
        a.x % b.x, a.y % b.y, a.z % b.z

        Returns a new object.
        '''

        try:
            try:
                return Point(self.x % other.x,self.y % other.x,self.z % other.z)
            except AttributeError:
                return self.__rmod__(other)
        except ZeroDivisionError:
            pass
        raise ZeroDivisionError('zero present in %s' % (other))

    def __rmod__(self,other):
        '''
        a.x % b, a.y % b, a.z % b

        Returns a new object.
        '''
        try:
            return Point(self._vfunc(other,lambda p:p[0]%p[1]))
        except TypeError:
            return Point(self.x % other,self.y % other,self.z % other)

    def __imod__(self,iterable):
        '''
        a.x %= b.x || a.x %= b[] || a.x %= b
        a.y %= b.y || a.y %= b[] || a.y %= b
        a.z %= b.z || a.z %= b[] || a.z %= b

        Updates self.
        '''
        try:
            self._ifunc(iterable,lambda p:p[0] % p[1])
            return self
        except ZeroDivisionError:
            pass
        raise ZeroDivisionError('zero present in %s' % (iterable))

    def __pow__(self,other):
        '''
        a.x ** b.x, a.y ** b.y, a.z ** b.z
        
        Returns a new object.
        '''
        try:
            return Point(self.x**other.x,self.y**other.y,self.z**other.z)
        except AttributeError:
            return self.__rpow__(other)

    def __rpow__(self,other):
        '''
        a.x ** b, a.y ** b, a.z ** b
        
        Returns a new object.
        '''
        try:
            return Point(self._vfunc(other,lambda p:p[0] ** p[1]))
        except TypeError:
            return Point(self.x**other,self.y**other,self.z**other)

    def __ipow__(self,iterable):
        '''
        a.x **= b.x || a.x **= b[0] || a.x **= b
        a.y **= b.y || a.y **= b[1] || a.y **= b
        a.z **= b.z || a.z **= b[2] || a.z **= b

        Updates self.
        '''
        self._ifunc(iterable,lambda p:p[0] ** p[1])
        return self

    def __neg__(self):
        '''
        a.x * -1, a.y * -1, a.z * -1

        Returns a new object.
        '''
        
        return self * -1
    
    def __pos__(self):
        '''
        a.x * 1, a.y * 1, a.z * 1

        Returns self.
        '''
        return self

    def __abs__(self):
        '''
        abs(a.x),abs(a.y),abs(a.z)

        Returns a new object.
        '''
        
        return Point(abs(self.x),abs(self.y),abs(self.z))
    
    def __invert__(self):
        '''
        ~int(a.x),~int(a.y),~int(a.z)

        Returns a new object.
        '''
        return Point(~int(self.x),~int(self.y),~int(self.z))

    def __len__(self):
        '''
        Returns the length of the Point if viewed as vector, excluding 'w'.
        '''
        return 3
    
    def __iter__(self):
        '''
        Returns a list iterator over the values of 'x', 'y', and 'z'.
        '''
        return iter(self.xyz)

    def __getitem__(self,key):
        '''
        :param: key - integer
        :return: float 
        
        p = Point()
        p[0,1,2,3] == p.[x,y,z,w]

        Treat the point like a one dimensional vector with four entries.
        '''
        try:
            return getattr(self,self.__class__.ordinateNamesAll[key])
        except IndexError:
            pass
        
        raise IndexError( 'index %d out of range' % (key))

    def __setitem__(self,key,value):
        '''
        Treat the point like a one dimensional vector with three entries.

        Attempts to set 'w' are ignored without raising an error.
        '''
        setattr(self,self.__class__.ordinateNamesAll[key],value)


    def _complex_setter(self,obj,keys):
        '''
        :param: obj  - object of unknown pedigree
        :param: keys - list of strings 
        :return: boolean

        This method attempts to find values of attributes named by 'keys'
        defined in 'obj' and use them to set the values of attributes in
        self.

        Returns True if at least zero or more values is found without
        incurring an exception.
        '''

        try:
            if len(obj) == 0:
                # obj doesn't contain anything, we're done
                return True
        except TypeError:
            # obj doesn't implement __len__, probably a scalar, maybe.
            pass
        
        found = False
        for key in keys:
            try:
                val = obj[key]
            except KeyError:
                # obj is a dict, key not present
                continue
            except TypeError:
                # obj is not a dict, check for named attributes
                try:
                    val = getattr(obj,key)
                except AttributeError:
                    continue
            setattr(self,key,val)
            found = True

        return found        


    def dot(self,other):
        '''
        :param: other - Point subclass
        :return: float

        Dot product.

        The dot product of a and b is a scalar value.
        '''
        return sum(self * other)

    def cross(self,other):
        '''
        :param: other - Point subclass
        :return: float

        Vector cross product.

        U x V = (u1*i + u2*j + u3*k) x (v1*i + v2*j + v3*k)

        s1 = u2v3 - u3v2
        s2 = u3v1 - u1v3
        s3 = u1v2 - u2v1

        Returns s1 + s2 + s3
        '''

        if self.z and other.z:
            s0 = (self.y*other.z) - (self.z*other.y)
            s1 = (self.z*other.x) - (self.x*other.z)
        else:
            s0 = 0
            s1 = 0
    
        s2 = (self.x*other.y) - (self.y*other.x)

        return s0 + s1 + s2

    def midpoint(self,other):
        '''
        :param: other - Point subclass
        :return: Point subclass
        
        Point midway between 'a' and 'b'.

        '''
        m = self + other  # create a new point
        m /= 2.           # scale it by half
        return m

    def isBetweenX(self,a,b):
        '''
        :param: a - Point subclass
        :param: b - Point subclass
        :return: boolean
        
        Return True if self.x is >= min(a.x,b.x) and <= max(a.x,b.x)
        '''
        minX,maxX = min(a.x,b.x),max(a.x,b.x)
        
        return (self.x >= minX) and (self.x <= maxX)

    def isBetweenY(self,a,b):
        '''
        :param: a - Point subclass
        :param: b - Point subclass
        :return: boolean

        Returns True if self.y is >= min(a.y,b.y) and <= max(a.y,b.y)
        '''
        minY,maxY = min(a.y,b.y),max(a.y,b.y)
        
        return (self.y >= minY) and (self.y <= maxY)

    def isBetweenZ(self,a,b):
        '''
        :param: a - Point subclass
        :param: b - Point subclass
        :return: boolean

        Return True if self.z is >= min(a.z,b.z) and <= max(a.z,b.z)
        '''
        minZ,maxZ = min(a.z,b.z),max(a.z,b.z)
        
        return (self.z >= a.z) and (self.z <= b.z)

    def isBetween(self,a,b):
        '''
        :param: a - Point subclass
        :param: b - Point subclass
        :return: boolean

        Check to see if the calling object's coordinates are within the X, Y
        and Z ranges of the supplied points 'a' and 'b'.

        This is *NOT* a collinearity check.
        '''
        
        if not self.isBetweenX(a,b):
            return False

        if not self.isBetweenY(a,b):
            return False

        if not self.isBetweenZ(a,b):
            return False
        
        return True
    
    def distance(self,other=None):
        '''
        :param: other - Point subclass
        :return: float

        Calculates the Euclidean distance from other.
        
        If other is not specified, the origin is used.
        '''

        if other is None:
            other = self.__class__()
            
        return math.sqrt(sum((other - self) ** 2))

    def distanceSquared(self,other=None):
        '''
        :param: other - Point subclass
        :return: float 

        Calculates Euclidean distance squared from other. 

        If other is not specified, the origin is used.

        It will be faster in a loop when trying to determine an
        ordering of points by their distance from an arbitrary point.
        '''

        if other is None:
            other = self.__class__()
            
        return sum((other-self)**2)

    def isCollinear(self,b,c,axis='z'):
        '''
        :param: b - Point subclass
        :param: c - Point subclass
        :return: boolean

        Returns true if the three points (self, b and c) are collinear.
        '''
        return self.ccw(b,c,axis) == 0

    def isCCW(self,b,c,axis='z'):
        '''
        :param: b - Point subclass
        :param: c - Point subclass
        :return: boolean

        True if the angle formed by self,b,c has a counter-clockwise rotation.

        Can raise CollinearPoints() if self, b, and c all lie on the
        same line.
        '''
        
        result = self.ccw(b,c,axis)
        
        if result == 0:
            raise CollinearPoints(self,b,c)
        
        return result > 0

    def ccw(self,b,c,axis='z'):
        '''
        :param: b    - Point subclass
        :param: c    - Point subclass
        :param: axis - string specifying axis of rotation
        :return: float

        Returns an integer signifying whether the angle described by the
        points self,b,c has a counter-clockwise rotation around the specified
        axis.
        
        > 0 : counter-clockwise
          0 : points are collinear 
        < 0 : clockwise
        '''
        
        bsuba = b - self
        csuba = c - self

        if axis == 'z':
            return (bsuba.x * csuba.y) - (bsuba.y * csuba.x)

        if axis == 'y':
            return (bsuba.x * csuba.z) - (bsuba.z * csuba.x)
                
        if axis == 'x':
            return (bsuba.y * csuba.z) - (bsuba.z * csuba.y)

        raise ValueError("axis '%s' no recognized." % (axis))
                



