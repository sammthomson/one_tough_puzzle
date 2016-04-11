""" Unit tests for puzzle.py

Author: Sam Thomson
Date: 1/1/2012
"""
from unittest import TestCase, main

from puzzle import (
    HEART, CLUB, DIAMOND, SPADE, PIECES, reshape, Side, PartialSolution,
    Solver)


class TestSides(TestCase):
    def setUp(self):
        self.h_out = Side(HEART, True)
        self.h_in = Side(HEART, False)
        self.c_out = Side(CLUB, True)

    def test_side_fit(self):
        """ Check that sides only fit if they have the same shape and
        complementary extrudes """
        self.assertTrue(self.h_out.fits_with(self.h_in))
        self.assertFalse(self.h_out.fits_with(self.h_out))
        self.assertFalse(self.h_out.fits_with(self.c_out))
        self.assertFalse(self.h_in.fits_with(self.c_out))

class TestPartialSolution(TestCase):
    def setUp(self):
        pieces = PIECES[:5]
        pieces[3] = pieces[3].spun(1)
        self.first_four = PartialSolution(reshape(pieces[:4]))
        self.first_five = PartialSolution(reshape(pieces))
    
    def test_check(self):
        # first four pieces fit, but fifth doesn't
        self.assertTrue(self.first_four.check())
        self.assertFalse(self.first_five.check())

class TestSolver(TestCase):
    def setUp(self):
        self.solver = Solver()

    def test_solver(self):
        """ Check that solver produces a valid solution """
        soln = self.solver.solve()
        self.assertTrue(soln.check())

if __name__ == "__main__":
    main()
