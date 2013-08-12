# -*- coding: utf-8 -*-
# <$licence>
#Written by JPablon
#Used with permission.


"""
    Implementation of some usefull buffers related to the cube engine.
"""


import struct
import array

class ByteBuffer(object):
    """Basic byte buffer class.
    """

    def __init__(self, raw=''):
        """If a str is passed as argument the buffer will be created in read
        only mode.
        """
        self.__b = array.array('B')
        self.__b.fromstring(raw)
        self.__c = 0
        self.__readonly = bool(raw)

    def subBuffer(self, n):
        """Retrieves an PacketBuffer object containing a sub  buffer starting
        at this buffer current position and ending at n.
        """
        self.check(n)
        r = PacketBuffer(self.__b[self.__c:self.__c + n])
        self.__c += n
        return r

    def getRawStr(self, n):
        """Same as above but it returns a string.
        """
        self.check(n)
        r = self.__b[self.__c:self.__c + n]
        self.__c += n
        return r.tostring()

    def setCursor(self, position):
        """Sets this buffer's position.
        """
        if position >= 0 and position < len(self.__b):
            self.__c = position
        return self.__c

    def getCursor(self):
        """Returns this buffer's position.
        """
        return self.__c

    def getRemaining(self):
        """
        """
        return len(self.__b) - self.__c

    def getRawBuffer(self):
        """Returns the raw buffer string.
        """
        return self.__b.tostring()

    def getArrayInstance(self):
        """
        """
        return self.__b

    def isWritable(self):
        """Return true if the current buffer is writable.
        """
        return not self.__readonly

    def check(self, n=1):
        """
        """
        if self.__c + n > len(self.__b):
            raise BufferError("Buffer overread.")

    def get(self):
        """
        """
        self.check()
        r = self.__b[self.__c]
        self.__c += 1
        return r

    def put(self, value):
        """
        """
        if self.__readonly:
            raise BufferError("You cant write on this buffer.")
        self.__b.append(value & 0xFF)


def bsigned(n):
    if n >= 128:
        return - (0x100 + (~ n + 1))
    return n


class PacketBuffer(ByteBuffer):
    """Taken from protocol.cpp

    All network traffic is in 32bit ints, which are then compressed using the
    following simple scheme (assumes that most values are small).

    All values written are attached at the end of the buffer, put operations
    dont increase the buffer position, if the buffer is writable the cursor
    position is only used to read.
    """

    def __init__(self, raw=''):
        """If a str is passed as argument the buffer will be created in read
        only mode.
        """
        ByteBuffer.__init__(self, raw)

    def getInt(self):
        """
        """
        n = bsigned(self.get())
        if n == -0x80:
            n = self.get() | (bsigned(self.get()) << 8)
            return n
        if n == -0x7F:
            n = (self.get() |
                (self.get() << 8) |
                (self.get() << 16) |
                (bsigned(self.get()) << 24))
            return n
        return n

    def getUint(self):
        """
        """
        n = self.get()
        if (n & 0x80) > 0:
            n += (self.get() << 7) - 0x80
            if n & (1 << 14):
                n += (self.get() << 14) - (1 << 14)
            if n & (1 << 21):
                n += (self.get() << 21) - (1 << 21)
            if n & (1 << 28):
                n = n | 0xF0000000
        return n

    def getFloat(self):
        """
        """
        s = self.getRawStr(4)
        n = struct.unpack('<f', s)[0]
        return n

    def getStr(self):
        """
        """
        s = []
        if self.getRemaining() <= 0:
            return str()
        for i in range(self.getRemaining()):
            char = self.get()
            if not char:
                break
            s.append(chr(char))
        return str().join(s)

    def putInt(self, n):
        """
        """
        if n < 0x8000 and n >= -0x8000:
            if n < 0x80 and n > -0x7F:
                self.put(n)
                return
            self.put(0x80)
            self.put(n)
            self.put(n >> 8)
        else:
            self.put(0x81)
            self.put(n)
            self.put(n >> 8)
            self.put(n >> 16)
            self.put(n >> 24)

    def putUint(self, n):
        """
        """
        if n < 0 or n >= (1 << 21):
            self.put(0x80 | (n & 0x7F))
            self.put(0x80 | ((n >> 7) & 0x7F))
            self.put(0x80 | ((n >> 14) & 0x7F))
            self.put(n >> 21)
        elif n < (1 << 7):
            self.put(n)
        elif n < (1 << 14):
            self.put(0x80 | (n & 0x7F))
            self.put(n >> 7)
        else:
            self.put(0x80 | (n & 0x7F))
            self.put(0x80 | ((n >> 7) & 0x7F))
            self.put(n >> 14)

    def putFloat(self, n):
        """
        """
        s = struct.pack('<f', n)
        self.putBuffer(s)

    def putBuffer(self, s):
        """
        """
        for c in s:
            self.put(ord(c))

    def putStr(self, s):
        """
        """
        self.putBuffer(s)
        self.put(0)


class BitBuffer(ByteBuffer):
    """
    """

    def __init__(self, raw=''):
        """If a str is passed as argument the buffer will be created in read
        only mode.
        """
        ByteBuffer.__init__(self, raw)
        self.__b = self.getArrayInstance()
        self.__p = 0  # remaining bits
        self.__byte = None

    def getBits(self, size):
        """
        """
        result, offset = 0, 0
        while size > 0:
            if not self.__p:
                self.__byte = self.get()
                self.__p = 8
            cbit = self.__byte & (1 << 8 - self.__p)
            self.__p -= 1
            if cbit:
                result = result | (1 << offset)
            offset += 1
            size -= 1
        return result

    def putBits(self, size, value):
        """
        """
        while size > 0:
            if not self.__p:
                self.put(0)
            offset = 8 - self.__p
            if offset > size:
                offset = size
            mask = (value & ((1 << offset) - 1)) << self.__p
            self.__b[len(self.__b) - 1] |= mask
            size -= offset
            value = value >> offset
            self.__p = (self.__p + offset) % 8

    def getRemainingBits(self):
        """
        """
        return self.__p