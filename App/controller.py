"""
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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


def loadData(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    loadAirport(analyzer)
    loadRoutes(analyzer)
    loadCities(analyzer)

    return analyzer

def loadAirport(analyzer):

    airportfile = cf.data_dir + '/Skylines/airports_full.csv'
    input_file = csv.DictReader(open(airportfile, encoding="utf-8"),
                                delimiter=",")

    for airport in input_file:

        model.addAirportVertex(analyzer, airport)


def loadRoutes(analyzer):

    routesfile = cf.data_dir + '/Skylines/routes_full.csv'
    input_file = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    for route in input_file:
            model.addAirportConnection(analyzer, route)


def loadCities(analyzer):

    citiesfile = cf.data_dir + '/Skylines/worldcities.csv'
    input_file = csv.DictReader(open(citiesfile, encoding="utf-8"),
                                delimiter=",")

    for city in input_file:

        model.addAirportCity(analyzer, city)


# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def getcluster(analyzer):

    return model.getcluster(analyzer)

def getTraficClusters(cluster, IATA1,IATA2):

    return model.getTraficClusters(cluster, IATA1,IATA2)


def getAffectedAirports(analyzer, IATA):

    return model.getAffectedAirports(analyzer, IATA)

def getCities(analyzer, name):

    return model.getCities(analyzer, name)
