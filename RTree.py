"""
This module contains a custom implementation of the R-Tree data structure, 
intended to be used to store a large number of points in 2d space. 

"""

from vector import Vector
from settings import *


class RTreeNode(object):
	# Node will split when N > MAX_N
	MAX_N = LEAF_MAX

	#################
	# Magic Methods #
	#################
	def __init__(self):
		self.N = 0
		self.parent = None
		self.xmin = None
		self.xmax = None
		self.ymin = None
		self.ymax = None
		self.mean = Vector(0, 0)

	def __str__(self):
		""" Returns string representation containing useful information. """
		return 'N: {}\nx-range: ({:.2f}, {:.2f})\ny-range: ({:.2f}, {:.2f})\nmean: {:s}\n'.format(\
			self.N, self.xmin, self.xmax, self.ymin, self.ymax, self.mean)

	def __contains__(self, p):
		return self.contains_point(p)

	##################
	# Public Methods #
	################## 
	def contains_point(self, p):
		""" Returns True if point p is in rectangle, else False. """
		if self.xmin <= p.get_x() <= self.xmax and self.ymin <= p.get_y() <= self.ymax:
			return True
		else:
			return False

	def expand_rectangle(self, p):
		""" Expands rectangle to include point p. """
		self.xmin = min(self.xmin, p.get_x()) if self.xmin else p.get_x()
		self.xmax = max(self.xmax, p.get_x()) if self.xmax else p.get_x()
		self.ymin = min(self.ymin, p.get_y()) if self.ymin else p.get_y()
		self.ymax = max(self.ymax, p.get_y()) if self.ymax else p.get_y()

	def expansion_heuristic(self, p):
		""" 
		Returns the area increase necessary for the bounding rectangle to
		include the point p. 
		"""
		# Find x and y increases necessary to bound p (heuristic, not exact)
		delta_x = max(p.get_x() - self.xmax, self.xmin - p.get_x(), 0)
		delta_y = max(p.get_y() - self.ymax, self.ymin - p.get_y(), 0)
		if p in self:
			assert delta_x + delta_y == 0
		return delta_x * (self.ymax - self.ymin) + delta_y * (self.xmax - self.xmin)

	def sibling(self):
		""" Return self.parent's other child, or None if self has no parent. """
		if self.parent is None:
			return None
		if self.parent.left == self:
			return self.parent.right
		else:
			return self.parent.left




class LeafNode(RTreeNode):
	""" Leaf nodes contain a list of objects with positions. """
	def __init__(self, parent=None):
		RTreeNode.__init__(self)
		self.children = []
		self.parent = parent

	def __iter__(self):
		""" Yields all children contained by leaf node. """
		for p in self.children:
			yield p

	def insert(self, p):
		""" Insert object p, expanding rectangle as necessary. """
		# Add object to list
		self.N += 1
		self.children.append(p)
		# Check if node needs to split
		if self.N > self.MAX_N:
			self.split()
		else:
			# Expand rectangle
			self.expand_rectangle(p)
			# Adjust mean (x,y)
			try:
				self.mean = (self.N - 1.0) / self.N * self.mean + p.p / self.N
			except AttributeError:
				self.mean = (self.N - 1.0) / self.N * self.mean + p / self.N

	def recalculate(self):
		""" Recalculate mean and N by scratch. """
		self.N = len(self.children)
		self.mean = Vector(0, 0)
		for p in self.children:
			self.mean += p.p / self.N

	def remove(self, p):
		""" Remove p from self.children, and recalculate ONLY this node's properties. """
		# NOTE THAT THE BOUNDING RECTANGLE MAY NOT BE "TIGHT" ANYMORE
		self.chilren.remove(p)
		self.N -= 1
		try:
			self.mean = (self.N + 1.0) / self.N * self.mean - p.p / self.N
		except AttributeError:
			self.mean = (self.N + 1.0) / self.N * self.mean - p / self.N

	def split(self):
		""" 
		This method is called when a leaf node is overflowing. Generate a page
		node from this node's data, and replace this node with the page node. 

		This method should not be called on the root node of an R-Tree. That case
		should be handled in the insert method of the R-Tree, so that the root
		can be properly updated.
		"""
		if self.parent is None:
			raise NeedReplaceRoot(PageNode(self))
		elif self.parent.left == self:
			self.parent.left = PageNode(self)
		elif self.parent.right == self:
			self.parent.right = PageNode(self)
		else:
			raise Exception('Node does not match either of its parents\' children.')



