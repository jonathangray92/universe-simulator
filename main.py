from settings import *
from universe import Universe, Particle
import argparse
try:
	from graphics import Graphics
	graphics_imported = True
except ImportError:
	graphics_imported = False

def main():
	# Parse arguments
	argparser = argparse.ArgumentParser()
	argparser.add_argument('-g', '--graphics', action="store_true")
	flags = argparser.parse_args()

	# Let there be light! (create an N-particle universe)
	universe = Universe(N_PARTICLES)
	print universe
	
	# Create graphics 
	if flags.graphics and graphics_imported:
		graph = Graphics(universe, GRAPHICS_DIR)
		graph.save_plot()
	
	# Incremenent time
	for i in xrange(50):
		print 'Computing step', i+1
		universe.increment_time()
		if flags.graphics and graphics_imported:
			graph.save_plot()

if __name__ == '__main__':
	main()