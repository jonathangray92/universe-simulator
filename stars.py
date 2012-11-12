from QTree import QTree
from vector import Vector
from random import gauss, uniform
import settings

class Stars():
	""" Collection of stars and functions to manipulate them. """
	#####################
	### Magic Methods ###
	#####################
	def __init__(self):
		""" Initialize a QTree and populate it with randomized stars. """
		self.tree = QTree()
		for _ in xrange(settings.N_PARTICLES):
			p = Vector(gauss(P_MU, P_STD), gauss(P_MU, P_STD))
			v = Vector(uniform(-V_MAX, V_MAX), uniform(-V_MAX, V_MAX))
			tree.insert(Particle(p, v))

	######################
	### Public Methods ###
	######################
	def compute_step(self):
		""" Recompute pos/vel vectors for all stars. """
		# Compute new velocity/position for each particle, but don't change 
		# the particles' attributes until after all stars are finished
		save_for_later = []
		for star in self.tree.traverse_all():
			# Save neighbours into memory for speed. Change this later? 
			clusters = list(self.tree.traverse_neighbours(star, 5.0))
			# Compute Runge Kutta coefficients
			k1v = G * sum(cluster[1] * self._invrsquared(star.p, cluster[0]) for cluster in clusters)
			k1r = star.v
			k2v = G * sum(cluster[1] * self._invrsquared(star.p + 0.5*k1r, cluster[0]) for cluster in clusters)
			k2r = P1.v * k1v * 0.5
			k3v = G * sum(cluster[1] * self._invrsquared(star.p + 0.5*k2r, cluster[0]) for cluster in clusters)
			k3r = P1.v * k2v * 0.5
			k4v = G * sum(cluster[1] * self._invrsquared(star.p + k3r, cluster[0]) for cluster in clusters)
			k4r = P1.v * k3v
			# Compute Runge Kutta final steps (save for later)
			v_inc += (k1v + 2*k2v + 2*k3v + k4v) / 6.0
			p_inc += (k1r + 2*k2r + 2*k3r + k4r) / 6.0
			save_for_later.append(dict(star=star, v_inc=v_inc, p_inc=p_inc))
		# Modify particles' attributes
		for save in save_for_later:
			save.star.p += save.p_inc
			save.star.v += save.v_inc


	#######################
	### Private Methods ###
	#######################	
	def _invrsquared(self, p1, p2):
		""" 
		Returns vector gravitation on p1 from p2 = (p2 - p1) / r^3 
		CONSTANTS G, M NOT TAKEN INTO ACCOUNT!!
		"""
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
