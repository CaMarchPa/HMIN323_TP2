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
        
        while len(dart)  > 0:
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
