﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """




import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from math import radians, cos, sin, asin, sqrt
assert config


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador


   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'AirportIATAS': None,
                    'AirportRoutesD': None,
                    'AirportRoutesND': None,
                    'AirportCities': None,
                    'CitiesMapInfo': None,
                    'Cities-ID': None
                    }
        analyzer['AirportIATAS'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareAirportIATA)

        analyzer['AirportRoutesD'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareAirportIATA)

        analyzer['AirportRoutesND'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareAirportIATA)

        analyzer['AirportCities'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareAirportIATA)

        analyzer['Cities_lst'] = lt.newList('ARRAY_LIST')

        analyzer['CitiesMapInfo'] = m.newMap(numelements=5000,
                                     maptype='PROBING',
                                     comparefunction=compareAirportIATA)

        analyzer['Cities-ID'] = m.newMap(numelements=5000,
                                     maptype='PROBING',
                                     comparefunction=compareCityName)


        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo

def addAirportVertex(analyzer, airport):

    airport1 = formatVertex(airport)

    map = analyzer['AirportIATAS']

    entry = m.get(map, airport['IATA'])

    if entry is None:
        m.put(map, airport['IATA'], airport)

    if not gr.containsVertex(analyzer['AirportRoutesD'], airport1):
        gr.insertVertex(analyzer['AirportRoutesD'], airport1)


    return analyzer


def addAirportConnection(analyzer, route):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    origin = route['Departure']
    destination = route['Destination']

    cleanDistance(route['distance_km'])
    distance = float(route['distance_km'])
    distance = abs(distance)
    addConnection(analyzer['AirportRoutesD'], origin, destination, distance)
    addAirportNDConnection(analyzer,origin,destination,distance)

def addAirportNDConnection(analyzer,origin,destination,distance): 

    arco_origin = gr.getEdge(analyzer['AirportRoutesD'],origin,destination)
    arco_destination = gr.getEdge(analyzer['AirportRoutesD'],destination,origin)

    if arco_origin != None and arco_destination != None:
        if not gr.containsVertex(analyzer['AirportRoutesND'], origin):
            gr.insertVertex(analyzer['AirportRoutesND'], origin)

        if not gr.containsVertex(analyzer['AirportRoutesND'], destination):
            gr.insertVertex(analyzer['AirportRoutesND'], destination)

        addConnection(analyzer['AirportRoutesND'], origin, destination, distance)

    
    return analyzer

def addAirportCity(analyzer, city):

    city_map = analyzer['CitiesMapInfo']
    city_id_map = analyzer['Cities-ID']

    entry = m.get(city_map,int(city['id']))

    if entry == None:

        m.put(city_map, int(city['id']), city)

    lt.addLast(analyzer['Cities_lst'], city)

    citynamentry = m.get(city_id_map,city['city'])

    if citynamentry == None:

        value = newCity()
        m.put(city_id_map, city['city'], value)

    else: 

        value = me.getValue(citynamentry)

    lt.addLast(value['ID'], city)
    
    return analyzer

def newCity():

    city = {'ID':lt.newList('ARRAY_LIST', cmpID)}   

    return city

def addConnection(graph, origin, destination, distance):

    ' Adiciona un arco entre dos aeropuertos'

    arco = gr.getEdge(graph,origin, destination)

    if arco is None:

        gr.addEdge(graph,origin, destination, distance)

    return graph


# Funciones para creacion de datos

def cleanDistance(distance):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if distance == '':
        distance = 0


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['IATA']
    return name

def harvesineDistance(lat1, lat2, lon1, lon2):

    R = 6371 #radio de la tierra en km

    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2*asin(sqrt(a))

    return c * R



# Funciones de consulta

def getInterconnections(analyzer):
    graph = analyzer['AirportRoutesD']
    vertex_list = gr.vertices(graph) 
    info_list = lt.newList("ARRAY_LIST", cmpfunction=compareconnections)

    graphND = analyzer['AirportRoutesND']
    vertex_listND = gr.vertices(graphND) 
    info_listND = lt.newList("ARRAY_LIST", cmpfunction=compareconnections)

    
    for vertex in lt.iterator(vertex_list):
        arocos_llegada = gr.indegree(graph, vertex)
        arcos_salida = gr.outdegree(graph, vertex)
        total_arcos = arocos_llegada + arcos_salida
        datos = {"Aeropuerto": vertex, 
                "TotalConnections": total_arcos}
        lt.addLast(info_list, datos)

    for vertex in lt.iterator(vertex_listND):
        total_arcosND = gr.degree(graphND,vertex)
        datos = {"Aeropuerto": vertex, 
                "TotalConnections": total_arcosND}
        lt.addLast(info_listND, datos)

    return info_list, info_listND

def getCities(analyzer, name):

    entry = m.get(analyzer['Cities-ID'], name)
    value = me.getValue(entry)

    return value['ID']

def getcluster(analyzer):

    cluster = scc.KosarajuSCC(analyzer['AirportRoutesD'])

    return cluster

def getClusterNum(cluster):

    cluster_num = scc.connectedComponents(cluster)

    return cluster_num


def getTraficClustersCon(cluster, IATA1,IATA2):

    airports_connected = scc.stronglyConnected(cluster, IATA1, IATA2)

    return airports_connected

def ClosestairportCity():
    pass

def DijkstraAirport(analyzer, airport):

    shortest_routes = djk.Dijkstra(analyzer['AirportRoutesD'], airport)

    return shortest_routes


def getShortestRoute(dijkstra, airport2):

    if djk.hasPathTo(dijkstra,airport2):

        dijk_route = djk.pathTo(dijkstra,airport2)

        dist_total = djk.distTo(dijkstra, airport2)

        return dijk_route,dist_total


def getAffectedAirports(analyzer, IATA):

    adj = gr.adjacents(analyzer['AirportRoutesD'],IATA)

    size = lt.size(adj)

    return adj, size


# Funciones utilizadas para comparar elementos dentro de una lista
def compareAirport():
     pass

def compareCityName(name, key):

    namekey = key['key']
    if (name == namekey):
        return 0
    elif (name > namekey):
        return 1
    else:
        return -1

def compareAirportIATA(IATA, keyvalue):
    """
    Compara dos aeropuertos
    """
    IATAcode = keyvalue['key']
    if (IATA == IATAcode):
        return 0
    elif (IATA > IATAcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

def cmpID(ID1, ID2):

    if (ID1 == ID2):
        return 0
    else:
        return -1

def compareconnections():
    pass

# Funciones de ordenamiento

