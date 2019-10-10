
from flask import *
from json import *
from tulip import tlp
import requests


app = Flask("Mon serveur")


@app.route('/')
def test():
         return render_template("accueil.html")


@app.route('/affiche')
def aff():
         return render_template("mongraphe.html")


@app.route('/graph')
def generate_graph():

         graph=tlp.newGraph()

         comic = graph.getStringProperty("comic")
         hero = graph.getStringProperty("hero")
         type_ = graph.getStringProperty("type")
         viewBorderColor = graph.getColorProperty("viewBorderColor")
         viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
         viewColor = graph.getColorProperty("viewColor")
         viewFont = graph.getStringProperty("viewFont")
         viewFontSize = graph.getIntegerProperty("viewFontSize")
         viewIcon = graph.getStringProperty("viewIcon")
         viewLabel = graph.getStringProperty("viewLabel")
         viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
         viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
         viewLabelColor = graph.getColorProperty("viewLabelColor")
         viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
         viewLayout = graph.getLayoutProperty("viewLayout")
         viewMetric = graph.getDoubleProperty("viewMetric")
         viewRotation = graph.getDoubleProperty("viewRotation")
         viewSelection = graph.getBooleanProperty("viewSelection")
         viewShape = graph.getIntegerProperty("viewShape")
         viewSize = graph.getSizeProperty("viewSize")
         viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
         viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
         viewTexture = graph.getStringProperty("viewTexture")
         viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
         viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")

         #for n in graph.getNodes():
         #print(n)


         char_hash= {}
         comic_hash={}

         r = requests.get('https://gateway.marvel.com:443/v1/public/characters?nameStartsWith=Iron%20Man&limit=1&apikey=4dff50d15e38e094affa81c7191ac0bd', headers={'referer': 'localhost'})
         r2= requests.get('https://gateway.marvel.com:443/v1/public/characters/1009368/comics?limit=100&apikey=4dff50d15e38e094affa81c7191ac0bd', headers={'referer': 'localhost'})


         print("Code de retour=>",r.status_code)

         if r.status_code == 200:
                  data_reply = r.json() #on récupère un dictionnaire dont la structure est expliqué sur le site marvel
                  print("Nombre de personnages trouvé : ", len(data_reply["data"]["results"]));
                  for character in data_reply["data"]["results"]:
                           print("id personnage=>", character['id'], " xx nom personnage=>", character['name'])
         else:
                  print("Erreur de téléchargement")


         if r2.status_code == 200:
                  data_reply2 = r2.json() #on récupère un dictionnaire dont la structure est expliqué sur le site marvel




         viewLabel = graph.getStringProperty("viewLabel")

         type_node=graph.getStringProperty("Type")
         for character in data_reply["data"]["results"]:
                  n1=graph.addNode()
                  viewLabel[n1]=character["name"]
                  type_node[n1]="Personnage"
                  char_hash[character["name"]]=n1
                  viewColor[n1]=(0,0,255)



         for comic in data_reply2["data"]["results"]:
                  node=graph.addNode()
                  type_node[node]="Comic"
                  viewLabel[node]=comic["title"]
                  comic_hash[comic["title"]]=node

         for target in graph.getNodes() :
                  if type_node[target]=="Personnage":
                           source=target


         graph.addEdge(source,target)


         for comic in data_reply2["data"]["results"]:
                  for name in comic["characters"]["items"]:
                           if name["name"] in char_hash.keys():
                                    n=char_hash[name["name"]]
                           else:
                                    n=graph.addNode()
                                    viewLabel[n]=name["name"]
                                    type_node[n]="Personnage"
                                    viewColor[n]=(0,255,0)
                                    char_hash[name["name"]]=n

                           destination=comic_hash[comic["title"]]
                           graph.addEdge(n,destination)

         params=tlp.getDefaultPluginParameters('FM^3 (OGDF)', graph)
         params['Node Size']= viewSize
         params['Edge Length Property']= viewMetric
         params['result']= viewLayout
         graph.applyLayoutAlgorithm('FM^3 (OGDF)')

         #return graph

         gjson={'nodes':[],'links':[]}
         for n in graph.getNodes():
                  gjson['nodes'].append({'id':viewLabel[n],'group':type_node[n]})
         for e in graph.getEdges():
                  gjson['links'].append({'source':viewLabel[graph.source(e)],'target':viewLabel[graph.target(e)],'value':1})


         return json.dumps(gjson)



@app.route('/json')
def create_json():
    graph=generate_graph()
    gjson={'nodes':[],'links':[]}
    for n in graph.getNodes():
        gjson['nodes'].append({'id':viewLabel[n],'group':type_node[n]})
    for e in graph.getEdges():
        gjson['links'].append({'source':viewLabel[graph.source(e)],'target':viewLabel[graph.target(e)],'value':1})

    return json.dumps(gjson)










def open_json():
         with open('templates/graph.json') as json_data:
             data= json.load(json_data)

         print(data)





if __name__ == '__main__':
	app.run(host="127.0.0.1", port=5002,debug=True)
    #app.run(host="127.0.0.1",debug=True)
