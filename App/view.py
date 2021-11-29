﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
import threading
from DISClib.ADT import map as m
from DISClib.ADT import stack
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de aeropuertos")
    print('3- Encontrar puntos de interconexión aérea')
    print('4- Encontrar clústeres de tráfico aéreo')
    print('5- Encontrar la ruta más corta entre ciudades')
    print('6- Utilizar las millas de viajero')
    print('7- Cuantificar el efecto de un aeropuerto cerrado')
    print('8- Comparar con servicio WEB externo')
    print('9- Visualizar gráficamente los requerimientos')
    print('0- Salir')


catalog = None

def printReq1(respuesta):
    print("Aeropuertos que sirven como punto de interconexión a más rutas aereas")
    print("Grafo Dirigido")
    print(respuesta[0])
    print("------------------------------------------------------")
    print("Grafo No Dirigido")
    print(respuesta[1])

def printReq2(total_clusters, aeropuertos_mismo, IATA1, IATA2):

    print('El número total de clusters dentro de la red de tráfico aéreo encontrados es de ' + str(total_clusters) + ' clusters.\n')
    
    if aeropuertos_mismo == True :

        print('El aeropuerto identificado por el IATA ' + str(IATA1) + ' y el identificado por el IATA ' + str(IATA2) + ' SI pertenecen al mismo cluster.')

    else:

        print('El aeropuerto identificado por el IATA ' + str(IATA1) + ' y el identificado por el IATA ' + str(IATA2) + ' NO pertenecen al mismo cluster.')


"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            print("Inicializando ....")

            analyzer = controller.init()

        elif int(inputs[0]) == 2:

            print('Cargando información de aeropuertos en el mundo...')

            controller.loadData(analyzer)

            clusters = controller.getcluster(analyzer)

           
            num_airportsD = gr.numVertices(analyzer['AirportRoutesD'])
            num_airportsND = gr.numVertices(analyzer['AirportRoutesND'])

            print('Total de vértices del grafo dirigido: ' + str(num_airportsD))
            print('Total de vértices del grafo no dirigido: ' + str(num_airportsND) + '\n')

            num_routesD = gr.numEdges(analyzer['AirportRoutesD'])
            num_routesND = gr.numEdges(analyzer['AirportRoutesND'])

            print('Total de arcos del grafo dirigido: ' + str(num_routesD))
            print('Total de arcos del grafo no dirigido: ' + str(num_routesND) + '\n')

        
            num_ciudades = lt.size(analyzer['Cities_lst'])

            print('Total de ciudades cargadas: ' + str(num_ciudades) + '\n')

            airport_mapa = analyzer['AirportIATAS']
            city_map = analyzer['CitiesMapInfo']

            airportDs = gr.vertices(analyzer['AirportRoutesD'])
            first_airportD = lt.getElement(airportDs, 1)

            airport_infoD = m.get(airport_mapa, first_airportD)

            #grafo no dirigido

            print('\n A continuación se muestra la información del primer aeropuerto cargado para el grafo dirigido y no dirigido respectivamente: \n')
            print('Nombre: ' + airport_infoD['value']['Name'] + ', Ciudad: ' + airport_infoD['value']['City'] + ', Pais: ' + airport_infoD['value']['Country'] + ', Latitud: ' + airport_infoD['value']['Latitude'] + ', Longitud: ' + airport_infoD['value']['Longitude'] )
            
            #grafo no dirigido

            city_last = lt.getElement(analyzer['Cities_lst'], num_ciudades)

            print('\n A continuación se muestra la información de la última ciudad cargada: \n')

            print('Nombre: ' + city_last['city'] + ', Población: ' + city_last['population'] + ', Latitud: ' + city_last['lat'] + ', Longitud: ' + city_last['lng'])

        elif int(inputs[0]) == 3:
            'Requerimiento 1: interconecciones'

            respuesta = controller.getInterconnections(analyzer)
            printReq1(respuesta)
        
        elif int(inputs[0]) == 4:

            'Requerimiento 2: clusters de tráfico aéreo'

            IATA1 = (input('Primer aeropuerto a consultar (código IATA): ')).upper
            IATA2 = (input('Segundo aeropuerto a consultar (código IATA): ')).upper

            cluster_respuesta = controller.getTraficClusters(clusters, IATA1, IATA2)

            printReq2(cluster_respuesta[0],cluster_respuesta[1], IATA1, IATA2)

    
        elif int(inputs[0]) == 5:
            pass

        elif int(inputs[0]) == 6:
            pass

        elif int(inputs[0]) == 7:
            pass

        elif int(inputs[0]) == 8:
            pass

        elif int(inputs[0]) == 9:
            pass

        elif int(inputs[0]) == 0:
            sys.exit(0)
            
        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
