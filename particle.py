from vector import Vector 

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

	def __repr__(self):
		""" String representation is a 4-tuple of position, velocity. """
		return '<Particle: (%f, %f, %f, %f)>' % (self.p.x, self.p.y, self.v.x, self.v.y)
	
	def get_x(self):
		""" Getter function for x-position. """
		return self.p.x

	def get_y(self):
		""" Getter function for y-position. """
		return self.p.y
