'''a pythonic Ellipse.

Super awesome.
'''

from .Point import Point
from .Line import Line

class Ellipse(object):

    def __init__(self,x_radius,y_radius,center=None):
        '''
        :param: x_radius  - float
        :param: y_radius  - float
        :param: center    - optional Point subclass initializer
        '''
        self.x_radius = x_radius
        self.y_radius = y_radius
        self.center   = center

    @property
    def x_radius(self):
        '''

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





    
