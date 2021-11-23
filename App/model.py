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
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
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
                    'Connections': None,
                    'AirportRoutesD': None,
                    'AirportRoutesND': None,
                    'AirportCities': None
                    }
        analyzer['Connections'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareAirportIATA)

        analyzer['AirportRoutesD'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareAirport)

        analyzer['AirportRoutesND'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareAirport)
        analyzer['AirportCities'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareAirport)


        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo

def addAirportVertex(analyzer, airport):

    if not gr.containsVertex(analyzer['AirportRoutesD'], airport):
        gr.insertVertex(analyzer['AirportRoutesD'], airport)

    if not gr.containsVertex(analyzer['AirportRoutesND'], airport):
        gr.insertVertex(analyzer['AirportRoutesND'], airport)

    if not gr.containsVertex(analyzer['AirportCities'], airport):
        gr.insertVertex(analyzer['AirportCities'], airport)

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


    origin = formatVertex(route['Departure'])
    destination = formatVertex(route['Destination'])
    cleanDistance(route['Departure'], route['Destination'])
    distance = float(route['distance_km'])
    distance = abs(distance)
    addConnection(analyzer['AirportRoutesD'], origin, destination, distance)

    #addConnection(analyzer['AirportRoutesND'], origin, destination, distance) #ESO YA HACE SOLO CONEXIONES ENTRE COMPONENTES QUE TENGA IDA Y VENIDA?

    return analyzer

def addAirportCity(analyzer, city):



    pass

def addConnection(graph, origin, destination, distance):

    ' Adiciona un arco entre dos aeropuertos'

    arco = gr.getEdge(graph,origin, destination)

    if arco is None:

        gr.addEdge(graph,origin, destination, distance)

    return graph


# Funciones para creacion de datos

def cleanDistance(origin, destination):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if origin['Distance'] == '':
        origin['Distance'] = 0
    if destination['Distance'] == '':
        destination['Distance'] = 0

def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['Name'] + '-'
    name = name + service['IATA']
    return name


# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compareAirport():
     pass

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
# Funciones de ordenamiento
