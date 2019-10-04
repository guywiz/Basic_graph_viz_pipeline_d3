# -*- coding:utf-8 -*-

from flask import Flask, request

from model import model
from view import view

data_model = model.Model()
view = view.View()

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
	'''
	on charge un graphe
	dans un cas plus general il faudrait prendre en compte
	les donnees de formulaire (avec la methode POST)
	et calculer un (sous)graphe
	parmi toute une palette de possibilites
	'''
	graph = data_model.load_graph()

	'''
	on confie le graphe calcule a la vue qui sait traduire la donnee
	"brute" en un objet qui se prete au calcul de la vue cote client
	'''
	view.graph2json(graph)

	'''
	on envoie le resultat cote client
	'''
	return app.send_static_file('static_graph.html')

if __name__ == '__main__':
	app.run(debug=True)

