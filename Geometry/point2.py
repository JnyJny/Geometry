'''
'''

import collections
import hashlib
import random
import math
from .constants import two_pi, pi_half
from .exceptions import CollinearPoints
from .propgen import FloatProperty, FloatMultiProperty


class Point(collections.Mapping):
    '''
    A three dimensional Point initialized with x,y and z values
    supplied or the origin if no ordinates are given. 

    Point initialization is very flexible! It can be initialized with
    zero to three positional parameters; 'x', 'y', 'z'.

    e.g:

    >> repr(Point())
    'Point(x=0.0, y=0.0, z=0.0)'
    >> repr(Point(1))
    'Point(x=1.0, y=0.0, z=0.0)'
    >> repr(Point(1,2))
    'Point(x=1.0, y=2.0, z=0.0)'
    >> repr(Point(1,2,3))
    'Point(x=1.0, y=2.0, z=3.0)'

    Of course, the Point can also be initialized with keyword
    arguments: x, y and z.

    >> repr(Point(z=1)
    'Point(x=0.0, y=0.0, z=1.0)'
    >> repr(Point(z=1,y=2,x=3)
    'Point(x=3.0, y=2.0, z=1.0)'

    Finally, Points can be initialized by mappings or sequences:

    >> repr(Point([4]*3))
    'Point(x=4.0, y=4.0, z=4.0)'
    >> repr(Point({'x':1,'y':2,'z':3,'foo':'whatevers'}))
    'Point(x=1.0, y=2.0, z=3.0)'

    Accessing the values of a Point are also very flexible. Each
    coordinate can be set/get individually via the properties 'x',
    'y' and 'z'. Coordinates can also be set/get in groups using
    the properties 'xy', 'xz', 'yz', 'xyz' and 'xyzw'.  Arguments
    to the setters can be mappings, sequences, or scalars. 

    Operations
    ==========

    +, -, *, /, //, %, **, +=, -=, *=, /=, //=, %=, **=, ==, !=

    Operands can be mappings, sequences or scalars. 

    Methods
    =======

                ccw: counter-clockwise function, also known as:
                     "The beating red heart of computational geometry."
                dot: dot product of two points
              cross: cross product of two points
           midpoint: point between two other points
           distance: Euclidean distance between points
    distanceSquared: Squared Euclidean distance
          isBetween: bounds checking a point between two other points
              isCCW: is angle ABC a counter-clockwise rotation?
        isCollinear: are points ABC collinear?

    Class Methods
    =============

      origin: a Point initialized to 0,0,0
        unit: converts vector AB to a unit vector
       units: list of three unit vectors on each axis
    gaussian: random Point with coordinates chosen from gaussian distribution.
      random: random Point within a circle
    
    '''
    x = FloatProperty('x')
    y = FloatProperty('y')
    z = FloatProperty('z')
    w = FloatProperty('w', default=1.0, readonly=True)
    xyzw = FloatMultiProperty('xyzw', readonly_keys='w')
    xyz = FloatMultiProperty('xyz')
    xy = FloatMultiProperty('xy')
    yz = FloatMultiProperty('yz')
    xz = FloatMultiProperty('xz')

    _keys = 'xyz'

    @classmethod
    def origin(cls):
        '''
        '''
        return cls(0, 0, 0)

    @classmethod
    def _convert(cls, other, ignoreScalars=False):
        '''
        Class private method for converting 'other' into a Point
        subclasss. If 'other' already is a Point subclass, nothing
        is done. If ignoreScalars is True and other is a float or int
        type, a TypeError exception is raised. 
        '''
        if ignoreScalars:
            if isinstance(other, (int, float)):
                msg = "unable to convert {} to {}".format(other, cls.__name__)
                raise TypeError(msg)

        return cls(other) if not issubclass(type(other), cls) else other

    @classmethod
    def unit(cls, A, B):
        '''
        :param: A - Point subclass
        :param: B - Point subclass
        :return: Point subclass

        Translates the vector AB to the origin and scales the length
        of the vector to one. 
        '''
        return (B - A) / A.distance(B)

    @classmethod
    def units(cls, scale=1):
        '''
        :param: scale - optional integer scale
        :return: list of three Point subclass

        Returns three points whose coordinates are the head of a
        unit vector from the origin ( conventionally i, j and k).

        '''
        return [cls(x=scale), cls(y=scale), cls(z=scale)]
                

    @classmethod
    def gaussian(cls, mu=0, sigma=1):
        '''
        :param: mu
        :param: sigma
        :return: Point subclass
        
        
        '''
        return cls(random.gauss(mu, sigma),
                   random.gauss(mu, sigma),
                   random.gauss(mu, sigma))

    @classmethod
    def random(cls, origin=None, radius=1):
        '''
        :param: origin
        :param: radius
        :return: Point subclass

        '''
        p = cls._convert(origin)

        r = random.uniform(0, radius)
        u = random.uniform(0, two_pi)
        v = random.uniform(-pi_half, pi_half)

        r_cosv = r * math.cos(v)

        p.x += r_cosv * math.cos(u)
        p.y += r_cosv * math.sin(u)
        p.z += radius * math.sin(v)

        return p

    def __init__(self, *args, **kwds):
        '''
        Initialize with:
        - positional arguments coresponding to x, y and z
        - keyword arguments: x, y and z
        - mappings
        - sequences
        '''

        self.x, self.y, self.z = 0.0, 0.0, 0.0

        if len(args) == 1:
            self.xyz = args[0]

        if len(args) > 1:
            self.xyz = args

        self.xyz = kwds

    def __setattr__(self, attr, value):
        '''
        Side-effect: deletes cached computed hash value if
                     x, y, or z attributes change. 
        '''
        super().__setattr__(attr, value)
        try:
            if attr[0] == '_' and attr[1] in self._keys:
                try:
                    del(self._hashvalue)
                except AttributeError:
                    pass
        except IndexError:
            pass

    def __hash__(self):
        '''
        Hash computed from the repr string. Re-computed if the
        object's repr string changes. 
        '''
        try:
            return self._hashvalue
        except AttributeError:
            pass
        digest = hashlib.sha1(bytes(repr(self), 'utf-8')).hexdigest()
        self._hashvalue = int(digest, 16)
        return self._hashvalue

    def __str__(self):
        '''
        '''
        return 'x={p.x}, y={p.y}, z={p.z}'.format(p=self)

    def __repr__(self):
        '''
        '''
        return '{p.__class__.__name__}({p!s})'.format(p=self)

    def __len__(self):
        '''
        Number of coordinates defined in a Point.
        '''
        try:
            return self._len
        except AttributeError:
            pass
        self._len = len(self._keys)
        return self._len

    def __bool__(self):
        '''
        Returns True iff all coordinates are non-zero.
        '''
        return all(self.values())

    def __iter__(self):
        '''
        '''
        self._ = list(self._keys)
        return self

    def __next__(self):
        '''
        When iterating, returns the mapping key for the next value. 
        '''
        try:
            return self._.pop(0)
        except IndexError:
            pass
        del(self._)
        raise StopIteration()

    def __getitem__(self, key):
        '''
        Recognizes keys:

        x, y, z, xy, yz, xz, xyz, xyzw, 0, 1, 2, 3

        Raises TypeError for any other key. 
        '''
        if key == 'x' or key == 0:
            return self.x
        if key == 'y' or key == 1:
            return self.y
        if key == 'z' or key == 2:
            return self.z
        if key == 'w' or key == 3:
            return self.w
        if key == 'xy':
            return (self.x, self.y)
        if key == 'yz':
            return (self.y, self.z)
        if key == 'xz':
            return (self.x, self.z)
        if key == 'xyz':
            return (self.x, self.y, self.z)
        if key == 'xyzw':
            return (self.x, self.y, self.z, self.w)
        raise TypeError(key)

    def __setitem__(self, key, newValue):
        '''
        Recognizes keys:

        x, y, z, xy, yz, xz, xyz, xyzw, 0, 1, 2

        Raises TypeError for any other key.
        '''
        if key == 'x' or key == 0:
            self.x = newValue
            return

        if key == 'y' or key == 1:
            self.y = newValue
            return

        if key == 'z' or key == 2:
            self.z = newValue
            return

        if key == 'xy':
            self.xy = newValue
            return

        if key == 'yz':
            self.yz = newValue
            return

        if key == 'xz':
            self.xz = newValue
            return

        if key == 'xyz' or key == 'xyzw':
            self.xyz = newValue
            return

        raise TypeError(key)

    
    def __eq__(self, other):
        '''
        a == b

        Returns boolean.
        '''
        try:
            b = self.__class__._convert(other)
        except:
            return False
        return all(u == v for u, v in zip(self.xyz, b.xyz))

    def _binary_(self, other, func, inplace=False):
        '''
        Implementation private method.

        All of the binary operations funnel thru this method to
        reduce cut-and-paste code and enforce consistent behavior
        of binary ops.

        Applies 'func' to 'self' and 'other' and returns the result.

        If 'inplace' is True the results of will be stored in 'self',
        otherwise the results will be stored in a new object.

        :param: other   mapping, array or scalar
        :param: func    callable with signature x(a,b)
        :param: inplace optional boolean
        :return: Point subclass
        '''

        dst = self if inplace else self.__class__(self)

        try:
            b = self.__class__._convert(other, ignoreScalars=True)
            dst.x = func(dst.x, b.x)
            dst.y = func(dst.y, b.y)
            dst.z = func(dst.z, b.z)
            return dst
        except TypeError:
            pass

        dst.x = func(dst.x, other)
        dst.y = func(dst.y, other)
        dst.z = func(dst.z, other)
        return dst

    def _unary_(self, func, inplace=False):
        '''
        Implementation private method.

        All of the unary operations funnel thru this method
        to reduce cut-and-paste code and enforce consistent
        behavior of unary ops.

        Applies 'func' to self and returns the result.

        If 'inplace' is True, the results are stored in 'self',
        otherwise the results will be stored in a new object.

        :param: func    callable with signature x(a)
        :param: inplace optional boolean
        :return: Point subclass

        '''
        dst = self if inplace else self.__class__(self)
        dst.x = func(dst.x)
        dst.y = func(dst.y)
        dst.z = func(dst.z)
        return dst

    def __add__(self, other):
        '''
        a.x + b.x || a.x + b[0] || a.x + b
        a.y + b.y || a.y + b[1] || a.y + b
        a.z + b.z || a.z + b[2] || a.z + b

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: a + b)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __radd__(self, other):
        '''

        b.x + a.x || b[0] + a.x || b + a.x
        b.y + a.y || b[1] + a.y || b + a.y
        b.z + a.z || b[2] + a.z || b + a.z

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: b + a)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __iadd__(self, other):
        '''
        a.x += b.x || a.x += b[0] || a.x += b
        a.y += b.y || a.y += b[1] || a.y += b
        a.z += b.z || a.z += b[2] || a.z += b

        Returns self.
        '''
        try:
            return self._binary_(other, lambda a, b: a + b, inplace=True)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __sub__(self, other):
        '''
        a.x - b.x || a.x - b[0] || a.x - b
        a.y - b.y || a.y - b[1] || a.y - b
        a.z - b.z || a.z - b[2] || a.z - b

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: a - b)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __rsub__(self, other):
        '''
        b.x - a.x || b[0] - a.x || b - a.x
        b.y - a.y || b[1] - a.y || b - a.y
        b.z - a.z || b[2] - a.z || b - a.z

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: b - a)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __isub__(self, other):
        '''
        a.x -= b.x || a.x -= b[0] || a.x -= b
        a.y -= b.y || a.y -= b[1] || a.y -= b
        a.z -= b.z || a.z -= b[2] || a.z -= b

        Returns self.
        '''
        try:
            return self._binary_(other, lambda a, b: a - b)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __mul__(self, other):
        '''
        a.x * b.x || a.x * b[0] || a.x * b
        a.y * b.y || a.y * b[1] || a.y * b
        a.z * b.z || a.z * b[2] || a.z * b

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: a * b)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __rmul__(self, other):
        '''
        b.x * a.x || b[0] * a.x || b * a.x
        b.y * a.y || b[1] * a.y || b * a.y
        b.z * a.z || b[2] * a.z || b * a.z

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: b * a)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __imul__(self, other):
        '''
        a.x *= b.x || a.x *= b[0] || a.x *= b
        a.y *= b.y || a.y *= b[1] || a.y *= b
        a.z *= b.z || a.z *= b[2] || a.z *= b

        Returns self.
        '''
        try:
            return self._binary_(other, lambda a, b: a * b, inplace=True)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __floordiv__(self, other):
        '''
        a.x // b.x || a.x // b[0] || a.x // b
        a.y // b.y || a.y // b[1] || a.y // b
        a.z // b.z || a.z // b[2] || a.z // b

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: a // b)
        except TypeError as e:
            err = TypeError(str(e))
        except ZeroDivisionError as e:
            err = ZeroDivisionError(str(e))
        raise err

    def __rfloordiv__(self, other):
        '''
        b.x // a.x || b[0] // a.x || b // a.x
        b.y // a.y || b[1] // a.y || b // a.y
        b.z // a.z || b[2] // a.z || b // a.z

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: b // a)
        except TypeError as e:
            err = TypeError(str(e))
        except ZeroDivisionError as e:
            err = ZeroDivisionError(str(e))
        raise err

    def __ifloordiv__(self, other):
        '''
        a.x //= b.x || a.x //= b[0] || a.x //= b
        a.y //= b.y || a.y //= b[1] || a.y //= b
        a.z //= b.z || a.z //= b[2] || a.z //= b

        Returns self.
        '''
        try:
            return self._binary_(other, lambda a, b: a // b, inplace=True)
        except TypeError as e:
            err = TypeError(str(e))
        except ZeroDivisionError as e:
            err = ZeroDivisionError(str(e))
        raise err

    def __truediv__(self, other):
        '''
        a.x / b.x || a.x / b[0] || a.x / b
        a.y / b.y || a.y / b[1] || a.y / b
        a.z / b.z || a.z / b[2] || a.z / b

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: a / b)
        except TypeError as e:
            err = TypeError(str(e))
        except ZeroDivisionError as e:
            err = ZeroDivisionError(str(e))
        raise err

    def __rtruediv__(self, other):
        '''
        b.x / a.x || b[0] / a.x || b / a.x
        b.y / a.y || b[1] / a.y || b / a.y
        b.z / a.z || b[2] / a.z || b / a.z

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: b / a)
        except TypeError as e:
            err = TypeError(str(e))
        except ZeroDivisionError as e:
            err = ZeroDivisionError(str(e))
        raise err

    def __itruediv__(self, other):
        '''
        a.x /= b.x || a.x /= b[0] || a.x /= b
        a.y /= b.y || a.y /= b[1] || a.y /= b
        a.z /= b.z || a.z /= b[2] || a.z /= b

        Returns self.
        '''
        try:
            return self._binary_(other, lambda a, b: a / b, inplace=True)
        except TypeError as e:
            err = TypeError(str(e))
        except ZeroDivisionError as e:
            err = ZeroDivisionError(str(e))
        raise err

    def __mod__(self, other):
        '''
        a.x % b.x || a.x % b[0] || a.x % b
        a.y % b.y || a.y % b[1] || a.y % b
        a.z % b.z || a.z % b[2] || a.z % b

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: a % b)
        except TypeError as e:
            err = TypeError(str(e))
        except ZeroDivisionError as e:
            err = ZeroDivisionError(str(e))
        raise err

    def __rmod__(self, other):
        '''
        b.x % a.x || b[0] % a.x || b % a.x
        b.y % a.y || b[1] % a.y || b % a.y
        b.z % a.z || b[2] % a.z || b % a.z

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: b % a)
        except TypeError as e:
            err = TypeError(str(e))
        except ZeroDivisionError as e:
            err = ZeroDivisionError(str(e))
        raise err

    def __imod__(self, other):
        '''
        a.x %= b.x || a.x %= b[0] || a.x %= b
        a.y %= b.y || a.y %= b[1] || a.y %= b
        a.z %= b.z || a.z %= b[2] || a.z %= b

        Returns self.
        '''
        try:
            return self._binary_(other, lambda a, b: a % b, inplace=True)
        except TypeError as e:
            err = TypeError(str(e))
        except ZeroDivisionError as e:
            err = ZeroDivisionError(str(e))
        raise err

    def __pow__(self, other, modulus=None):
        '''
        a.x ** b.x || a.x ** b[0] || a.x ** b
        a.y ** b.y || a.y ** b[1] || a.y ** b
        a.z ** b.z || a.z ** b[2] || a.z ** b


        Returns new object.
        '''
        fn = pow if modulus is None else lambda a, b: pow(
            int(a), int(b), modulus)
        try:
            return self._binary_(other, fn)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __rpow__(self, other, modulus=None):
        '''
        b.x ** a.x || b[0] ** a.x || b ** a.x
        b.y ** a.y || b[1] ** a.y || b ** a.y
        b.z ** a.z || b[2] ** a.z || b ** a.z

        Returns new object.
        '''
        fn = pow if modulus is None else lambda a, b: pow(
            int(b), int(a), modulus)
        try:
            return self._binary_(other, fn)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __ipow__(self, other, modulus=None):
        '''
        a.x **= b.x || a.x **= b[0] || a.x **= b
        a.y **= b.y || a.y **= b[1] || a.y **= b
        a.z **= b.z || a.z **= b[2] || a.z **= b

        Returns self.
        '''
        fn = pow if modulus is None else lambda a, b: pow(
            int(a), int(b), modulus)
        try:
            return self._binary_(other, fn, inplace=True)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __rshift__(self, other):
        '''
        a.x >> b.x || a.x >> b[0] || a.x >> b
        a.y >> b.y || a.y >> b[1] || a.y >> b
        a.z >> b.z || a.z >> b[2] || a.z >> b

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: int(a) >> int(b))
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __rrshift__(self, other):
        '''
        b.x >> a.x || b[0] >> a.x|| b >> a.x
        b.y >> a.y || b[1] >> a.y|| b >> a.y
        b.z >> a.z || b[2] >> a.z|| b >> a.z

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: int(b) >> int(a))
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __irshift__(self, other):
        '''
        a.x >> b.x || a.x >> b[0] || a.x >> b
        a.y >> b.y || a.y >> b[1] || a.y >> b
        a.z >> b.z || a.z >> b[2] || a.z >> b

        Returns self.
        '''
        try:
            return self._binary_(other, lambda a, b: int(a)
                                 >> int(b), inplace=True)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __lshift__(self, other):
        '''
        a.x << b.x || a.x << b[0] || a.x << b
        a.y << b.y || a.y << b[1] || a.y << b
        a.z << b.z || a.z << b[2] || a.z << b

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: int(a) << int(b))
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __rlshift__(self, other):
        '''
        b.x << a.x || b[0] << a.x|| b << a.x
        b.y << a.y || b[1] << a.y|| b << a.y
        b.z << a.z || b[2] << a.z|| b << a.z

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: int(b) << int(a))
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __ilshift__(self, other):
        '''
        a.x << b.x || a.x << b[0] || a.x << b
        a.y << b.y || a.y << b[1] || a.y << b
        a.z << b.z || a.z << b[2] || a.z << b

        Returns self.
        '''
        try:
            return self._binary_(other, lambda a, b: int(a)
                                 << int(b), inplace=True)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __and__(self, other):
        '''
        a.x & b.x || a.x & b[0] || a.x & b
        a.y & b.y || a.y & b[1] || a.y & b
        a.z & b.z || a.z & b[2] || a.z & b

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: int(a) & int(b))
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __rand__(self, other):
        '''
        b.x & a.x || b[0] & a.x|| b & a.x
        b.y & a.y || b[1] & a.y|| b & a.y
        b.z & a.z || b[2] & a.z|| b & a.z

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: int(b) & int(a))
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __iand__(self, other):
        '''
        a.x &= b.x || a.x &= b[0] || a.x &= b
        a.y &= b.y || a.y &= b[1] || a.y &= b
        a.z &= b.z || a.z &= b[2] || a.z &= b

        Returns self.
        '''
        try:
            return self._binary_(other, lambda a, b: int(a)
                                 & int(b), inplace=True)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __or__(self, other):
        '''
        a.x | b.x || a.x | b[0] || a.x | b
        a.y | b.y || a.y | b[1] || a.y | b
        a.z | b.z || a.z | b[2] || a.z | b

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: int(a) | int(b))
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __ror__(self, other):
        '''
        b.x | a.x || b[0] | a.x|| b | a.x
        b.y | a.y || b[1] | a.y|| b | a.y
        b.z | a.z || b[2] | a.z|| b | a.z

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: int(b) | int(a))
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __ior__(self, other):
        '''
        a.x | b.x || a.x | b[0] || a.x | b
        a.y | b.y || a.y | b[1] || a.y | b
        a.z | b.z || a.z | b[2] || a.z | b

        Returns self.
        '''
        try:
            return self._binary_(other, lambda a, b: int(a)
                                 | int(b), inplace=True)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __xor__(self, other):
        '''
        a.x ^ b.x || a.x ^ b[0] || a.x ^ b
        a.y ^ b.y || a.y ^ b[1] || a.y ^ b
        a.z ^ b.z || a.z ^ b[2] || a.z ^ b

        Returns new object.
        '''
        try:
            return self._binary_(other, lambda a, b: int(a) ^ int(b))
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __rxor__(self, other):
        '''
        b.x ^ a.x || b[0] ^ a.x|| b ^ a.x
        b.y ^ a.y || b[1] ^ a.y|| b ^ a.y
        b.z ^ a.z || b[2] ^ a.z|| b ^ a.z

        Returns new object.
        '''

        try:
            return self._binary_(other, lambda a, b: int(b) ^ int(a))
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    def __ixor__(self, other):
        '''
        a.x ^ b.x || a.x ^ b[0] || a.x ^ b
        a.y ^ b.y || a.y ^ b[1] || a.y ^ b
        a.z ^ b.z || a.z ^ b[2] || a.z ^ b

        Returns self.
        '''
        try:
            return self._binary_(other, lambda a, b: int(a)
                                 ^ int(b), inplace=True)
        except TypeError as e:
            err = TypeError(str(e))
        raise err

    # unary functions

    def __pos__(self):
        '''
        +a

        Returns self.
        '''
        return self

    def __neg__(self):
        '''
        -a

        Returns a new object with it's members negated.
        '''
        return self * -1

    def __abs__(self):
        '''
        abs(a.x),abs(a.y),abs(a.z)

        Returns self.
        '''
        return self._unary_(abs, inplace=True)

    def __invert__(self):
        '''
        ~int(a.x),~int(a.y),~int(a.z)

        Returns self.
        '''
        return self._unary_(lambda v: ~int(v), inplace=True)

    def __round__(self, n=0):
        '''
        round(a.x,n), round(a.y,n), round(a.z,n)

        Returns a new object.
        '''
        return self._unary_(lambda v: round(v, n))

    def __floor__(self):
        '''
        floor(a.x,n), floor(a.y,n), floor(a.z,n)

        Returns a new object.
        '''
        return self._unary_(math.floor)

    def __ceil__(self):
        '''
        ceil(a.x,n), ceil(a.y,n), ceil(a.z,n)

        Returns a new object.
        '''
        return self._unary_(math.ceil)

    def __trunc__(self):
        '''
        trunc(a.x), trunc(a.y), trunc(a.z)

        Returns new object.
        '''

        return self._unary_(math.trunc)

    def dot(self, other):
        '''
        Dot product of self and other, computed:

        a.x*b.x + a.y*b.y + a.z*b.z

        Returns a float
        '''
        return sum((self * other).values())

    def cross(self, other):
        '''
        Vector cross product of points U (self) and V (other), computed:

        U x V = (u1*i + u2*j + u3*k) x (v1*i + v2*j + v3*k)
        s1 = u2v3 - u3v2
        s2 = u3v1 - u1v3
        s3 = u1v2 - u2v1

        U x V = s1 + s2 + s3

        Returns a float.
        '''

        b = self.__class__._convert(other)

        return sum([(self.y * b.z) - (self.z * b.y),
                    (self.z * b.x) - (self.x * b.z),
                    (self.x * b.y) - (self.y * b.x)])

    def midpoint(self, other):
        '''
        The point midway between 'self' and 'other'.

        Returns a new object.
        '''

        return (self + self.__class__._convert(other)) / 2

    def isBetween(self, a, b, axes='xyz'):
        '''
        Checks the coordinates specified in 'axes' of 'self' to
        determine if they are bounded by 'a' and 'b'. The range
        is inclusive of end-points.

        Returns boolean.
        '''
        a = self.__class__._convert(a)
        b = self.__class__._convert(b)

        fn = lambda k: (self[k] >= min(a[k], b[k])) and (
            self[k] <= max(a[k], b[k]))

        return all(fn(axis) for axis in axes)

    def distance(self, other=None):
        '''
        The Euclidean distance from 'self' to 'other'.

        If 'other' is not specified, the origin is used.

        Returns a float.
        '''
        return math.sqrt(self.distanceSquared(other))

    def distanceSquared(self, other=None):
        '''
        Returns the squared Euclidean distance from 'self' to 'other'.

        If 'other' is not specified, the origin is used.

        Returns a float.

        Note: Use distanceSquared when ordering points by distance
              from an arbitrary point. Avoids a square root which can
              improve performance.
        '''
        return sum(((other - self) ** 2).values())

    def ccw(self, b, c, axis='z'):
        '''
        CCW - Counter Clockwise

        Returns an integer signifying the direction of rotation around 'axis'
        described by the angle b,self,c.

        > 0 : counter-clockwise
          0 : points are collinear
        < 0 : clockwise

        Returns an integer.

        Raises a ValueError if axis is not in 'xyz'.
        '''
        bsuba = b - self
        csuba = c - self

        if axis == 'z' or axis == 0:
            return (bsuba.x * csuba.y) - (bsuba.y * csuba.x)

        if axis == 'y' or axis == 1:
            return (bsuba.x * csuba.z) - (bsuba.z * csuba.x)

        if axis == 'x' or axis == 2:
            return (bsuba.y * csuba.z) - (bsuba.z * csuba.y)

        msg = "invalid axis '{!r}', must be one of {}".format(axis, self._keys)
        raise ValueError(msg)

    def isCCW(self, b, c, axis='z'):
        '''
        Returns True if the angle determined by a,self,b around 'axis'
        describes a counter-clockwise rotation, otherwise False.

        Raises CollinearPoints if self, b, c are collinear.
        '''

        result = self.ccw(b, c, axis)

        if result == 0:
            raise CollinearPoints(b, self, c)

        return result > 0

    def isCollinear(self, b, c):
        '''
        Returns True if 'self' is collinear with 'b' and 'c', otherwise False.
        '''

        return all(self.ccw(b, c, axis) == 0 for axis in self._keys)
