#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class GMap:
    def __init__(self):
        """ 
        Constructor of GMap of degree=2
        """

        self.maxid = 0
        self.alphas = { 0 : {}, 1 : {}, 2 : {} }
        self.positions = {}

    def darts(self): 
        """ 
        Return a list of id representing the darts of the structure 
        """
        return self.alphas[0].keys()

    def alpha(self, degree, dart):
        """ Return the application of the alpha_deg on dart """
        return self.alphas[degree][dart]

    def alpha_composed(self, list_of_alpha_value, dart):
        """ 
        Return the application of a composition of alphas on dart 
        """
        if list_of_alpha_value == []:
            return dart
        else:
            return self.alpha_composed(list_of_alpha_value[:-1],self.alpha(list_of_alpha_value[-1],dart))
		
    def is_free(self, degree, dart):
        """ 
        Test if dart is free for alpha_degree (if it is a fixed point) 
        """
        return self.alpha(degree, dart) == dart

	def add_dart(self):
		""" 
		Create a new dart and return its id. 
		Set its alpha_i to itself (fixed points) 
		""
		dart = self.maxid
		self.maxid += 1
		for degree in self.alphas.keys():
			self.alphas[degree][dart] = dart
		return dart"""
		dart = self.maxid
		self.maxid += 1
		for degree in self.alphas.keys():
			self.alphas[degree]
		return dart
		

    def is_valid(self):
        """ 
        Test the validity of the structure. 
        Check that alpha_0 and alpha_1 are involutions with no fixed points.
        """
        are_involutions = True
        are_involutions = are_involutions and np.all([self.alpha(0, dart) != dart for dart in self.darts()])
        are_involutions = are_involutions and np.all([self.alpha_composed([0,0], dart) == dart for dart in self.darts()])
        are_involutions = are_involutions and np.all([self.alpha(1, dart) != dart for dart in self.darts()])
        are_involutions = are_involutions and np.all([self.alpha_composed([1,1], dart) == dart for dart in self.darts()])
        are_involutions = are_involutions and np.all([self.alpha_composed([0,2, 0, 2], dart) == dart for dart in self.darts()])
        
        return are_involutions

    def link_darts(self,degree, dart1, dart2): 
        """ 
        Link the two darts with a relation alpha_degree if they are both free.
        """
        if self.is_free(degree, dart1) and self.is_free(degree, dart2):
			self.alphas[degree][dart1] = dart2
			self.alphas[degree][dart2] = dart1

    def print_alphas(self):
        """ 
        Print for each dart, the value of the different alpha applications.
        """ 
        try:
            from colorama import Style, Fore
        except:
            print "Try to install colorama (pip install colorama) for a better-looking display!"
            for d in self.darts():
                print d," | ",self.alpha(0,d),self.alpha(1,d),self.alpha(2,d) # , self.get_position(d)
        else:
            print "d     α0  α1  α2"
            for d in self.darts():
                print d," | ",Fore.MAGENTA+str(self.alpha(0,d))," ",Fore.GREEN+str(self.alpha(1,d))," ",Fore.BLUE+str(self.alpha(2,d))," ",Style.RESET_ALL 
	
	
	def orbit(self, dart, list_of_alpha_value):
		""" 
		Return the orbit of dart using a list of alpha relation.
		Example of use : gmap.orbit(0,[0,1]).
		"""
		result = []
		marked = set([])
		toprocess = [dart]
		while len(toprocess) > 0:
			d = toprocess.pop(0)
			if not d in marked:
				result.append(d)
				marked.add(d)
				for degree in list_of_alpha_value:
					toprocess.append(self.alpha(degree, d))
					
	def elements(self, degree):
		""" 
        Return one dart per element of degree. For this, consider all darts as initial set S. 
        Take the first dart d, remove from the set all darts of the orbit starting from d and 
        corresponding to element of degree degree. Take then next element from set S and do the 
        same until S is empty. 
        Return all darts d that were used. 
        """
		elements = []
		darts = set(self.darts())
		
		list_of_alpha_value = range(3)
		list_of_alpha_value.remove(degree)
		while len(darts)  > 0:
			dart = darts.pop()
			elementi = self.orbit(dart, list_of_alpha_value)
			darts -= set(elementi)
			elements.append(dart)
			
		return elements
        
        
	"""
	PLONGEMENT GÉOMÉTRIQUE
	"""
	def get_embedding_dart(self, dart, propertydict):
		""" 
        Check if a dart of the orbit representing the vertex has already been 
        associated with a value in propertydict. If yes, return this dart, else
        return the dart passed as argument.
        """
		for d in self.orbit(dart, [1, 2]):
			if propertydict.has_key(d):
				return d
		return dart
		
	def get_position(self, dart):
		"""
        Retrieve the coordinates associated to the vertex &lt;alpha_1, alpha_2&gt;(dart) 
        """
        return self.positions.get(self.get_embedding_dart(dart, self.positions))
        
	def set_position(self, dart, position):
		"""
        Associate coordinates with the vertex &lt;alpha_1,alpha_2&gt;(dart)
        """
        self.positions[self.get_embedding_dart(dart, self.positions)] = position
        
	def sew_dart(self, degree, dart1, dart2, merge_attribute = True):
		"""
        Sew two elements of degree 'degree' that start at dart1 and dart2.
        Determine first the orbits of dart to sew and heck if they are compatible.
        Sew pairs of corresponding darts, and if they have different embedding 
        positions, merge them. 
        """
		if degree == 1:
			self.link_darts(degree, dart1, dart2)
		else:
			alpha_list = [0]
			orbit1 = self.orbit(dart1, alpha_list)
			orbit2 = self.orbit(dart2, alpha_list)
			if len(orbit1) != len(orbit2):
				raise ValueError('orbites incompatible', orbit1, orbit2)
			for dart1, dart2 in zip(orbit1, orbit2):
				self.link_darts(degree, dart1, dart2)
				if merge_attribute:
					dart1_em = self.get_embedding_dart(dart1, self.positions)
					dart2_em = self.get_embedding_dart(dart2, self.positions)
					if dart1_em in self.positions and dart2_em in self.positions:
						new_position = (slef.positions[dart1_em] + self.positions[dart2_em]) / 2
						del self.positions[dart2_em]
						self.positions[dart1_em] = new_position
						
	
	def element_center(self, dart, degree):
		list_of_alpha_value = range(3)
		list_of_alpha_value.remove(degree)
		return np.mean([self.get_position(d) for d in self.orbit(dart,list_of_alpha_value)])


	def dart_display(self, radius=0.1, coef=0.8, add=False):
		import openalea.plantgl.all as pgl

		sphere = pgl.Sphere(radius,slices=16,stacks=16)
		coal = pgl.Material(ambient=(8,10,13),diffuse=3.,specular=(89,89,89),shininess=0.3)
		purple = pgl.Material(ambient=(72,28,72),diffuse=2.,specular=(89,89,89),shininess=0.3)
		green = pgl.Material(ambient=(0,88,9),diffuse=2.,specular=(89,89,89),shininess=0.3)
		blue = pgl.Material(ambient=(9,0,88),diffuse=2.,specular=(89,89,89),shininess=0.3)

		s = pgl.Scene()

		dart_points = {}
		for dart in self.darts():
			dart_point = self.get_position(dart)
			dart_face_center = self.element_center(dart,2)
			dart_edge_center = self.element_center(dart,1)

			dart_face_point = dart_face_center + coef*(dart_point-dart_face_center)
			dart_face_edge_center = dart_face_center + coef*(dart_edge_center-dart_face_center)

			dart_edge_point = dart_face_edge_center + coef*(dart_face_point-dart_face_edge_center)
			dart_middle_edge_point = dart_face_edge_center + 0.33*(dart_edge_point-dart_face_edge_center)

			dart_points[dart] = [dart_edge_point,dart_middle_edge_point]

			s += pgl.Shape(pgl.Translated(dart_points[dart][0],sphere),coal)
			s += pgl.Shape(pgl.Polyline(dart_points[dart],width=2),coal)

		for dart in self.darts():
			alpha_0_points = []
			alpha_0_points += [dart_points[dart][1]]
			alpha_0_points += [dart_points[self.alpha(0,dart)][1]]
			s += pgl.Shape(pgl.Polyline(alpha_0_points,width=5),purple)

			alpha_1_points = []
			alpha_1_points += [0.66*dart_points[dart][0] + 0.33*dart_points[dart][1]]
			alpha_1_points += [0.66*dart_points[self.alpha(1,dart)][0] + 0.33*dart_points[self.alpha(1,dart)][1]]
			s += pgl.Shape(pgl.Polyline(alpha_1_points,width=5),green)

			alpha_2_points = []
			alpha_2_points += [0.33*dart_points[dart][0] + 0.66*dart_points[dart][1]]
			alpha_2_points += [0.33*dart_points[self.alpha(2,dart)][0] + 0.66*dart_points[self.alpha(2,dart)][1]]
			s += pgl.Shape(pgl.Polyline(alpha_2_points,width=5),blue)

		if add : 
			pgl.Viewer.add(s)
		else : 
			pgl.Viewer.display(s)

	def display(self, color = (190,205,205), add = False):
    """
    Display the 2-cells of a 2-G-Map using the ordered orbit of its darts in PlantGL.
    For each face element, retrieve the position of its ordered face darts and add a FaceSet PlantGL object to the scene.
    Example : s += pgl.Shape(pgl.FaceSet( [[0,0,0],[1,0,0],[1,1,0],[0,1,0]], [[0,1,2,3]]) , pgl.Material((0,100,0))) # for a green square
    """
	
	def oderedorbit(self, dart, list_of_alpha_value):
		 """
        Return the ordered orbit of dart using a list of alpha relations by applying
        repeatingly the alpha relations of the list to dart.
        Example of use. gmap.orderedorbit(0,[0,1]).
        Warning: No fixed point for the given alpha should be contained.
        """
        orbit = []
        current_dart = dart
        current_alpha_degree = 0
        nbr_alpha = len(list_of_alpha_value)
        while( current_dart != dart) or orbit == []:
			orbit.append(current_dart)
			current_alpha = list_of_alpha_value[current_alpha_degree]
			current_dart = self.alpha(current_alpha, current_dart)
			current_alpha_degree = (current_alpha_degree+1) % nbr_alpha
		return orbit
        
	def eulercharacteristic(self):
	"""
	Compute the Euler-Poincare characteristic of the subdivision
	"""
	
	
	def dual(self):
	"""
	Compute the dual of the object
	Create a new GMap object with the same darts but reversed alpha relations
	Update the positions of the dual 0-cells as the centers of the 2-cells
	"""    
        
        
        
        
        
        
        
        
        
        
        
        
