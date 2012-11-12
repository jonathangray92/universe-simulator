"""
This module contains a 2d Vector class that can be used to represent a point 
in 2d space. Simple vector mathemetics is implemented. 

"""

class Vector(object):
	""" 2d vectors can represent position, velocity, etc. """

	#################
	# Magic Methods #
	#################
	def __init__(self, x, y):
		""" Vector must be initialized with values. """
		self.x = float(x)
		self.y = float(y)
		
	def __add__(self, other):
		""" Overloads Vector + Vector syntax. """
		return Vector(self.x + other.x, self.y + other.y)

	def __div__(self, other):
		""" Overloads Vector / constant syntax. """
		return Vector(self.x / other, self.y / other)

	def __iadd__(self, other):
		""" Overloads Vector += Vector syntax. """
		self.x += other.x
		self.y += other.y
		return self

	def __imul__(self, other):
		""" Overloads Vector *= constant syntax. """
		self.x *= other
		self.y *= other
		return self

	def __isub__(self, other):
		""" Overloads Vector -= Vector syntax. """
		self.x -= other.x
		self.y -= other.y
		return self

	def __iter__(self):
		""" Allows Vector objects to be converted to tuples, lists. """
		yield self.x
		yield self.y

	def __mul__(self, other):
		""" Overloads Vector * constant syntax. """
		return Vector(self.x * other, self.y * other)

	def __neg__(self):
		""" Overloads -Vector syntax. """
		return Vector(-self.x, -self.y)

	def __rmul__(self, other):
		""" Overloads constant * Vector syntax. """
		return self.__mul__(other)

	def __repr__(self):
		""" Returns string representation of vector. """
		return '<Vector (%f, %f)>' % (self.x, self.y)

	def __sub__(self, other):
		""" Overloads Vector - Vector syntax. """
		return Vector(self.x - other.x, self.y - other.y)

	##################
	# Public Methods #
	################## 
	def get_x(self):
		""" Getter for x position. """
		return self.x

	def get_y(self):
		""" Getter for y position. """
		return self.y

	def norm(self):
		""" Returns the norm of the vector. """
		return (self.x**2 + self.y**2)**(0.5)



def euclidean(a, b):
	return ((a.get_x() - b.get_x())**2 + (a.get_y() - b.get_y())**2)**.5