#!/usr/bin/env python
"""
Rebuilding turtle_frame.cpp in Python
"""

# Currently not supported:
# - graphical output
#   - 2D space
#   - turtle images
#   - all Qt fields and callbacks
# - services
#   - clear
#   - reset
#   - spawn
#   - kill
# - methods
#   - clear

import argparse
import os
import random
from turtle import Turtle

import rospy
from util.rgb import Rgb
from util.point import Point

DEFAULT_BG_R = 0x45
DEFAULT_BG_G = 0x56
DEFAULT_BG_B = 0xff


class TurtleFrame(object):
	""" The turtle frame class """

	_width = 0
	_height = 0
	_background = [[]]
	_turtles = {}

	_id_counter = 0
	_last_turtle_update = None
	_update_interval = None

	_has_gui = False
	_frame_count = 0
	_gui_output = None


	def __init__(self):
		""" Ctor """

		parser = argparse.ArgumentParser(prog="tf")
		parser.add_argument("--draw-gui", "-g", action="store_true", dest="has_gui")
		args = parser.parse_args()

		object.__init__(self)

		# Initialise background (500 x 500)
		self._background = [[
			Rgb(DEFAULT_BG_R, DEFAULT_BG_G, DEFAULT_BG_B) for _ in range(0, 500)
			] for _ in range(0, 500)]
		self._width = len(self._background)
		self._height = len(self._background[0])
		self._has_gui = args.has_gui

		# Only one node can be active at a time. For multiple turtles, rework implementation.
		# rospy.init_node("turtle_frame")
		rospy.set_param("background_r", DEFAULT_BG_R)
		rospy.set_param("background_g", DEFAULT_BG_G)
		rospy.set_param("background_b", DEFAULT_BG_B)

		rospy.loginfo("Starting turtle frame, %s", rospy.get_name())

		trt_x = random.randrange(0, self._width)
		trt_y = random.randrange(0, self._height)

		self._spawn_turtle(trt_x, trt_y)

		# Colouring the background
		# Window is 500 x 500, starting bottom left at 0,0 and ending top right at 499,499

		# Top left: Pastel purple
		self._draw_area(Rgb.pastel_purple(), Point(0, 250), Point(250, 499))
		# Top right: Pastel yellow
		self._draw_area(Rgb.pastel_yellow(), Point(250, 250), Point(499, 499))
		# Bottom left: Pastel green
		self._draw_area(Rgb.pastel_green(), Point(0, 0), Point(250, 250))
		# Bottom right: Pastel blue
		self._draw_area(Rgb.pastel_blue(), Point(250, 0), Point(499, 250))
		# Intrusion zone (middle): Red
		self._draw_area(Rgb.red(), Point(245, 245), Point(255, 255))

		# Initialise GUI (if requested)
		self._redraw()

		# Initialise update timer (16 msec)
		self._update_interval = rospy.Duration(0.016)
		rospy.Timer(self._update_interval, self._update_turtles)

		# Block until shut down
		rospy.spin()


	def _draw_area(self, colour, from_point, to_point):
		"""
		Draw defined area in defined colour.\n
		colour: Instance of Rgb class\n
		top_left/bottom_right: Instances of Point class
		"""

		assert(isinstance(colour, Rgb))
		assert(isinstance(from_point, Point))
		assert(isinstance(to_point, Point))

		from_x = min(from_point.x, to_point.x)
		to_x = max(from_point.x, to_point.x)
		from_y = min(from_point.y, to_point.y)
		to_y = max(from_point.y, to_point.y)

		# BL x, TR y      === TR ===
		# === BL ===      TR x, BL y

		# pylint: disable-msg=C0103; (Invalid variable names x, y)
		for x in range(from_x, to_x + 1):
			for y in range(from_y, to_y + 1):
				self._background[x][y] = colour


	def _spawn_turtle(self, trt_x, trt_y, name=None):
		""" Add a turtle to the field at the given coordinates. """

		if name is None or name == "":
			name = self._create_unique_turtle_name()
		elif self._has_turtle(name):
			return ""

		turtle = Turtle(name, Point(trt_x, trt_y))
		self._turtles[name] = turtle

		rospy.loginfo("New turtle at [%s] at x=[%f], y=[%f]", name, trt_x, trt_y)

		return name


	def _create_unique_turtle_name(self):
		""" Increase the ID counter until a unique name of the form "turtle<id>" is found. """

		self._id_counter += 1
		new_name = "turtle{}".format(self._id_counter)

		if self._has_turtle(new_name):
			return self._create_unique_turtle_name()

		return new_name


	def _has_turtle(self, name):
		""" Check the turtles for the given name. """
		return name in self._turtles


	def _update_turtles(self, _):
		""" Update callback: Call update() on all turtles and redraws GUI. """

		if self._last_turtle_update is None:
			self._last_turtle_update = rospy.Time.now()
			return

		modified = False
		for key in self._turtles:
			modified |= self._turtles[key].update(
				self._update_interval.to_sec(), self._background, self._width, self._height)

		if modified:
			self._redraw()

		self._frame_count += 1


	def _redraw(self):
		""" Draw an updated GUI output. """

		if not self._has_gui:
			return

		if self._gui_output is None:
			self._gui_output = [["" for _ in range(0, 50)] for _ in range(0, 50)]

		self._update_output()

		os.system("clear")

		# pylint: disable-msg=C0103; (Invalid variable names x, y)
		# We draw from top left (0,49) to bottom right (49,0)
		for y in range(49, -1, -1):
			line_output = ""
			for x in range(0, 50):
				line_output += self._gui_output[x][y] + " "
			print(line_output)


	def _update_output(self):
		""" Update the GUI output in scale 1:10. Turtle is marked with "-". """

		# pylint: disable-msg=C0103; (Invalid variable names x, y)
		for x in range(0, 50):
			for y in range(0, 50):
				self._gui_output[x][y] = self._get_output_letter(
					self._background[x*10][y*10])

		for turtle in self._turtles.values():
			trt_x = turtle.pos.x / 10
			trt_y = turtle.pos.y / 10
			for x in range(max(trt_x-1, 0), min(trt_x+2, 50)):
				for y in range(max(trt_y-1, 0), min(trt_y+2, 50)):
					self._gui_output[x][y] = " "

			self._gui_output[turtle.pos.x / 10][turtle.pos.y / 10] = "-"


	def _get_output_letter(self, rgb):
		""" Produce a letter for the given Rgb. Returns "?" for unknown colours. """

		if rgb == Rgb.pastel_purple():
			return "u"
		elif rgb == Rgb.pastel_yellow():
			return "y"
		elif rgb == Rgb.pastel_green():
			return "g"
		elif rgb == Rgb.pastel_blue():
			return "b"
		elif rgb == Rgb.red():
			return "R"

		return "?"



if __name__ == "__main__":
	TF = TurtleFrame()
