# from graphics import Graphics
from settings import *
from universe import Universe, Particle

def main():
	universe = Universe(N_PARTICLES)
	print universe
	# graph = Graphics(universe)
	# graph.save_plot()
	
	for _ in xrange(1):
		universe.increment_time()
	# 	graph.save_plot()

	for particle in universe.particles:
		print particle 

if __name__ == '__main__':
	main()