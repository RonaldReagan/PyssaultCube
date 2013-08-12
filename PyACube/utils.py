# -*- coding: utf-8 -*-
# <$licence>
#Written by JPablon
#Used with permission.


"""Misc functions.
"""


import math


def enum(*sequential, **n):
    """
    """
    return type('Enum', (), dict(zip(sequential, range(len(sequential))), **n))


def millis2time(millis):
    """
    """
    return divmod(millis / 1000, 60)


def time2millis(time):
    """
    """
    return ((time[0] * 60) + time[1]) * 1000


def filtertext(text):
    """
    """
    for i in range(len(text)):
        if text[i] == chr(0x0c):
            return text[:i] + filtertext(text[i + 2:])
    return text


def angleDiff(degree1, degree2):
    """
    """
    r = (degree1 - degree2) % 360
    if r > 180:
        return -(360 - r)
    return r


def out(text):
    """
    """
    output = filtertext(text)
    print(output)


class Vector(object):
    """3 point vector.
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """
        """
        self.__v = [x, y, z]
        self.__k = dict({'x': 0, 'y': 1, 'z': 2})

    #
    # Class interface

    def getAsList(self):
        """
        """
        return self.__v

    def add(self, vector):
        """
        """
        vlist = vector.getAsList()
        for i in range(3):
            self.__v[i] = self.__v[i] + vlist[i]

    def sub(self, vector):
        """
        """
        vlist = vector.getAsList()
        for i in range(3):
            self.__v[i] = self.__v[i] - vlist[i]

    def mul(self, vector):
        """
        """
        vlist = vector.getAsList()
        for i in range(3):
            self.__v[i] = self.__v[i] * vlist[i]

    def div(self, vector):
        """
        """
        vlist = vector.getAsList()
        for i in range(3):
            self.__v[i] = self.__v[i] / vlist[i]

    def getDistance(self, v2):
        """
        """
        tmp = Vector(self.x, self.y, self.z)
        tmp.sub(v2)
        return math.sqrt(tmp.x ** 2 + tmp.y ** 2 + tmp.z ** 2)

    def getFlatDistance(self, v2):
        """
        """
        tmp = Vector(self.x, self.y, 0)
        tmp.sub(v2)
        return math.sqrt(tmp.x ** 2 + tmp.y ** 2)

    #
    # Internal functions

    def __getattr__(self, name):
        if '_Vector__k' in self.__dict__ and name in self.__k:
            return self.__dict__['_Vector__v'][self.__k[name]]
        return object.__getattr__(self, name)

    def __setattr__(self, name, value):
        if '_Vector__k' in self.__dict__ and name in self.__k:
            self.__dict__['_Vector__v'][self.__k[name]] = value
            return
        object.__setattr__(self, name, value)


class switch(object):
    """This class provides the functionality we want. You only need to look at
    this if you want to know how this works. It only needs to be defined
    once, no need to muck around with its internals.
    http://code.activestate.com/recipes/410692/
    """
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop
        """
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite
        """
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False