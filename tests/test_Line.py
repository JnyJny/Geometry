#!/usr/bin/env python3

import unittest
import sys
sys.path.append('..')

from Geometry import *

class LineInitializationTestCase(unittest.TestCase):

    def testLineInitializationWithNoArguments(self):
        l = Line()
        # Line([0,0,0],[1,1,0])
        self.assertListEqual(l.A.xyz,[0]*3)
        self.assertListEqual(l.B.xyz,[0]*3)

    def testLineInitializaitonWithOneArgument(self):

        l = Line(Point([2]*3))
        self.assertListEqual(l.A.xyz,[2]*3)
        self.assertListEqual(l.B.xyz,[0]*3)

        l = Line(A=Point([2]*3))
        self.assertListEqual(l.A.xyz,[2]*3)
        self.assertListEqual(l.B.xyz,[0]*3)

        with self.assertRaises(UngrokkableObject):
            l = Line(A=self)

        l = Line(B=Point([2]*3))
        self.assertListEqual(l.A.xyz,[0]*3)
        self.assertListEqual(l.B.xyz,[2]*3)

        with self.assertRaises(UngrokkableObject):
            l = Line(B=self)

    def testLineInitializationWithTwoArguments(self):

        l = Line(A=Point(1,2,3),B=Point(4,5,6))
        self.assertListEqual(l.A.xyz,[1,2,3])
        self.assertListEqual(l.B.xyz,[4,5,6])

        with self.assertRaises(UngrokkableObject):
            l = Line(A=self,B=self)

    def testLineAGetter(self):
        l = Line(A=[1,2,3])

        self.assertListEqual(l.A.xyz,[1,2,3])
        self.assertListEqual(l[0].xyz,[1,2,3])

    def testLineASeter(self):
        l = Line()
        l.A = Point(1,1,1)
        self.assertListEqual(l.A.xyz,[1]*3)


    def testLineAGetter(self):
        l = Line(A=[1,2,3])
        self.assertListEqual(l.A.xyz,[1,2,3])
        self.assertListEqual(l[0].xyz,[1,2,3])

    def testLineASetter(self):
        l = Line()
        l.A = Point(1,1,1)
        self.assertListEqual(l.A.xyz,[1]*3)


    def testLineBGetter(self):
        l = Line(B=[1,2,3])
        self.assertListEqual(l.B.xyz,[1,2,3])
        self.assertListEqual(l[1].xyz,[1,2,3])

    def testLineBSetter(self):
        l = Line()
        l.B = Point(1,1,1)
        self.assertListEqual(l.B.xyz,[1]*3)
                             

    def testLineABGetter(self):

        l = Line([1,2,3],[4,5,6])
        A,B = l.AB
        self.assertListEqual(A.xyz,[1,2,3])
        self.assertListEqual(B.xyz,[4,5,6])

    def testLineABSetter(self):        
        
        l = Line()
        
        l.A = [4,5,6]
        l.B = [1,2,3]
        self.assertListEqual(l.A.xyz,[4,5,6])
        self.assertListEqual(l.B.xyz,[1,2,3])

        l = Line()
        l.AB = [1,2,3],[4,5,6]
        self.assertListEqual(l.A.xyz,[1,2,3])
        self.assertListEqual(l.B.xyz,[4,5,6])

        l.AB = None
        self.assertListEqual(l.A.xyz,[0,0,0])
        self.assertListEqual(l.B.xyz,[0,0,0])

        l.AB = [1,1,1]
        self.assertListEqual(l.A.xyz,[1,1,1])
        self.assertListEqual(l.B.xyz,[0,0,0])
        

if __name__ == '__main__':
    unittest.main()
