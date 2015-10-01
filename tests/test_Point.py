#!/usr/bin/env python3

import unittest
import sys
sys.path.append('..')
from Geometry import *

class TestObject(object):
    def __init__(self,x=None,y=None,z=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:            
            self.z = z

class Ungrokkable(object):
    pass

ZerosList   = [0]*3
OnesList    = [1]*3

ZerosDict   = {'x':0,'y':0,'z':0}
OnesDict    = {'x':1,'y':1,'z':1}

ZerosObject = TestObject(0,0,0)
OnesObject  = TestObject(1,1,1)

ZerosPoint  = Point()
OnesPoint   = Point(1,1,1)

class PointInitializationTestCase(unittest.TestCase):
    
    def testPointOriginCreation(self):
        self.assertListEqual(Point().xyz,ZerosList)
        self.assertListEqual(Point(None).xyz,ZerosList)
        self.assertListEqual(Point(()).xyz,ZerosList)
        self.assertListEqual(Point([]).xyz,ZerosList)
        self.assertListEqual(Point({}).xyz,ZerosList)
        self.assertListEqual(Point(Point()).xyz,ZerosList)
        self.assertListEqual(Point(ZerosList).xyz,ZerosList)
        self.assertListEqual(Point(ZerosDict).xyz,ZerosList)
        self.assertListEqual(Point(ZerosObject).xyz,ZerosList)

    def testPointWOrdinate(self):
        self.assertListEqual(Point().xyzw,[0,0,0,1])
        self.assertEqual(Point().w,1)

        with self.assertRaises(AttributeError):
            p = Point()
            p.w = 2

    def testCreatePointWithRegularArguments(self):
        self.assertListEqual(Point(1).xyz,[1,0,0])
        self.assertListEqual(Point(1,1).xyz,[1,1,0])
        self.assertListEqual(Point(1,1,1).xyz,[1,1,1])
        
    def testCreatePointWithKeywords(self):
        self.assertListEqual(Point(x=1).xyz,[1,0,0])
        self.assertListEqual(Point(y=1).xyz,[0,1,0])
        self.assertListEqual(Point(z=1).xyz,[0,0,1])
        self.assertListEqual(Point(x=1,y=1).xyz,[1,1,0])
        self.assertListEqual(Point(x=1,z=1).xyz,[1,0,1])
        self.assertListEqual(Point(y=1,z=1).xyz,[0,1,1])
        self.assertListEqual(Point(x=1,y=1,z=1).xyz,[1,1,1])

    def testCreatePointWithArgumentsAndKeywords(self):

        self.assertListEqual(Point(1,x=2).xyz,[2,0,0])
        self.assertListEqual(Point(0,1,y=2).xyz,[0,2,0])
        self.assertListEqual(Point(0,0,1,z=2).xyz,[0,0,2])

        self.assertListEqual(Point(1,x=2,y=1).xyz,[2,1,0])
        self.assertListEqual(Point(0,1,y=2,x=1).xyz,[1,2,0])
        self.assertListEqual(Point(0,1,y=2,z=1).xyz,[0,2,1])
        self.assertListEqual(Point(0,0,1,z=2,x=1).xyz,[1,0,2])
        self.assertListEqual(Point(0,0,1,z=2,y=1).xyz,[0,1,2])
        
        self.assertListEqual(Point(1,x=2,y=1,z=1).xyz,[2,1,1])
        self.assertListEqual(Point(0,1,y=2,x=1,z=1).xyz,[1,2,1])
        self.assertListEqual(Point(0,1,y=2,z=1,x=1).xyz,[1,2,1])
        self.assertListEqual(Point(0,0,1,z=2,x=1,y=1).xyz,[1,1,2])
        self.assertListEqual(Point(0,0,1,z=2,y=1,x=1).xyz,[1,1,2])

        self.assertListEqual(Point(1,x=4,y=5,z=6).xyz,[4,5,6])
        self.assertListEqual(Point(1,2,x=4,y=5,z=6).xyz,[4,5,6])
        self.assertListEqual(Point(1,2,3,x=4,y=5,z=6).xyz,[4,5,6])
        

    def testCreatePointWithObjects(self):
        for n in range(1,3):
            l = [1]*n
            r = [1]*n + [0]*(3-n)
            self.assertListEqual(Point(l).xyz,r)

        self.assertListEqual(Point(**OnesDict).xyz,OnesList)
        self.assertListEqual(Point(OnesPoint).xyz,OnesList)
        self.assertListEqual(Point(OnesObject).xyz,OnesList)

        with self.assertRaises(UngrokkableObject):
            Point(Ungrokkable())

class PointAttributeSettersTestCase(unittest.TestCase):
    
    def testXYZSetter(self):
        p = Point(1,1,1)
        self.assertListEqual(p.xyz,[1]*3)
                             
        p.xyz = None
        self.assertListEqual(p.xyz,[0]*3,'p.xyz = None')
        
        for thing in [ OnesList, OnesDict, OnesPoint, OnesObject ]:
            msg = 'p.xyz = {t}({o})'.format(o=thing,t=thing.__class__.__name__)
            p = Point()
            p.xyz = thing
            self.assertListEqual(p.xyz,[1]*3,msg)

        with self.assertRaises(UngrokkableObject):
            p = Point()
            p.xyz = Ungrokkable()

        for value,result in [(1,[1,0,0]),((1,2),[1,2,0]),((1,2,3),[1,2,3])]:
            p = Point()
            p.xyz = value
            self.assertListEqual(p.xyz,result,'p.xyz = {v}'.format(v=value))

        for key in 'xyz':
            p = Point()
            d = {key:1}
            p.xyz = d
            self.assertEqual(getattr(p,key),1,
                             "p.{k} = dict('{k}':1)".format(k=key))

    def testXYSetter(self):

        p = Point(1,1,1)
        self.assertListEqual(p.xyz,[1]*3)
                             
        p.xy = None
        self.assertListEqual(p.xyz,[0,0,1],'p.xy = None')
        
        for thing in [ OnesList, OnesDict, OnesPoint, OnesObject]:
            msg = 'p.xy = {t}({o})'.format(o=thing,t=thing.__class__.__name__)
            p = Point()
            p.xy = thing
            self.assertListEqual(p.xyz,[1,1,0],msg)

        with self.assertRaises(UngrokkableObject):
            p = Point()
            p.xy = Ungrokkable()

        for value,result in [(1,[1,0,0]),((1,2),[1,2,0])]:
            p = Point()
            p.xy = value
            self.assertListEqual(p.xyz,result,'p.xyz = {v}'.format(v=value))

        for key in 'xyz':
            p = Point()
            p.xy = {key:1}
            value = getattr(p,key)
            expected = int(key != 'z')
            self.assertEqual(value,expected,"p.{k} = dict('{k}':1)".format(k=key))

    def testYZSetter(self):

        p = Point(1,1,1)
        self.assertListEqual(p.xyz,[1,1,1])
                             
        p.yz = None
        self.assertListEqual(p.xyz,[1,0,0],'p.yz = None')
        
        for thing in [ OnesList, OnesDict, OnesPoint, OnesObject]:
            msg = 'p.yz = {t}({o})'.format(o=thing,t=thing.__class__.__name__)
            p = Point()
            p.yz = thing
            self.assertListEqual(p.xyz,[0,1,1],msg)

        for value,result in [(1,[0,1,0]),((1,2),[0,1,2])]:
            p = Point()
            p.yz = value
            self.assertListEqual(p.xyz,result,'p.xyz = {v}'.format(v=value))

        with self.assertRaises(UngrokkableObject):
            p = Point()
            p.yz = Ungrokkable()

        for key in 'xyz':
            p = Point()
            p.yz = {key:1}
            value = getattr(p,key)
            expected = int(key != 'x')
            self.assertEqual(value,expected,"p.{k} = dict('{k}':1)".format(k=key))

    def testXZSetter(self):

        p = Point(1,1,1)
        self.assertListEqual(p.xyz,[1,1,1])
                             
        p.xz = None
        self.assertListEqual(p.xyz,[0,1,0],'p.xz = None')
        
        for thing in [ OnesList, OnesDict, OnesPoint, OnesObject]:
            msg = 'p.xz = {t}({o})'.format(o=thing,t=thing.__class__.__name__)
            p = Point()
            p.xz = thing
            self.assertListEqual(p.xyz,[1,0,1],msg)

        with self.assertRaises(UngrokkableObject):
            p = Point()
            p.xz = Ungrokkable()            

        for value,result in [(1,[1,0,0]),((1,2),[1,0,2])]:
            p = Point()
            p.xz = value
            self.assertListEqual(p.xyz,result,'p.xyz = {v}'.format(v=value))

        for key in 'xyz':
            p = Point()
            p.xz = {key:1}
            value = getattr(p,key)
            expected = int(key != 'y')
            self.assertEqual(value,expected,"p.{k} = dict('{k}':1)".format(k=key))

class PointAttributeTypesTestCase(unittest.TestCase):
    
    def testPointCoordinateTypesForFloat(self):
        p = Point()
        self.assertIsInstance(p.x,float)
        self.assertIsInstance(p.y,float)
        self.assertIsInstance(p.z,float)

        p.xyz = None
        self.assertIsInstance(p.x,float)
        self.assertIsInstance(p.y,float)
        self.assertIsInstance(p.z,float)

        p.xyz = ZerosList
        self.assertIsInstance(p.x,float)
        self.assertIsInstance(p.y,float)
        self.assertIsInstance(p.z,float)

        p.xyz = ZerosObject
        self.assertIsInstance(p.x,float)
        self.assertIsInstance(p.y,float)
        self.assertIsInstance(p.z,float)

        p.xyz = ZerosPoint
        self.assertIsInstance(p.x,float)
        self.assertIsInstance(p.y,float)
        self.assertIsInstance(p.z,float)
        
        
class PointOperationsTestCase(unittest.TestCase):
    
    def testPointAddition(self):

        p = Point()
        q = Point(1,1,1)

        r = p + p
        self.assertListEqual(r.xyz,[0]*3)

        r = p + q
        self.assertListEqual(r.xyz,[1]*3)

        r = q + q
        self.assertListEqual(r.xyz,[2]*3)

        r = q + 1
        self.assertListEqual(r.xyz,[2]*3)

        r += 1
        self.assertListEqual(r.xyz,[3]*3)

    def testPointSubtraction(self):
        
        p = Point()
        q = Point(1,1,1)

        r = p - q
        self.assertListEqual(r.xyz,[-1]*3)

        r = q - p
        self.assertListEqual(r.xyz,[1]*3)

        r = q - 1
        self.assertListEqual(r.xyz,[0]*3)

        r -= 1
        
        self.assertListEqual(r.xyz,[-1]*3)

    def testPointMultiplication(self):

        p = Point()
        q = Point(1,1,1)

        r = p * p
        self.assertListEqual(r.xyz,[0]*3)

        r = p * q
        self.assertListEqual(r.xyz,[0]*3)

        r = q * q
        self.assertListEqual(r.xyz,[1]*3)

        r = p * 1
        self.assertListEqual(r.xyz,[0]*3)

        r = q * 1
        self.assertListEqual(r.xyz,[1]*3)

        r *= 1
        self.assertListEqual(r.xyz,[1]*3)

        r *= 0
        self.assertListEqual(r.xyz,[0]*3)        
        

    def testPointTrueDivision(self):

        n = 2.
        m = 3.
        
        p = Point([n]*3)
        q = Point([m]*3)

        r = q / p
        self.assertListEqual(r.xyz,[m/n]*3)

        r = p / p
        self.assertListEqual(r.xyz,[1]*3) 

        r = p / q
        self.assertListEqual(r.xyz,[n/m]*3)

        r = p / OnesObject
        self.assertListEqual(r.xyz,[n]*3)

        r = p / 2
        self.assertListEqual(r.xyz,[1]*3)

        r = p / 1
        self.assertListEqual(r.xyz,[n]*3)

        r /= 1
        self.assertListEqual(r.xyz,[n]*3)

        r /= n
        self.assertListEqual(r.xyz,[n/n]*3)

        with self.assertRaises(ZeroDivisionError):
            p = Point(1,1,1)
            q = Point()
            r = p / q

        with self.assertRaises(ZeroDivisionError):
            p = Point(1,1,1)
            r = q / 0

        with self.assertRaises(ZeroDivisionError):
            p = Point(1,1,1)
            r = q / ZerosObject            

        with self.assertRaises(ZeroDivisionError):
            p = Point(1,1,1)
            q = Point()
            p /= q

        with self.assertRaises(ZeroDivisionError):
            p = Point(1,1,1)
            q = Point()
            p /= 0            

    def testPointFloorDivision(self):

        n = 2.
        m = 3.
        
        p = Point([n]*3)
        q = Point([m]*3)

        r = p // p
        self.assertListEqual(r.xyz,[1]*3)

        r = q // p
        self.assertListEqual(r.xyz,[m//n]*3)

        r = p // q
        self.assertListEqual(r.xyz,[n//m]*3)

        r = p // OnesObject
        self.assertListEqual(r.xyz,[n//1]*3)

        r = p // n
        self.assertListEqual(r.xyz,[n//n]*3)

        r = p // 1
        self.assertListEqual(r.xyz,[n]*3)

        r //= n
        self.assertListEqual(r.xyz,[1]*3)

        with self.assertRaises(ZeroDivisionError):
            r = p // ZerosPoint

        with self.assertRaises(ZeroDivisionError):
            r = p // 0

        with self.assertRaises(ZeroDivisionError):
            p = Point(1,1,1)
            p //= 0

    def testPointModulus(self):

        p = Point([2]*3)
        q = Point([4]*3)

        r = p % p
        self.assertListEqual(r.xyz,[0]*3)
        
        r = p % q
        self.assertListEqual(r.xyz,[2]*3)
        
        r = q % p
        self.assertListEqual(r.xyz,[0]*3)

        with self.assertRaises(ZeroDivisionError):
            z = Point()
            r = p % z

        with self.assertRaises(ZeroDivisionError):
            r = p % ZerosObject

        with self.assertRaises(ZeroDivisionError):
            r = p % 0

        with self.assertRaises(ZeroDivisionError):
            p = Point(1,1,1)
            p %= 0     

        r = q % 3
        self.assertListEqual(r.xyz,[1]*3)
        
        r %= 2
        self.assertListEqual(r.xyz,[1]*3)


    def testPointPow(self):

        p = Point()
        q = Point(2,2,2)

        r = p ** p
        self.assertListEqual(r.xyz,[1]*3)

        r = q ** p
        self.assertListEqual(r.xyz,[1]*3)

        r = p ** q
        self.assertListEqual(r.xyz,[0]*3)
        
        r = q ** p
        self.assertListEqual(r.xyz,[1]*3)

        r = p ** 0
        self.assertListEqual(r.xyz,[1]*3)

        r = p ** 1
        self.assertListEqual(r.xyz,[0]*3)

        r = q ** 0
        self.assertListEqual(r.xyz,[1]*3)

        r = q ** 1
        self.assertListEqual(r.xyz,[2]*3)

        r **= 2
        self.assertListEqual(r.xyz,[4]*3)

    def testPointMiscOps(self):

        p = Point(1,1,1)
        
        q = -p
        self.assertListEqual(q.xyz,[-1]*3)

        q = +p
        self.assertEqual(p,q)
        self.assertTrue(q is p)

        q = ~p
        self.assertListEqual(q.xyz,[-2]*3)

        q = abs(Point(-1,-1,-1))
        self.assertEqual(p,q)
        
        self.assertEqual(hash(p),hash(q))
        self.assertTrue(p is not q)

        q = Point()
        self.assertNotEqual(p,q)
        self.assertNotEqual(hash(p),hash(q))
        self.assertTrue(p is not q)
        
    def testPointIteration(self):
        
        pts =[1,2,3]
        p = Point(pts)
        
        for n,v in enumerate(p):
            self.assertEqual(p[n],pts[n])

        self.assertEqual(p[3],1)

        with self.assertRaises(IndexError):
            p[4]

        with self.assertRaises(IndexError):
            p[-5]

    def testPointStrings(self):
        p = Point()
        s = str(p)
        self.assertTrue('x=' in s)
        self.assertTrue('y=' in s)
        self.assertTrue('z=' in s)
        
        r = repr(p)
        self.assertTrue(r.startswith(Point.__name__))
        self.assertTrue('x=' in r)
        self.assertTrue('y=' in r)
        self.assertTrue('z=' in r)

    def testPointBytes(self):
        p = Point()
        self.assertIsInstance(p.bytes,bytes)
        self.assertEqual(p.bytes,bytes(repr(p),'utf-8'))

        
class PointInstanceMethodsTestCase(unittest.TestCase):
    
    def testPointCCW(self):
        
        a = Point()
        self.assertListEqual(a.xyz,[0]*3)
        b = Point(1,0)
        self.assertListEqual(b.xyz,[1,0,0])
        c = Point(1,1)
        self.assertListEqual(c.xyz,[1,1,0])
        d = Point(2,2)
        self.assertListEqual(d.xyz,[2,2,0])

        self.assertEqual(a.ccw(b,c),1)
        self.assertEqual(a.ccw(c,d),0)
        self.assertEqual(c.ccw(b,a),-1)

        self.assertTrue(a.isCCW(b,c))
        self.assertFalse(c.isCCW(b,a))

        with self.assertRaises(CollinearPoints):
            a.isCCW(c,d)

        self.assertTrue(a.isCollinear(c,d))
        self.assertFalse(a.isCollinear(b,c))

    def testPointCrossProduct(self):

        i,j,k = Point.units()

        self.assertEqual(i.cross(i),0)
        self.assertEqual(j.cross(j),0)
        self.assertEqual(k.cross(k),0)
        
        self.assertEqual(i.cross(j),1)
        self.assertEqual(i.cross(k),-1)

        self.assertEqual(j.cross(k),1)
        self.assertEqual(j.cross(i),-1)

        self.assertEqual(k.cross(i),1)
        self.assertEqual(k.cross(j),-1)

    def testPointDotProduct(self):
        
        i,j,k = Point.units()

        self.assertEqual(i.dot(i),1)
        self.assertEqual(j.dot(j),1)
        self.assertEqual(k.dot(k),1)

        self.assertEqual(i.dot(j),0)
        self.assertEqual(i.dot(k),0)

        self.assertEqual(j.dot(i),0)
        self.assertEqual(j.dot(k),0)

        self.assertEqual(k.dot(i),0)
        self.assertEqual(k.dot(j),0)

    def testPointDistance(self):

        i,j,k = Point.units()

        self.assertEqual(i.distance(),1)
        self.assertEqual(j.distance(),1)
        self.assertEqual(k.distance(),1)

        self.assertEqual(i.distance(j),j.distance(i))
        self.assertEqual(i.distance(k),k.distance(i))
        self.assertEqual(j.distance(k),k.distance(j))

        self.assertEqual(i.distanceSquared(j),j.distanceSquared(i))
        self.assertEqual(i.distanceSquared(k),k.distanceSquared(i))
        self.assertEqual(j.distanceSquared(k),k.distanceSquared(j))

    def testPointMidpoint(self):
        i,j,k = Point.units()
        m = i.midpoint(j)
        self.assertIsInstance(m,Point)
        self.assertTrue(m.isCollinear(i,j))
        self.assertEqual(m.distance(i),m.distance(j))
        self.assertEqual(i.distance(m),j.distance(m))
        self.assertEqual(m,(i+j)/2)
        
    def testPointBetween(self):
        
        i,j,k = Point.units()
        
        a = (i+j+k) / 2

        self.assertTrue(a.isBetweenX(i,j))
        self.assertTrue(a.isBetweenX(j,i))
        self.assertTrue(a.isBetweenX(i,k))
        self.assertTrue(a.isBetweenX(k,i))
        self.assertFalse(a.isBetweenX(j,k))
        self.assertFalse(a.isBetweenX(k,j))

        self.assertTrue(a.isBetweenY(i,j))
        self.assertTrue(a.isBetweenY(j,i))
        self.assertTrue(a.isBetweenY(j,k))
        self.assertTrue(a.isBetweenY(k,j))
        self.assertFalse(a.isBetweenY(i,k))
        self.assertFalse(a.isBetweenY(k,i))
        
        self.assertTrue(a.isBetweenZ(k,i))
        self.assertTrue(a.isBetweenZ(i,k))
        self.assertTrue(a.isBetweenZ(k,j))
        self.assertTrue(a.isBetweenZ(j,k))
        self.assertFalse(a.isBetweenZ(i,j))
        self.assertFalse(a.isBetweenZ(j,i))

        a = (i+j+k) * 2
        
        self.assertListEqual(a.xyz,[2]*3)

        self.assertFalse(a.isBetweenX(i,j))
        self.assertFalse(a.isBetweenX(j,i))
        self.assertFalse(a.isBetweenX(i,k))
        self.assertFalse(a.isBetweenX(k,i))
        self.assertFalse(a.isBetweenX(j,k))
        self.assertFalse(a.isBetweenX(k,j))

        self.assertFalse(a.isBetweenY(i,j))
        self.assertFalse(a.isBetweenY(j,i))
        self.assertFalse(a.isBetweenY(j,k))
        self.assertFalse(a.isBetweenY(k,j))
        self.assertFalse(a.isBetweenY(i,k))
        self.assertFalse(a.isBetweenY(k,i))
        
        self.assertFalse(a.isBetweenZ(k,i))
        self.assertFalse(a.isBetweenZ(i,k))
        self.assertFalse(a.isBetweenZ(k,j))
        self.assertFalse(a.isBetweenZ(j,k))
        self.assertFalse(a.isBetweenZ(i,j))
        self.assertFalse(a.isBetweenZ(j,i))

class PointClassmethodsTestCase(unittest.TestCase):
    
    def testPointClassmethodGaussian(self):
        
        p = Point.gaussian()
        self.assertIsInstance(p,Point)
        # uh. yup. 

    def testPointClassmethodRandomLocation(self):        
        p = Point.randomLocation()
        self.assertIsInstance(p,Point)
        self.assertLessEqual(p.distance(),1)
        
        p = Point.randomLocation(Point(5,5,0),2)
        self.assertIsInstance(p,Point)
        self.assertLessEqual(p.distance(Point(5,5,0)),2)

    def testPointClassmethodRandomLocationInRectangle(self):
        i,j,_ = Point.units()
        p = Point.randomLocationInRectangle()
        self.assertIsInstance(p,Point)
        self.assertTrue(p.isBetweenX(i,j))
        self.assertTrue(p.isBetweenY(i,j))

        o = Point(2,2)
        p = Point.randomLocationInRectangle(o,2,2)
        self.assertIsInstance(p,Point)
        self.assertTrue(p.isBetweenX(o,o+2))
        self.assertTrue(p.isBetweenY(o,o+2))

    def testPointClassmethodUnits(self):
        i,j,k = Point.units()
        self.assertListEqual(i.xyz,[1,0,0])
        self.assertListEqual(j.xyz,[0,1,0])
        self.assertListEqual(k.xyz,[0,0,1])

    def testPointClassmethodUnitize(self):

        a,b = Point.gaussian(), Point.gaussian()

        c = Point.unitize(a,b)

        self.assertIsInstance(c,Point)
        self.assertAlmostEqual(c.distance(),1.0,delta=sys.float_info.epsilon)

        for u in Point.units():
            r = Point.unitize(Point(),u)
            self.assertListEqual(u.xyz,r.xyz,
                                 'unitize(O,{u}) => {r} != {u}'.format(u=u,r=r))

    
if __name__ == '__main__':
    unittest.main()
            
