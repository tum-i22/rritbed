#!/usr/bin/env python
""" Unit tests for the ArgumentConstraint class """

import random
import unittest

from sys import maxint as MAXINT
from parameterized import parameterized

from argument_constraint import ArgumentConstraint


class Tests(unittest.TestCase):
	""" All tests """

	@parameterized.expand([
		(1, 1, 1), # all overlapping
		(-1, -1, 1), # default overlapping min
		(1, -1, 1), # default overlapping max
		(0, -2, 2) # default not overlapping
	])
	def test_ctor_valid(self, default_value, min_value, max_value):
		""" Tests for the constructor with valid inputs """
		# Test will fail if the constructor raises an error
		ArgumentConstraint(default_value, min_value, max_value)


	@parameterized.expand([
		(1, 0, 0), # default > max
		(-1, 0, 0), # default < min
		(0, 1, -1), # max < min
	])
	def test_ctor_invalid(self, default_value, min_value, max_value):
		""" Tests for the constructor with invalid inputs """
		with self.assertRaises(ValueError):
			ArgumentConstraint(default_value, min_value, max_value)


	@parameterized.expand([
		(1, 1, 1, 1), # hits both ends
		(0, -1, 1, 0), # is default value
		(0, -1, 1, -1), # hits min
		(0, -1, 1, 1), # hits max
		(0, -2, 2, 1) # random value
	])
	def test_fits_does(self, default_value, min_value, max_value, test_value):
		""" Tests valid fits """
		self._test_fits(default_value, min_value, max_value, test_value, True)


	@parameterized.expand([
		(0, 0, 0, 1), # too big
		(0, 0, 0, -1), # too small
		(0, -1, 1, 100), # way too big
		(0, -1, 1, -100) # way too small
	])
	def test_fits_doesnt(self, default_value, min_value, max_value, test_value):
		""" Tests invalid fits """
		self._test_fits(default_value, min_value, max_value, test_value, False)


	def _test_fits(self, default_value, min_value, max_value, test_value, expected):
		constraint = ArgumentConstraint(default_value, min_value, max_value)
		self.assertEqual(constraint.fits(test_value), expected)


	def test_floatification(self):
		""" Random test ensuring all values put into the class are floatified """

		almost_maxint = MAXINT - 200
		value = random.uniform(-almost_maxint-1, almost_maxint)
		min_val = value - 200
		max_val = value + 200

		constraint = ArgumentConstraint(value, min_val, max_val)

		self.assertIsInstance(constraint.default_value, float)
		self.assertIsInstance(constraint.min_value, float)
		self.assertIsInstance(constraint.max_value, float)

		self.assertEqual(value, constraint.default_value)
		self.assertEqual(min_val, constraint.min_value)
		self.assertEqual(max_val, constraint.max_value)
