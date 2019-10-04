# -*- coding:utf-8 -*-

import configparser
from tulip import *
import math
import json

class View(object):
	"""docstring for View"""
	def __init__(self):
		super(View, self).__init__()		
		self.config = configparser.ConfigParser()
		self.config.read('app/webapp.ini')
		self.store_path = self.config.get('view', 'store_path')

	def center_graph(self, graph):
		'''
		translates x, y coords of nodes so bounding box
		sits in a box with bottom left point (0,0)
		and top right (w, h)
		'''
		print([graph['viewLayout'][n].getX() for n in graph.getNodes()])
		print([graph['viewLayout'][n].getY() for n in graph.getNodes()])
		box = tlp.computeBoundingBox(graph)
		w = box.width()
		h = box.height()
		print('Box W: ', w, ' H: ', h)
		c = box.center()
		cx = c.getX()
		cy = c.getY()
		for n in graph.getNodes():
			xn = graph['viewLayout'][n].getX()
			yn = graph['viewLayout'][n].getY()
			X = (xn - cx + w/2)
			Y = yn - cy + h/2
			graph['viewLayout'][n] = tlp.Coord(X, Y, 0.0)
		return w, h

	def graph2json(self, graph):
		json_object = {}
		size = graph['viewSize']
		label = graph['viewLabel']
		width, height = self.center_graph(graph)
		layout = graph['viewLayout']
		json_object['bbox'] = {'width': width, 'height': height}

		nodes = []
		for n in graph.getNodes():
			nodes.append({'index': n.id, 'size': math.sqrt(size[n].getX()**2 + size[n].getY()**2), 'name': label[n], 'x': layout[n].getX(), 'y': layout[n].getY()})	
		json_object['nodes'] = nodes
		links = []
		for e in graph.getEdges():
			links.append({'source': graph.source(e).id, 'target': graph.target(e).id})
		json_object['links'] = links
		with open('static/static_graph.json', 'w') as fp:
			json.dump(json_object, fp)
