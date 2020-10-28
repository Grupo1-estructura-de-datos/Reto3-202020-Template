"""
 * Copyright 2020, Departamento de sistemas y Computación
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from App import controller
assert config
import datetime
from DISClib.ADT import queue as qe

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Añadir nueva información de accidentes")
    print("3- Conocer los accidentes en una fecha (REQ1)")
    print("4- Consultar accidentes anteriores a una fecha (REQ2)")
    print("5- Consultar accidentes en un rango de fechas (REQ3)")
    print("6- Conocer el estado con mas accidentes (REQ4)")
    print("7- Conocer los accidentes por rango de horas (REQ5)")
    print("8- Conocer la zona geográfica mas accidentada (REQ6)")
    print("0- Salir")
    print("*******************************************")

# ___________________________________________________
#  Funciones para imprimir la inforamación de
#  respuesta.  La vista solo interactua con
#  el controlador.
# ___________________________________________________

def ImprimirEnConsola(cola, DatosAdicionales=None):
    if qe.isEmpty(cola)==False: 
        Centinela = True
        print("-"*100)
        while Centinela==True:
            print("", end=" "*10)
            print("•" + qe.dequeue(cola))
            if qe.isEmpty(cola)==True: Centinela=False
        print("-"*100)
    else: print("No se encontrar peliculas para el criterio")
    if DatosAdicionales!=None:
        if qe.isEmpty(DatosAdicionales)==False:
            CentinelaAdicionales = True
            while CentinelaAdicionales==True:
                dato = qe.dequeue(DatosAdicionales)
                print(str(dato[0])+str(dato[1]))
                if qe.isEmpty(DatosAdicionales)==True: CentinelaAdicionales=False

"""
Menu principal
"""
while True:
    try:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs) == 0:
            print("\nHasta pronto!")
            break

        if int(inputs) == 1:
            print("\nInicializando....")
            # cont es el controlador que se usará de acá en adelante
            cont = controller.init()

        elif int(inputs) == 2:
            archivo = (input("Por favor añada el nombre del archivo que se quiere añadir a la base de datos que se analiza: "))
            print("\nCargando información de accidentes ....")
            controller.loadData(cont, archivo)
            total = str(controller.crimesSize(cont))
            print('Crimenes cargados: ' + total)
            print('Altura del arbol: ' + str(controller.indexHeight(cont)))
            print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
            print('Menor Llave: ' + str(controller.minKey(cont)))
            print('Mayor Llave: ' + str(controller.maxKey(cont)))

        elif int(inputs) == 3:
            print("\nBuscando accidentes en una fecha: ")
            initialDate = input("Fecha (YYYY-MM-DD): ")
            initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d').date()
            cola=controller.f3(cont,initialDate)
            ImprimirEnConsola(cola)

        elif int(inputs) == 4:
            print("\nBuscando accidentes antes de una fecha: ")
            initialDate = input("Fecha (YYYY-MM-DD): ")
            initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d').date()
            cola=controller.f4(cont,initialDate)
            ImprimirEnConsola(cola)

        elif int(inputs) == 5:
            print("\nBuscando accidentes en rango de fechas: ")
            initialDate = input("Fecha Inicial (YYYY-MM-DD): ")
            finalDate = input("Fecha Final (YYYY-MM-DD): ")
            initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d').date()
            finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d').date()
            cola=controller.f5(cont,initialDate,finalDate)
            ImprimirEnConsola(cola)

        elif int(inputs) == 6:
            print("\nBuscando el estado con más accidentes: ")
            initialDate = input("Fecha Inicial (YYYY-MM-DD): ")
            finalDate = input("Fecha Final (YYYY-MM-DD): ")
            initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d').date()
            finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d').date()
            cola=controller.f6(cont,initialDate,finalDate)
            ImprimirEnConsola(cola)

        elif int(inputs) == 7:
            print("\nBuscando accidentes en rango de horas: ")
            initialDate = input("Hora Inicial (HH:MM): ")
            initialDate = "1900-01-01 " + initialDate
            finalDate = input("Hora Final (HH:MM): ")
            finalDate = "1900-01-01 " + finalDate
            initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d %H:%M').time()
            finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d %H:%M').time()
            cola=controller.f7(cont,initialDate,finalDate,int(total))
            ImprimirEnConsola(cola)

        elif int(inputs) == 8:
            print("\nBuscando accidentes en rango de busqueda: ")
            lat1 = float(input("Ingrese la latitud inicial: "))
            lon1 = float(input("Ingrese la longitud inicial: "))
            r = int(input("Ingrese el radio de busqueda (en millas): "))
            cola=controller.f8(cont,lat1,lon1,r)
            ImprimirEnConsola(cola)
    except:
        print("\nAlgo ocurrió mal, asegurese que todo esté bien e intente nuevamente: ")
sys.exit(0)