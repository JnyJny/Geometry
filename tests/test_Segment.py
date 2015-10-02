#!/usr/bin/env python3

import unittest
import sys
import math

sys.path.append('..')

from Geometry import Line, Segment, Ray, Point
from Geometry.exceptions import *

class SegmentInitializationTestCase(unittest.TestCase):

    def testSegmentInitializationWithNoArguments(self):
        s = Segment()
        # Segment([0,0,0],[1,1,0])
        self.assertListEqual(s.A.xyz,[0]*3)
        self.assertListEqual(s.B.xyz,[0]*3)

    def testSegmentInitializaitonWithOneArgument(self):

        s = Segment(Point([2]*3))
        self.assertListEqual(s.A.xyz,[2]*3)
        self.assertListEqual(s.B.xyz,[0]*3)

        s = Segment(A=Point([2]*3))
        self.assertListEqual(s.A.xyz,[2]*3)
        self.assertListEqual(s.B.xyz,[0]*3)

        with self.assertRaises(UngrokkableObject):
            s = Segment(A=self)

        s = Segment(B=Point([2]*3))
        self.assertListEqual(s.A.xyz,[0]*3)
        self.assertListEqual(s.B.xyz,[2]*3)

        with self.assertRaises(UngrokkableObject):
            s = Segment(B=self)

    def testSegmentInitializationWithTwoArguments(self):

        s = Segment(A=Point(1,2,3),B=Point(4,5,6))
        self.assertListEqual(s.A.xyz,[1,2,3])
        self.assertListEqual(s.B.xyz,[4,5,6])

        with self.assertRaises(UngrokkableObject):
            s = Segment(A=self,B=self)

    def testSegmentAGetter(self):
        s = Segment(A=[1,2,3])
        self.assertListEqual(s.A.xyz,[1,2,3])

    def testSegmentASetter(self):
        s = Segment()
        s.A = Point(1,1,1)
        self.assertListEqual(s.A.xyz,[1]*3)

    def testSegmentBGetter(self):
        s = Segment(B=[1,2,3])
        self.assertListEqual(s.B.xyz,[1,2,3])

    def testSegmentBSetter(self):
        s = Segment()
        s.B = Point(1,1,1)
        self.assertListEqual(s.B.xyz,[1]*3)
                             

    def testSegmentABGetter(self):
        s = Segment([1,2,3],[4,5,6])
        A,B = s.AB
        self.assertListEqual(A.xyz,[1,2,3])
        self.assertListEqual(B.xyz,[4,5,6])

    def testSegmentABSetter(self):        
        s = Segment()
        s.AB = [1,2,3],[4,5,6]
        self.assertListEqual(s.A.xyz,[1,2,3])
        self.assertListEqual(s.B.xyz,[4,5,6])
        s.AB = None
        self.assertListEqual(s.A.xyz,[0,0,0])
        self.assertListEqual(s.B.xyz,[0,0,0])
        s.AB = [1,1,1]
        self.assertListEqual(s.A.xyz,[1,1,1])
        self.assertListEqual(s.B.xyz,[0,0,0])


class SegmentClassmethodTestCase(unittest.TestCase):

    def testSegmentConversionFromLineWithMissingArgument(self):
        with self.assertRaises(TypeError):
            s = Segment.fromSegment()

    def testSegmentConversionFromLineWithGoodLine(self):
        l = Line([1,2,3],[4,5,6])
        s = Segment.fromLine(l)
        
        self.assertFalse(s is l)
        self.assertIsInstance(l,Line)
        self.assertIsInstance(s,Segment)
        self.assertListEqual(s.A.xyz,l.A.xyz)
        self.assertListEqual(s.B.xyz,l.B.xyz)

    def testSegmentConversionFromRayWithMissingArgument(self):
        with self.assertRaises(TypeError):
            s = Segment.fromRay()

    def testSegmentConversionFromRayWithGoodRay(self):
        r = Ray([1,2,3],[4,5,6])
        s = Segment.fromRay(r)
        
        self.assertFalse(r is s)
        self.assertIsInstance(r,Ray)
        self.assertIsInstance(s,Segment)
        self.assertListEqual(s.A.xyz,r.A.xyz)
        self.assertListEqual(s.B.xyz,r.B.xyz)

