# -*- coding:utf-8 -*-

from flask import Flask, request
from tulip import *
import configparser

class Model(object):
	"""docstring for Model"""
	def __init__(self):
		super(Model, self).__init__()
		self.config = configparser.ConfigParser()
		self.config.read('app/webapp.ini')
		self.model_path = self.config.get('data', 'path')

	def load_graph(self):
		'''
		on va chercher un sous-graphe
		(ici, on fait simple, on ne fait que charger le graphe depuis un fichier)
		'''
		graph = tlp.loadGraph(self.model_path)

		'''
		on peut ensuite pensee a tout un tas de traitements
		a faire sur les donnees,
		acceder a des donnees annexes pour enrichir le graphe
		lancer des algorithmes sur le graphe, etc.
		'''
		params = tlp.getDefaultPluginParameters('GEM (Frick)', graph)
		graph.applyLayoutAlgorithm('GEM (Frick)', params)
		params = tlp.getDefaultPluginParameters('Size Mapping', graph)
		params['min size'] = 1
		params['max size'] = 3
		graph.applySizeAlgorithm('Size Mapping', params)
		return graph

		
		