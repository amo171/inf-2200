'''
Code written for inf-2200, University of Tromso

This file is not actual part of assignment, it just assures that
the functions in common.py work as intended, and demonstrate how
unit tests can be written using the unittest python module.
'''

import operator
import unittest
from common import *

def lrange(num1, num2 = None, step = 1):
    op = operator.__lt__

    if num2 is None:
        num1, num2 = 0, num1
    if num2 < num1:
        if step > 0:
            num1 = num2
        op = operator.__gt__
    elif step < 0:
        num1 = num2

    while op(num1, num2):
        yield num1
        num1 += step

class TestCommon(unittest.TestCase):
    def setUp(self):
        pass

    def test_signed_conversion(self):
        for a in range(-100, 200):
            for b in range(-100, 200):
                ra = fromUnsignedWordToSignedWord(a)
                rb = fromUnsignedWordToSignedWord(b)

                self.assertEqual(a, ra) # Signed-to-signed conversion does not alter value
                self.assertEqual(b, rb) # Signed-to-signed conversion does not alter value

                self.assertEqual(fromSignedWordToUnsignedWord(a + b), fromSignedWordToUnsignedWord(ra + rb))
                self.assertEqual(fromSignedWordToUnsignedWord(a - b), fromSignedWordToUnsignedWord(ra - rb))
                self.assertEqual(fromSignedWordToUnsignedWord(a & b), fromSignedWordToUnsignedWord(ra & rb))
                self.assertEqual(fromSignedWordToUnsignedWord(a | b), fromSignedWordToUnsignedWord(ra | rb))
                self.assertEqual(fromSignedWordToUnsignedWord(~(a | b)), fromSignedWordToUnsignedWord(~(ra | rb)))

        for a in lrange(0x7ffff000, 0x8000f000):
            b = fromUnsignedWordToSignedWord(a)
            c = fromSignedWordToUnsignedWord(a)
            r = fromSignedWordToUnsignedWord(b)

            self.assertEqual(a, r)
            self.assertEqual(a, c) # Unsigned-to-unsigned does not alter value

if __name__ == '__main__':
    unittest.main()
