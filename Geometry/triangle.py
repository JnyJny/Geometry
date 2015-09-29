''' a pythonic Triangle

Tastes like chicken!
'''
from .point import Point
from .line import Segment
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
    vertexNameA = 'A'
    vertexNameB = 'B'
    vertexNameC = 'C'
    edgeNames = ['AB','BC','AC']
    edgeNameAB = 'AB'
    edgeNameBC = 'BC'
    edgeNameAC = 'AC'
    
    @classmethod
    def randomTriangle(cls,radius,origin=None):
        '''
        :param: radius - float
        :param: origin - optional Point subclass
        :return: Triangle

        Creates a triangle with random coordinates in the circle
        described by (origin,radius).  If origin is unspecified, (0,0)
        is assumed.
        '''
        pts = []
        while len(pts) < 3:
            pt = Point.randomLocation(radius,origin)
            if pt not in pts:
                pts.append(pt)
        return cls(pts)

    def __init__(self,*args,**kwds):
        
        if len(args) == 0 and len(kwds) == 0:
            return

        if len(args) == 1:
            self.ABC = args[0]
        else:
            self.ABC = args

        for name in self.vertexNames:
            try:
                setattr(self,name,kwds[name])
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
    def A(self,newValue):
        self._A.xyz = newValue

    @property
    def B(self):
        '''
        Vertex of triangle, Point subclass.
        '''
        try:
            return self._B
        except AttributeError:
            pass
        self._B = Point(1,0)
        return self._B
    
    @B.setter
    def B(self,newValue):
        self._B.xyz = newValue
        
    @property
    def C(self):
        '''
        Vertex of triangle, Point subclass.
        '''
        try:
            return self._C
        except AttributeError:
            pass
        self._C = Point(0,1)
        return self._C

    @C.setter
    def C(self,newValue):
        self._C.xyz = newValue
        
    @property
    def ABC(self):
        '''
        A list of the triangle's vertices, list.
        '''
        return [self.A,self.B,self.C]
    
    @ABC.setter
    def ABC(self,iterable):
        self.A,self.B,self.C = iterable
        
    @property
    def AB(self):
        '''
        Line segment with endpoints A and B, Segment subclass.
        '''
        return Segment(self.A,self.B)

    @property
    def AC(self):
        '''
        Line segment with endpoints A and C, Segment subclass.
        '''
        return Segment(self.A,self.C)

    @property
    def BC(self):
        '''
        Line segment with endpoints B and C, Segment subclass.
        '''
        return Segment(self.B,self.C)

    @property
    def vertices(self):
        return self.ABC
    
    @property
    def sides(self):
        '''
        List of line segments.
        '''
        return [self.AB,self.BC,self.AC]

    @property
    def hypotenuse(self):
        '''
        The longest side of the triangle.
        '''
        self.sides.sort(key=lambda pair:pair[0].distance(pair[1]))
        return self.sides[-1]

    @property
    def alpha(self):
        '''
        The angle described by CAB in radians, float.
        '''
        raise NotImplemented('alpha')

    @property
    def beta(self):
        '''
        The angle described by ABC in radians, float.
        '''
        raise NotImplemented('beta')

    @property
    def gamma(self):
        '''
        The angle described by BCA in radians, float.
        '''
        raise NotImplemented('gamma')

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
        return self.A.isCCW(self.B,self.C)

    @property
    def ccw(self):
        '''
        Result of ccw(A,B,C), float.
        '''
        return self.A.ccw(self.B,self.C)
    
    @property
    def area(self):
        '''
        Area of the triangle, float.
        '''
        return abs(self.ccw) / 2

    def height(self,side='AB'):
        '''
        :param: side - optional string
        :return: float

        The distance from the specified side to the opposite point.

        '''
        raise NotImplemented('height')
        
        
    def flip(self,side='AB'):
        '''
        :param: side - optional string
        :return: None

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
            return
        
        if side == 'BC':
            tmp = Point(self.B)
            self.B = self.C
            self.C = tmp
            return
        
        if side == 'AC':
            tmp = Point(self.A)
            self.A = self.C
            self.C = tmp
            return
        
        raise ValueError("Unknown side '%s' requested." % (side))
    
    def __contains__(self,point):
        '''
        :param: point - Point subclass
        :return: boolean

        Returns True if point is inside the triangle or
        lies on any of it's sides.
        '''
        try:
            results = [self.A.ccw(self.B,point),
                       self.B.ccw(self.C,point),
                       self.C.ccw(self.A,point)]
        except CollinearPoints:
            # point is on the lines AB, BC, or CA and that counts.
            return True
        
        return not (any([x>0 for x in results]) and any([x<0 for x in results]))

    def doesIntersect(self,other):
        '''
        :param: other - Triangle subclass
        :return: boolean

        Returns True iff:
            Any of other's vertices are contained within self or
            Any of self's vertices are contained within other.
        '''

        if any([v in self for v in other.vertices]):
            return True

        return any([v in other for v in self.vertices])
            
        
            