class PageNode(RTreeNode):
	""" Page Nodes have two RTreeNode children. Their bounding rectangles contain
	both children's rectangles. """
	def __init__(self, leaf):
		""" A page node is built from an overflowing leaf node. """
		RTreeNode.__init__(self)
		# Initialize this, and two new leaf nodes
		self.left = LeafNode(self)
		self.right = LeafNode(self)
		self.parent = leaf.parent
		# Split the rectangle through its longer side
		if leaf.xmax - leaf.xmin > leaf.ymax - leaf.ymin:
			send_left = lambda p: p.get_x() < leaf.mean.x
		else:
			send_left = lambda p: p.get_y() < leaf.mean.y
		# Insert all leaf children into left or right leaf nodes
		for p in leaf.children:
			if send_left(p): 
				self.left.insert(p)
			else:
				self.right.insert(p)
		# Calculate RTreeNode properties for this page
		self.N = leaf.N
		self.parent = None
		self.xmin = min(self.left.xmin, self.right.xmin)
		self.xmax = max(self.left.xmax, self.right.xmax)
		self.ymin = min(self.left.ymin, self.right.ymin)
		self.ymax = max(self.left.ymax, self.right.ymax)
		self.mean = float(self.left.N) / self.N * self.left.mean + float(self.right.N) / self.N * self.right.mean

	def __iter__(self):
		""" Yields all children contained in this page. """
		for p in self.left:
			yield p
		for p in self.right:
			yield p

	def leafs_below(self):
		""" Yields all leaf nodes in this page. """
		if type(self.left) == LeafNode:
			yield self.left
		else:
			for n in self.left.leafs_below():
				yield n
		if type(self.right) == LeafNode:
			yield self.right
		else:
			for n in self.right.leafs_below():
				yield n

	def insert(self, p):
		""" Insert point p into one of the child nodes, and update bounding rectangle. """
		# Insert p into one of the child nodes
		if self.left.expansion_heuristic(p) < self.right.expansion_heuristic(p):
			self.left.insert(p)
		else:
			self.right.insert(p)
		# Update RTreeNode properties to include p
		self.expand_rectangle(p)
		self.N += 1
		self.mean = (float(self.left.N) / self.N) * self.left.mean + \
					(float(self.right.N) / self.N) * self.right.mean

	def recalculate(self):
		""" Recalculate left and right children, and then recalculate this one. """
		self.left.recalculate()
		self.right.recalculate()
		self.N = self.left.N + self.right.N
		if self.N == 0: 
			self.mean = Vector(0, 0)
		self.mean = float(self.left.N)/self.N * self.left.mean + \
					float(self.right.N) / self.N * self.right.mean



class NeedReplaceRoot(Exception):
	""" Custom exception, raised once when the original leaf root splits. """
	def __init__(self, new_root):
		self.new_root = new_root
		


class RTree(object):
	""" Custom RTree implementation. Uses Node classes above. """
	#################
	# Magic Methods #
	################# 
	def __init__(self):
		""" An empty tree contains one empty leaf node as the root. """
		self.root = LeafNode()

	def __iter__(self):
		""" Yields all children of all nodes in the tree. """
		for p in self.root:
			yield p

	def __str__(self):
		""" Returns the string implementation of its root node. """
		return str(self.root)

	##################
	# Public Methods #
	################## 
	def all_leaf_nodes(self):
		""" Yields all leaf nodes in the tree. """
		if type(self.root) == LeafNode:
			yield self.root
		else:
			for n in self.root.leafs_below():
				yield n

	def insert(self, p):
		""" Call the insert function of the root node. """
		try:
			self.root.insert(p)
		except NeedReplaceRoot as e:
			self.root = e.new_root

	def search(self, p):
		""" 
		Returns the node that contains p, or None if outside the tree. Searches
		until a leaf node is found, or until p could be in left or right children. 
		"""
		# Check if p is in the tree
		if not p in self.root:
			return None
		# If so, binary search
		search = self.root
		while type(search) != LeafNode:
			if p in search.left:
				if p in search.right:
					return search
				else:
					search = search.left
			elif p in search.right:
				search = search.right
			else:
				raise Exception('Search Error: p not found in either left/right children.')
		# If while loop breaks, a leaf node is found, so return it
		else:
			return search
		# If the method makes it here, something is very wrong. 
		raise Exception('Search Error: method should return before this point.')

	def recalculate_all(self):
		""" Calls the recalculate function of the root node. """
		self.root.recalculate()

	def upward_sibling_traversal(self, node):
		""" 
		Yields the sibling of node, then the sibling of node's parent,
		then the sibling of node's grandparent, etc.
		"""
		trav = node
		while trav.parent: 
			yield trav.sibling()
			trav = trav.parent