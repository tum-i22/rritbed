#!/usr/bin/env python
""" Printer class """

from __future__ import print_function
import sys


class Printer(object):
	""" Printer that allows squelching output. """

	def __init__(self, squelch=False, verbose=True, name=None):
		""" Ctor """

		object.__init__(self)

		self.squelch = squelch
		self.verbose = verbose
		self.name = name
		self.last_ended_in_newline = True


	def prt(self, message, only_verbose=False, preface=True, newline=True):
		"""
		Print if not squelching. Handles newline characters in the message.
		: param only_verbose : Pass True to only print the message in verbose mode.
		"""

		for line in message.split("\n"):
			self._prt_line(line, only_verbose, preface, newline)


	def _prt_line(self, line, only_verbose, preface, newline):
		""" Print single line. """

		if self.squelch or only_verbose and not self.verbose:
			return

		if preface and self.name and self.last_ended_in_newline:
			line = self._preface_line(line)
		self.last_ended_in_newline = newline

		print(line, end="\n" if newline else "")
		sys.stdout.flush()


	def _preface_line(self, line):
		""" Preface the given line with the contained name. """
		return "[{}] {}".format(self.name, line)



class Storer(Printer):
	"""
	Printer replacement that stores all lines given to it.
	Does NOT support verbosity or non-newlines when storing!
	"""

	def __init__(self, squelch=False, verbose=True, name=None):
		""" Ctor """

		super(Storer, self).__init__(squelch, verbose, name)
		self.lines = []


	def prt(self, message, only_verbose=False, preface=True, newline=True):
		""" Save the given message. """

		self.lines.append((message, only_verbose, preface, newline))
