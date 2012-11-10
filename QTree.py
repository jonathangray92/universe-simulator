""" 
Custom quad-tree implementation
"""

class QTree():
	""" 
	QTree has four children, each of which is a single point or a QTree. 
	Almost all algorithms are recursive based on this property. 
	"""

	#####################
	### Magic Methods ###
	#####################
	def __init__(self, objects):
		""" Generate a tree from an iterable containing objects with 2d positions. """
		pass

	######################
	### Public Methods ###
	######################
	def traverse_all(self):
		""" Generate all points in tree. """
		pass


	def traverse_neighbours(self, P, d):
		""" 
		Generate nearby points and clusters of faraway points. The yield of this 
		generator will be a set of points with masses to be used in gravity
		calculations. The input is a point P and a minimum distance d from P
		for clustering. 
		"""
		pass


	#######################
	### Private Methods ###
	#######################