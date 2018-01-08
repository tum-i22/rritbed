#!/usr/bin/env python
"""
Launch file orchestrator
For usage see _help() method.
"""

import sys

class LaunchFileOrchestrator(object):
	""" Creates a launch file based on the given arguments """

	_help_text = """
Usage:
lfo </path/to/file> [OPTIONS]

Possible OPTIONS:
--help     : Display this help
-m         : Create launch file with only one manually controlled turtle,
             a logger node and rosbag recording.
             Excludes all other options!
-i="/file" : Path to file with identifiers to use for namespaces.
             Limits number of namespaces to the number of individual 
             identifiers in file!
-n=NUMBER  : Number of namespaces to create
	"""

	def __init__(self):
		""" Ctor """

		object.__init__(self)

		args = sys.argv[1:]

		if "--help" in args or not args:
			self._print_help()
			exit()

		# TODO: Read arguments


	def create(self):
		# TODO: Create just one launch file with multiple namespaces!
		# Use VIN as namespace name?
		# "Manual" launch *is* supposed to be one launch file with *just* the manually controlled turtle
		# Pass as arguments instead the number of namespaces or a file with identifiers?
		pass


	def _print_help(self):
		print(self._help_text)



if __name__ == "__main__":
	LFO = LaunchFileOrchestrator()
	LFO.create()
