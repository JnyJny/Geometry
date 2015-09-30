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

ZerosPoint = Point()
OnesPoint = Point(1,1,1)

class PointInitializationTestCase(unittest.TestCase):
    
    def testOriginPoints(self):
        '''
        '''
        self.assertListEqual(Point().xyz,ZerosList)
        self.assertListEqual(Point(None).xyz,ZerosList)
        self.assertListEqual(Point(()).xyz,ZerosList)
        self.assertListEqual(Point([]).xyz,ZerosList)
        self.assertListEqual(Point({}).xyz,ZerosList)
        self.assertListEqual(Point(Point()).xyz,ZerosList)
        self.assertListEqual(Point(ZerosList).xyz,ZerosList)
        self.assertListEqual(Point(ZerosDict).xyz,ZerosList)
        self.assertListEqual(Point(ZerosObject).xyz,ZerosList)
        
        self.assertListEqual(Point().xyzw,[0,0,0,1])
        self.assertEqual(Point().w,1)

    def testCreatePointWithRegularArguements(self):

        self.assertListEqual(Point(1).xyz,[1,0,0])
        self.assertListEqual(Point(1,1).xyz,[1,1,0])
        self.assertListEqual(Point(1,1,1).xyz,[1,1,1])

    def testCreatePointWithObjects(self):
        for n in range(1,3):
            l = [1]*n + [0]*(3-n)
            self.assertListEqual(Point(l).xyz,l)

        self.assertListEqual(Point(**OnesDict).xyz,OnesList)
        self.assertListEqual(Point(OnesPoint).xyz,OnesList)
        self.assertListEqual(Point(OnesObject).xyz,OnesList)

        with self.assertRaises(UngrokkableObject):
            Point(Ungrokkable())
        

    def testCreatePointWithKeywords(self):
        self.assertListEqual(Point(x=1).xyz,[1,0,0])
        self.assertListEqual(Point(y=1).xyz,[0,1,0])
        self.assertListEqual(Point(z=1).xyz,[0,0,1])

        self.assertListEqual(Point(x=1,y=1).xyz,[1,1,0])
        self.assertListEqual(Point(x=1,z=1).xyz,[1,0,1])
        self.assertListEqual(Point(y=1,z=1).xyz,[0,1,1])
        

    def testXYZSetter(self):
        
        p = Point(1,1,1)
        self.assertListEqual(p.xyz,[1]*3)
                             
        p.xyz = None
        self.assertListEqual(p.xyz,[0]*3,'p.xyz = None')
        
        for thing in [ OnesList, OnesDict, OnesPoint, OnesObject ]:
            msg = 'p.xyz = {t}({o})'.format(o=thing,t=thing.__class__.__name__)
            p = Point()
            self.assertListEqual(p.xyz,[0]*3)
            p.xyz = thing
            self.assertListEqual(p.xyz,[1]*3,msg)

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
            self.assertListEqual(p.xyz,[0]*3)
            p.xy = thing
            self.assertListEqual(p.xyz,[1,1,0],msg)

        for value,result in [(1,[1,0,0]),((1,2),[1,2,0])]:
            p = Point()
            p.xy = value
            self.assertListEqual(p.xyz,result,'p.xyz = {v}'.format(v=value))

        for key in 'xyz':
            p = Point()

            p.xy = {key:1}
            value = getattr(p,key)
            
            expected = 1
            if key == 'z':
                expected = 0
                
            self.assertEqual(value,expected,"p.{k} = dict('{k}':1)".format(k=key))

    def testYZSetter(self):

        p = Point(1,1,1)
        self.assertListEqual(p.xyz,[1,1,1])
                             
        p.yz = None
        self.assertListEqual(p.xyz,[1,0,0],'p.yz = None')
        
        for thing in [ OnesList, OnesDict, OnesPoint, OnesObject]:
            msg = 'p.yz = {t}({o})'.format(o=thing,t=thing.__class__.__name__)
            p = Point()
            self.assertListEqual(p.xyz,[0]*3)
            p.yz = thing
            self.assertListEqual(p.xyz,[0,1,1],msg)

        for value,result in [(1,[0,1,0]),((1,2),[0,1,2])]:
            p = Point()
            p.yz = value
            self.assertListEqual(p.xyz,result,'p.xyz = {v}'.format(v=value))

        for key in 'xyz':
            p = Point()

            p.yz = {key:1}
            value = getattr(p,key)
            
            expected = 1
            if key == 'x':
                expected = 0
                
            self.assertEqual(value,expected,"p.{k} = dict('{k}':1)".format(k=key))

    def testXZSetter(self):

        p = Point(1,1,1)
        self.assertListEqual(p.xyz,[1,1,1])
                             
        p.xz = None
        self.assertListEqual(p.xyz,[0,1,0],'p.xz = None')
        
        for thing in [ OnesList, OnesDict, OnesPoint, OnesObject]:
            msg = 'p.xz = {t}({o})'.format(o=thing,t=thing.__class__.__name__)
            p = Point()
            self.assertListEqual(p.xyz,[0]*3)
            p.xz = thing
            self.assertListEqual(p.xyz,[1,0,1],msg)

        for value,result in [(1,[1,0,0]),((1,2),[1,0,2])]:
            p = Point()
            p.xz = value
            self.assertListEqual(p.xyz,result,'p.xyz = {v}'.format(v=value))

        for key in 'xyz':
            p = Point()

            p.xz = {key:1}
            value = getattr(p,key)
            
            expected = 1
            if key == 'y':
                expected = 0
                
            self.assertEqual(value,expected,"p.{k} = dict('{k}':1)".format(k=key))            
    def testPointAddition(self):

        p = Point()
        self.assertListEqual(p.xyz,[0]*3)

        q = Point([1]*3)
        self.assertListEqual(q.xyz,[1]*3)

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
        self.assertListEqual(p.xyz,[0]*3)
        
        q = Point(1,1,1)
        self.assertListEqual(q.xyz,[1]*3)

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
        self.assertListEqual(p.xyz,[0]*3)
        
        q = Point(1,1,1)
        self.assertListEqual(q.xyz,[1]*3)

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
        # XXX needs to check for zero division
        n = 2.
        m = 3.
        
        p = Point([n]*3)
        self.assertListEqual(p.xyz,[n]*3)
        
        q = Point([m]*3)
        self.assertListEqual(q.xyz,[m]*3)

        r = q / p
        self.assertListEqual(r.xyz,[m/n]*3)

        r = p / p
        self.assertListEqual(r.xyz,[1]*3) 

        r = p / q
        self.assertListEqual(r.xyz,[n/m]*3)

        r = p / 2
        self.assertListEqual(r.xyz,[1]*3)

        r = p / 1
        self.assertListEqual(r.xyz,[n]*3)

        r /= 1
        self.assertListEqual(r.xyz,[n]*3)

        r /= n
        self.assertListEqual(r.xyz,[n/n]*3)
        

    def testPointFloorDivision(self):
        # XXX needs to check for zero division
        n = 2.
        m = 3.
        
        p = Point([n]*3)
        self.assertListEqual(p.xyz,[n]*3)
        
        q = Point([m]*3)
        self.assertListEqual(q.xyz,[m]*3)

        r = p // p
        self.assertListEqual(r.xyz,[1]*3)

        r = q // p
        self.assertListEqual(r.xyz,[m//n]*3)

        r = p // q
        self.assertListEqual(r.xyz,[n//m]*3)

        r = p // n
        self.assertListEqual(r.xyz,[n//n]*3)

        r = p // 1
        self.assertListEqual(r.xyz,[n]*3)

        r //= n
        self.assertListEqual(r.xyz,[1]*3)


    def testPointModulus(self):
        # XXX needs to check for zero division
        p = Point([2]*3)
        self.assertListEqual(p.xyz,[2]*3)
        
        q = Point([4]*3)
        self.assertListEqual(q.xyz,[4]*3)

        r = p % p
        self.assertListEqual(r.xyz,[0]*3)
        
        r = p % q
        self.assertListEqual(r.xyz,[2]*3)
        
        r = q % p
        self.assertListEqual(r.xyz,[0]*3)

        r = q % 3
        self.assertListEqual(r.xyz,[1]*3)
        
        r %= 2
        self.assertListEqual(r.xyz,[1]*3)


    def testPointPow(self):

        p = Point()
        self.assertListEqual(p.xyz,[0]*3)
        
        q = Point(2,2,2)
        self.assertListEqual(q.xyz,[2]*3)

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
        self.assertListEqual(p.xyz,[1]*3)
        
        q = -p
        self.assertListEqual(q.xyz,[-1]*3)

        q = ~p
        self.assertListEqual(q.xyz,[-2]*3)

        q = Point(1,1,1)
        
        self.assertEqual(p,q)

        q = Point()

        self.assertNotEqual(p,q)

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
        self.assertListEqual(i.xyz,[1,0,0])
        self.assertListEqual(j.xyz,[0,1,0])
        self.assertListEqual(k.xyz,[0,0,1])

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
        i = Point(1,0,0)
        self.assertListEqual(i.xyz,[1,0,0])
        j = Point(0,1,0)
        self.assertListEqual(j.xyz,[0,1,0])
        k = Point(0,0,1)
        self.assertListEqual(k.xyz,[0,0,1])


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

        self.assertListEqual(i.xyz,[1,0,0])
        self.assertListEqual(j.xyz,[0,1,0])
        self.assertListEqual(k.xyz,[0,0,1])

        self.assertEqual(i.distance(j),j.distance(i))
        self.assertEqual(i.distance(k),k.distance(i))
        self.assertEqual(j.distance(k),k.distance(j))

        self.assertEqual(i.distanceSquared(j),j.distanceSquared(i))
        self.assertEqual(i.distanceSquared(k),k.distanceSquared(i))
        self.assertEqual(j.distanceSquared(k),k.distanceSquared(j))

    def testPointBetween(self):
        pass

    def testPointClassmethods(self):
        pass
                
        
    
if __name__ == '__main__':
    unittest.main()
            
