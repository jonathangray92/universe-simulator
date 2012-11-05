"""
This module will handle all pyplot functionality.

"""

import matplotlib.pyplot as plt
from settings import *
from universe import Universe
from os import makedirs
from os.path import exists as path_exists

class Graphics(object):
	""" Each object of this class handles the graphics of a universe object. """
	def __init__(self, universe):
		""" Initialize an object with the universe object to visualize. """
		assert type(universe) == Universe
		self.universe = universe
		self.fig = plt.figure()
		self.ax = self.fig.add_subplot(111)

	def generate_plot(self):
		""" Generate the plot and do nothing with it. """
		x, y = zip(*[p.p for p in self.universe])
		self.ax.cla()
		self.ax.plot(x, y, '.')
		self.ax.set_title('Universe at time: %d' % self.universe.time)
		self.ax.set_xlim([P_MU-4*P_STD, P_MU+4*P_STD])
		self.ax.set_ylim([P_MU-4*P_STD, P_MU+4*P_STD])

	def show_plot(self):
		""" Generate and show a 2d plot of the universe. """
		self.generate_plot()
		plt.show()

	def save_plot(self):
		""" Save plot to the dumps/ folder """
		# Generate the plot
		self.generate_plot()
		# Create save directory
		directory = './dumps/%s/' % str(int(self.universe.init_time))
		if not path_exists(directory):
			makedirs(directory)
		# Save image file
		self.fig.savefig(directory+str(self.universe.time))