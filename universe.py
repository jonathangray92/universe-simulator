"""
This module serves to implement the Universe class, from which a simulation can
be run. A Universe object consists mostly of an R-Tree of Particles packaged 
with methods to control those particles efficiently.

"""

from vector import Vector
from RTree import RTree
from random import gauss, uniform
from settings import *
from time import time as unix_time

class Particle(object):
	""" Particles have position and velocity vectors. """
	def __init__(self, p, v):
		""" Position and velocity can be initialized with Vectors or tuples. """
		# Position
		if type(p) == tuple:
			self.p = Vector(*p)
		elif type(p) == Vector:
			self.p = p
		else:
			raise Exception('Unknown parameter passed to Particle.__init__()')
		# Velocity
		if type(v) == tuple:
			self.v = Vector(*v)
		elif type(v) == Vector:
			self.v = v
		else:
			raise Exception('Unknown parameter passed to Particle.__init__()')

	def __str__(self):
		""" String representation is a 4-tuple of position, velocity. """
		return '(%f, %f, %f, %f)' % (self.p.x, self.p.y, self.v.x, self.v.y)
	
	def update_position(self):
		""" Updates position vector by current velocity. """
		self.p += self.v

	def get_x(self):
		""" Getter function for x-position. """
		return self.p.x

	def get_y(self):
		""" Getter function for y-position. """
		return self.p.y



class Universe(object):
	""" Universe object contains all the information of the universe at an instant. """

	#################
	# Magic Methods #
	################# 
	def __init__(self, N):
		""" Create a universe with N particles in it. """
		self.N = N
		self.particles = self.initialize_particles(N)
		self.time = 0
		self.init_time = unix_time()

	def __iter__(self):
		""" Yields all particles in the universe, one by one. """
		for p in self.particles:
			yield p

	def __str__(self):
		""" For now, string representation defaults to that of its R-Tree. """
		return str(self.particles)

	##################
	# Public Methods #
	################## 
	def invrsquared(self, p1, p2):
		""" Returns gravitation WITHOUT CONSTANTS = (p2 - p1) / r^3 """
		try:
			pos1 = p1.p
		except AttributeError:
			pos1 = p1
		try:
			pos2 = p2.p
		except AttributeError:
			pos2 = p2
		rvec = pos2 - pos1
		return rvec / (rvec.get_x()**2 + rvec.get_y()**2)**(1.5)


	def initialize_particles(self, N):
		""" Return an R-Tree with N randomized particles. """
		tree = RTree()
		for _ in xrange(N):
			p = Vector(gauss(P_MU, P_STD), gauss(P_MU, P_STD))
			v = Vector(uniform(-V_MAX, V_MAX), uniform(-V_MAX, V_MAX))
			tree.insert(Particle(p, v))
		return tree

	def increment_time(self):
		""" Increment a single time step, performing all calculations. """
		self.time += 1
		self.update_all_particles_velocity()
		self.update_all_particles_position()

	def update_all_particles_position(self):
		""" 
		Calls p.update_position() on all particles. Makes note of the particles
		which leave the bounds of their leaf nodes, and reinserts them into the 
		tree at the end. 
		"""
		# Update positions for all leaves. Note all that leave leaf boundaries
		reinsert = []
		for leaf in self.particles.all_leaf_nodes():
			for p in leaf: 
				p.update_position()
				if not p in leaf:
					reinsert.append((p, leaf))
		# Remove all nodes that need reinsertion
		for p, leaf in reinsert:
			leaf.children.remove(p)
		# Recalculate mean/N for all nodes
		self.particles.recalculate_all()
		# Reinsert all nodes that were removed
		for p, _ in reinsert:
			self.particles.insert(p)


	def update_all_particles_velocity(self):
		""" Calls self.update_particle_velocity() on all particles. """
		for p in self.particles:
			self.update_particle_velocity(p)

	def update_particle_velocity(self, p):
		""" 
		Updates the velocity vector of particle p due to all gravity. 
		1. Particles in the same node are treated individually
		2. Check particles in sibling node
		3. Move up a level, and check particles in sibling node
		4. Repeat step 3
		"""
		# Initial stuff
		assert type(p) == Particle
		gravity = Vector(0, 0)
		# Find tree node that holds p
		node = self.particles.search(p)
		# Calculate gravity between individual particles in node
		for part in node: 
			if part == p: 
				continue
			gravity += self.invrsquared(p, part)
		# Check all "other" nodes that do not contain p
		for other in self.particles.upward_sibling_traversal(node):
			gravity += other.N * self.invrsquared(p, other.mean)
		# Scale gravity and update velocity
		p.v += GRAV * gravity
