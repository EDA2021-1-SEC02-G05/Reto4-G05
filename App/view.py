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
    print("2- Cargar información de buses de singapur")
    print('3- Encontrar puntos de interconexión aérea')
    print('4- Encontrar clústeres de tráfico aéreo')
    print('5- Encontrar la ruta más corta entre ciudades')
    print('6- Utilizar las millas de viajero')
    print('7- Cuantificar el efecto de un aeropuerto cerrado')
    print('8- Comparar con servicio WEB externo')
    print('9- Visualizar gráficamente los requerimientos')
    print('0- Salir')


catalog = None

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
            num_airportsD = gr.numVertices(analyzer['AirportRoutesD'])
            num_airportsND = gr.numVertices(analyzer['AirportRoutesND'])

            num_routesD = gr.numEdges(analyzer['AirportRoutesD'])
            num_routesND = gr.numEdges(analyzer['AirportRoutesND'])

            #TODO: TOTAL CIUDADES

            #first_airportD
            #first_airportND
            #last_city


        elif int(inputs[0]) == 3:
            pass
        
        elif int(inputs[0]) == 4:
            pass

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