class SegmentPropertiesTestCase(unittest.TestCase):

    def testSegmentPropertySlopeParameterM(self):
        s = Segment(Point(),Point(1,1,1))
        
        self.assertListEqual(s.m.xyz,[1,1,1])

    def testSegmentPropertyMapping(self):
        s = Segment()
        
        m = s.mapping
        
        self.assertIsInstance(m,dict)
        for key in Segment.vertexNames:
            self.assertEqual(getattr(s,key),m[key])

    def testSegmentPropertyLength(self):
        i,j,k = Point.units()
        
        s = Segment(B=i)
        t = Segment(B=j)
        u = Segment(B=k)

        self.assertEqual(s.length,1)
        self.assertEqual(t.length,1)
        self.assertEqual(u.length,1)
        
    def testSegmentPropertyNormal(self):
        i,j,_ = Point.units()
        s = Segment(B=i)
        self.assertListEqual(s.normal.A.xyz,j.xyz)


class SegmentInstanceMethodsTestCase(unittest.TestCase):

    def testSegmentInstanceMethodPointAt(self):
        s = Segment(B=[1,0,0])
        self.assertListEqual(s.pointAt(0).xyz,s.A.xyz)
        self.assertListEqual(s.pointAt(1).xyz,s.B.xyz)
        self.assertListEqual(s.pointAt(0.5).xyz,[0.5,0,0])

    def testSegmentStringMethods(self):


        s = str(Segment(Point.gaussian(),Point.gaussian()))
        self.assertEqual(s.count('A='),1)
        self.assertEqual(s.count('B='),1)
        self.assertEqual(s.count('x='),2)
        self.assertEqual(s.count('y='),2)
        self.assertEqual(s.count('z='),2)        
        
        r = repr(Segment(Point.gaussian(),Point.gaussian()))
        self.assertTrue(r.startswith(Segment.__name__))
        self.assertEqual(s.count('A='),1)
        self.assertEqual(s.count('B='),1)
        self.assertEqual(s.count('x='),2)
        self.assertEqual(s.count('y='),2)
        self.assertEqual(s.count('z='),2)

    def testSegmentIteratorMethods(self):
        s = Segment([1,2,3],[4,5,6])
        
        self.assertEqual(len(s),2)
        self.assertListEqual(s[0].xyz,[1,2,3])
        self.assertListEqual(s[1].xyz,[4,5,6])
        self.assertListEqual(s[-2].xyz,[1,2,3])
        self.assertListEqual(s[-1].xyz,[4,5,6])
        with self.assertRaises(IndexError):
            s[2]
        with self.assertRaises(IndexError):
            s[-3]

    def testSegmentInstaceMethodContains(self):
        s = Segment(B=[1,0,0])
        p = Point(.5)
        q = Point(y=.5)
        self.assertTrue(p in s)
        self.assertFalse(q in s)

    def testSegmentInstanceMethodFlip(self):
        s = Segment(B=[1,1,1])
        s.flip()
        self.assertListEqual(s.A.xyz,[1,1,1])
        self.assertListEqual(s.B.xyz,[0,0,0])

    def testSegmentInstanceMethodDoesIntersect(self):
        i,j,_ = Point.units()
        s = Segment(B=i)
        t = Segment(B=j)
        o = Segment([0,1,0],[1,1,0])

        self.assertTrue(s.doesIntersect(s))
        self.assertTrue(s.doesIntersect(t))
        self.assertFalse(s.doesIntersect(o))
        
    def testSegmentInstanceMethodIntersection(self):
        i,j,_ = Point.units()
        s = Segment(B=i)
        t = Segment(B=j)
        self.assertListEqual(s.intersection(t).xyz,[0,0,0])

    def testSegmentInstanceMethodDistanceFromPoint(self):
        i,j,_ = Point.units()

        s = Segment(B=i)
        self.assertEqual(s.distanceFromPoint(j),1)
        self.assertEqual(s.distanceFromPoint(i),0)

    def testSegmentInstanceMethodIsNormal(self):
        i,j,_ = Point.units()

        s = Segment(B=i)
        t = Segment(B=j)

        self.assertTrue(s.isNormal(t))


    def testSegmentInstanceMethodRadiansBetween(self):
        i,j,_ = Point.units()

        s = Segment(B=i)
        t = Segment(B=j)

        self.assertEqual(s.radiansBetween(t),math.pi/2)
        self.assertEqual(s.radiansBetween(s),0)
        

    def testSegmentInstanceMethodDegreesBetween(self):
        i,j,_ = Point.units()

        s = Segment(B=i)
        t = Segment(B=j)

        self.assertEqual(s.degreesBetween(t),90)
        self.assertEqual(s.degreesBetween(s),0)
    

        
if __name__ == '__main__':
    unittest.main()
