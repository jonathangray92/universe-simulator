""" 
Custom quad-tree implementation
"""

from math import atan2, pi

class QTree():
	""" 
	QTree has four children, each of which is a single point or a QTree. 
	Almost all algorithms are recursive based on this property. 
	"""

	#####################
	### Magic Methods ###
	#####################
	def __init__(self, P):
		""" Initialize a new tree rooted around point P. """
		self.root = P
		self.centroid = P.p
		self.weight = 1
		self.sub_NE = None
		self.sub_NW = None
		self.sub_SE = None
		self.sub_SW = None

	def __repr__(self):
		""" String representation lists root, centroid, and weight. """
		return '<QTree: %r, %r, %r>' % (self.root, self.centroid, self.weight)


	######################
	### Public Methods ###
	######################
	def insert(self, P):
		""" Insert point P into the tree. """
		# Insert into the proper subtree, or create it if necessary
		if P.get_x() < self.root.get_x():
			if P.get_y() < self.root.get_y():
				if self.sub_SW: 
					self.sub_SW.insert(P)
				else: 
					self.sub_SW = QTree(P)
			else:
				if self.sub_NW: 
					self.sub_NW.insert(P)
				else: 
					self.sub_NW = QTree(P)
		else:
			if P.get_y() < self.root.get_y():
				if self.sub_SE: 
					self.sub_SE.insert(P)
				else: 
					self.sub_SE = QTree(P)
			else:
				if self.sub_NE: 
					self.sub_NE.insert(P)
				else: 
					self.sub_NE = QTree(P)
		# Update statistics
		self.weight += 1
		self.centroid = (self.weight-1)/self.weight * self.centroid + P.p / self.weight


	def traverse_all(self):
		""" Generate all points in tree. """
		yield self.root
		if self.sub_NE: 
			for p in self.sub_NE.traverse_all():
				yield p
		if self.sub_NW: 
			for p in self.sub_NW.traverse_all():
				yield p
		if self.sub_SE: 
			for p in self.sub_SE.traverse_all():
				yield p
		if self.sub_SW: 
			for p in self.sub_SW.traverse_all():
				yield p



	def traverse_neighbours(self, P, d):
		""" 
		Generate nearby points and clusters of faraway points. The yield of this 
		generator will be a set of points with masses to be used in gravity
		calculations. The input is a point P and a minimum distance d from P
		for clustering. 

		Yields tuples: (Vector, weight)
		"""
		# Find position of P relative to root
		x_dist = P.get_x() - self.root.get_x()
		y_dist = P.get_y() - self.root.get_y()
		r_dist = (x_dist**2 + y_dist**2)**.5
		theta = atan2(y_dist, x_dist)

		# Re-orient quadrants, so that algorithm can be written in terms of 
		# P's quadrant, quad opposite P in x/y directions, and quad diagonally
		# opposite P
		if theta < -pi/2:
			(quad, opp_x, opp_y, opp_diag) = (self.sub_SW, self.sub_SE, self.sub_NW, self.sub_NE)
		elif theta < 0:
			(quad, opp_x, opp_y, opp_diag) = (self.sub_SE, self.sub_SW, self.sub_NE, self.sub_NW)
		elif theta < pi/2:
			(quad, opp_x, opp_y, opp_diag) = (self.sub_NE, self.sub_NW, self.sub_SE, self.sub_SW)
		else:
			(quad, opp_x, opp_y, opp_diag) = (self.sub_NW, self.sub_NE, self.sub_SW, self.sub_SE)

		# Always yield the root and traverse the quadrant in which P is located
		# Note: P is not considered to be a neighbour of P, so don't yield it
		if self.root != P:
			yield (self.root, 1)
		if quad: 
			for y in quad.traverse_neighbours(P, d): 
				yield y

		# If d >= r_dist, and traverse all quadrants
		if d >= r_dist:
			if opp_x:
				for y in opp_x.traverse_neighbours(P, d): 
					yield y
			if opp_y:
				for y in opp_y.traverse_neighbours(P, d): 
					yield y
			if opp_diag:
				for y in opp_diag.traverse_neighbours(P, d): 
					yield y

		# If d < r_dist, the diagonal will be yielded, and the opposite quads
		# will be either yielded or traversed
		else:
			if opp_diag:
				yield (opp_diag.centroid, opp_diag.weight)
			if opp_x:
				if d > abs(x_dist):
					for y in opp_x.traverse_neighbours(P, d):
						yield y
				else:
					yield (opp_x.centroid, opp_x.weight)
			if opp_y:
				if d > abs(y_dist):
					for y in opp_y.traverse_neighbours(P, d):
						yield y
				else:
					yield (opp_y.centroid, opp_y.weight)


	#######################
	### Private Methods ###
	#######################