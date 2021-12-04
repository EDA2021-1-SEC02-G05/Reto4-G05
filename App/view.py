"""
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
from DISClib.DataStructures import mapentry as me
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
    print("Grafo Dirigido: A continuación se muestra el TOP 10\n")

    print(respuesta[0])
    print("------------------------------------------------------")
    print("Grafo No Dirigido")
    print(respuesta[1])
    #print(lt.isPresent(respuesta[1],{'Aeropuerto': 'VLD', 'TotalConnections': 1}))
    #print(lt.getElement(respuesta[1],3291))

def printReq2(total_clusters, aeropuertos_mismo, IATA1, IATA2):

    print('El número total de clusters dentro de la red de tráfico aéreo encontrados es de ' + str(total_clusters) + ' clusters.\n')
    
    if aeropuertos_mismo == True :

        print('El aeropuerto identificado por el IATA ' + str(IATA1) + ' y el identificado por el IATA ' + str(IATA2) + ' SI pertenecen al mismo cluster.')

    else:

        print('El aeropuerto identificado por el IATA ' + str(IATA1) + ' y el identificado por el IATA ' + str(IATA2) + ' NO pertenecen al mismo cluster.')

def printReq3(analyzer, ruta, distancia_total, aero_origen, aero_destino):

    aero_origen_entry = m.get(analyzer['AirportIATAS'], aero_origen)
    aero_origen_info = me.getValue(aero_origen_entry)
    aero_destino_entry = m.get(analyzer['AirportIATAS'], aero_destino)
    aero_destino_info = me.getValue(aero_destino_entry)

    print('A continuación se muestran los aeropuertos de origen y destino respectivamente y su información: \n')

    print('IATA: ' + aero_origen_info['IATA'] + ', Nombre: ' + aero_origen_info['Name'] + ', Ciudad: ' + aero_origen_info['City'] + ', Pais: ' + aero_origen_info['Country'])
    print('IATA: ' + aero_destino_info['IATA'] + ', Nombre: ' + aero_destino_info['Name'] + ', Ciudad: ' + aero_destino_info['City'] + ', Pais: ' + aero_destino_info['Country'] + '\n')

    print('La ruta más corta hallada entre ambos aeropuertos es de ' + str(distancia_total) + ' km. \n')
    print('A continuación se mostrará la ruta tomada con sus respectivas paradas y distancias parciales: \n')

    for trayecto in lt.iterator(ruta):
        print('Origen: ' + trayecto['vertexA'] + ', Destino: ' + trayecto['vertexB'] + ', Distancia (km): ' + str(trayecto['weight']) + '.')


def printReq5(lista, tamano, IATA):

    print('Si el aeropuerto identificado con el código IATA ' + str(IATA) + ' se encontrara fuera de servicio, ' + str(tamano) + ' aeropuertos se verían afectados.\n')

    print('A continuación se presenta la lista de aeropuertos que se verían afectados: ')

    for aero in lt.iterator(lista):

        print(aero)

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
            cluster_num = controller.getClusterNum(clusters)

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

            airportDs = gr.vertices(analyzer['AirportRoutesD'])
            first_airportD = lt.getElement(airportDs, 1)

            airport_infoD = m.get(airport_mapa, first_airportD)

            #grafo no dirigido

            print('\nA continuación se muestra la información del primer aeropuerto cargado para el grafo dirigido y no dirigido respectivamente: \n')
            print('Nombre: ' + airport_infoD['value']['Name'] + ', Ciudad: ' + airport_infoD['value']['City'] + ', Pais: ' + airport_infoD['value']['Country'] + ', Latitud: ' + airport_infoD['value']['Latitude'] + ', Longitud: ' + airport_infoD['value']['Longitude'] )
            
            #grafo no dirigido

            city_last = lt.getElement(analyzer['Cities_lst'], num_ciudades)

            print('\nA continuación se muestra la información de la última ciudad cargada:')

            print('Nombre: ' + city_last['city'] + ', Población: ' + city_last['population'] + ', Latitud: ' + city_last['lat'] + ', Longitud: ' + city_last['lng']+'\n')

        elif int(inputs[0]) == 3:

            'Requerimiento 1: interconecciones'

            respuesta = controller.getInterconnections(analyzer)
            printReq1(respuesta)
        
        
        elif int(inputs[0]) == 4:

            'Requerimiento 2: clusters de tráfico aéreo'

            IATA1 = input('Primer aeropuerto a consultar (código IATA): ')
            IATA2 = input('Segundo aeropuerto a consultar (código IATA): ')

            cluster_con = controller.getTraficClustersCon(clusters, IATA1, IATA2)

            printReq2(cluster_num,cluster_con, IATA1, IATA2)

        
        elif int(inputs[0]) == 5:

            'Requerimiento 3: Encontrar la ruta más corta entre ciudades'

            origen = input('Escoja la ciudad de origen: ')

            ciudades_o = controller.getCities(analyzer, origen)

            if lt.size(ciudades_o) > 1:

                print('Se encontraron los siguientes códigos de ciudades con el mismo nombre que usted seleccionó: ')

                for ciudad in lt.iterator(ciudades_o):

                    print(ciudad['city']+', '+ ciudad['country'] + ', ' + ciudad['lat'] + ', ' + ciudad['lng'] + ', ' + ciudad['id'])

                ciudad_o_codigo = input('De las anteriores ciudades, seleccione el código de la que quiere como ciudad de origen: ')

            else:

                ciudad_o_codigo = ciudades_o['elements'][0]['id']

            airport_origin = controller.ClosestairportCity(analyzer,ciudad_o_codigo)

            dijkstra_airport = controller.DijkstraAirport(analyzer, airport_origin)
            
            destino = input('Escoja la ciudad de destino: ')

            ciudades_d = controller.getCities(analyzer, destino)

            if lt.size(ciudades_d) > 1:

                print('Se encontraron los siguientes códigos de ciudades con el mismo nombre que usted seleccionó: ')
                for ciudad in lt.iterator(ciudades_d):

                    print(ciudad['city']+', '+ ciudad['country'] + ', ' + ciudad['lat'] + ', ' + ciudad['lng'] + ', ' + ciudad['id'])

                ciudad_d_codigo = input('De las anteriores ciudades, seleccione el código de la que quiere como ciudad de destino: ')
            else:

                ciudad_d_codigo = ciudades_d['elements'][0]['id']

            airport_destination = controller.ClosestairportCity(analyzer,ciudad_d_codigo)

            respuesta = controller.getShortestRoute(dijkstra_airport, airport_destination)

            printReq3(analyzer, respuesta[0],respuesta[1], airport_origin, airport_destination)


        elif int(inputs[0]) == 6:

            'Requerimiento 4: Utilizar las millas de viajero'
            pass

        elif int(inputs[0]) == 7:

            'Requerimiento 5: Cuantificar el efecto de un aeropuerto cerrado'

            IATA = input('Ingrese el código IATA del aeropuerto a consultar: ')

            afectados = controller.getAffectedAirports(analyzer, IATA)

            printReq5(afectados[0], afectados[1], IATA)

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
