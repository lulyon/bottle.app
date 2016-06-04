# -*- coding: utf-8 -*-
#
# unittest example

def setUp():
    print "function setup"

def tearDown():
    print "function teardown"

def func1Start():
    print "func1 start"

def func1End():
    print "func1 end"

def func2Start():
    print "func2 start"

def func2End():
    print "func2 end"

def Testfunc1():
    print "Testfunc1"
    assert True

def Testfunc2():
    print "Testfunc2"
    assert True

Testfunc1.setup = func1Start
Testfunc1.tearDown = func1End
Testfunc2.setup = func2Start
Testfunc2.tearDown = func2End


class TestClass():
    arr1 = 2
    arr2 = 2

    def setUp(self):
        self.arr1 = 1 +1
        self.arr2 = 3 -1
        print "MyTestClass setup"

    def tearDown(self):
        print "MyTestClass teardown"

    def Testfunc1(self):
        assert self.arr1 == self.arr2

    def Testfunc2(self):
        assert self.arr1 == 2
