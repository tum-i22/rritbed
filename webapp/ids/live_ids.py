#!/usr/bin/env python
""" Live IDS """

import os
import time
import uuid
from enum import Enum

class LiveIds(object):
	""" Live intrusion detection """

	LOG_DIR = "log"
	LOG_FILE_PREFIX = "log"

	def __init__(self):
		""" Ctor """

		object.__init__(self)


	def process(self, log_entry):
		""" Process the given entry. Outputs a warning when the detection was successful. """

		classification = self._classify(log_entry)
		if classification == IdsClassification.normal:
			return

		# Assert after most returns are done for improved performance; the above check still works.
		assert(isinstance(classification, IdsClassification))

		self._print_and_log_intrusion(log_entry, classification)

		raise NotImplementedError()


	def _classify(self, log_entry):
		"""
		Classify the given log entry and return the classification.
		returns: An IdsClassification object
		"""

		raise NotImplementedError()


	def _print_and_log_intrusion(self, log_entry, classification):
		""" Print a warning and log the given intrusion in a new file. """

		raise NotImplementedError()


# pylint: disable-msg=R0903; (Too few public methods)
class IdsClassification(Enum):
	""" IDS classification results """

	normal = 0
	intrusion = 1
