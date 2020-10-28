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

import config as cf
from App import model
import datetime
import csv
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.ADT import queue
from scipy import stats as statistics
"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, crimesfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    crimesfile = cf.data_dir + crimesfile
    input_file = csv.DictReader(open(crimesfile, encoding="utf-8"),
                                delimiter=",")
    for crime in input_file:
        model.addCrime(analyzer, crime)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def crimesSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.crimesSize(analyzer)

def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)

def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)

def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)

def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)

def f3(cont,initialDate):
    accidentesFecha=model.entryFecha(cont,initialDate)
    cola=queue.newQueue()
    severidadesL = m.keySet(accidentesFecha)
    severidadesV = m.valueSet(accidentesFecha)
    itesevL=it.newIterator(severidadesL)
    itesevV=it.newIterator(severidadesV)
    while it.hasNext(itesevL):
        llave=str(it.next(itesevL))
        valor=str(lt.size(it.next(itesevV)["lstoffenses"]))
        valor=("Hay " + valor + " accidentes para la severidad " + llave + " en el día dado.")
        queue.enqueue(cola,valor)
    return cola

def f4(cont,initialDate):
    accidentesFechaAntes=model.entryFechaAntes(cont,initialDate)
    cola=queue.newQueue()
    suma=0
    maxim=0
    díaMax=None
    iteradorAFA=it.newIterator(accidentesFechaAntes)
    while it.hasNext(iteradorAFA):
        entry=it.next(iteradorAFA)
        N=lt.size(entry["lstcrimes"])
        if N>maxim:
            maxim=N
            díaMax = datetime.datetime.strptime(lt.getElement(entry["lstcrimes"],0)["Start_Time"], '%Y-%m-%d %H:%M:%S').date()
        suma+=N
    texto=("En total se reportaron " + str(suma) + " accidentes previos a la fecha")
    queue.enqueue(cola,texto)
    texto=("La fecha con más accidentes fue " + str(díaMax))
    queue.enqueue(cola,texto)
    return cola

def f5(cont,initialDate,finalDate):
    accidentesEntreFechas=model.EntreFechas(cont,initialDate,finalDate)
    return f5f6(accidentesEntreFechas,"En total se reportaron "," accidentes entre las fechas indicadas","La categoria de severidad con más accidentes fue la categoría ")

def f6(cont,initialDate,finalDate):
    accidentesEntreFechas=model.EntreFechas2(cont,initialDate,finalDate)
    return f5f6(accidentesEntreFechas,None,None,"El estado en el que más accidentes se presentaron fue: ")

def f7(cont,initialDate,finalDate,total):
    accidentesEntreHoras=model.EntreHoras(cont,initialDate,finalDate)
    cola=queue.newQueue()
    sevs=[0]*10
    suma=0
    iteradorAEH=it.newIterator(accidentesEntreHoras)
    while it.hasNext(iteradorAEH):
        entry=it.next(iteradorAEH)
        N=lt.size(entry["lstcrimes"])
        offenseIndex=entry["offenseIndex"]
        severidadesL = m.keySet(offenseIndex)
        severidadesV = m.valueSet(offenseIndex)
        itesevL=it.newIterator(severidadesL)
        itesevV=it.newIterator(severidadesV)
        while it.hasNext(itesevL):
            llave=int(it.next(itesevL))
            valor=lt.size(it.next(itesevV)["lstoffenses"])
            sevs[llave]+=valor
        suma+=N
    queue.enqueue(cola,("En total hubo " + str(suma) + " accidentes en el rango horario solicitado"))
    ñ=0
    while ñ<len(sevs):
        if sevs[ñ]!=0:
            queue.enqueue(cola,("Se presentaron " + str(sevs[ñ]) + " accidentes de severidad " + str(ñ)))
        ñ+=1
    porcentaje = round((suma/total)*100,2)
    queue.enqueue(cola,("Estos accidentes constituyen el " + str(porcentaje) +  """%""" + " del total de accidentes"))
    return cola

def f8 (cont,lat1,lon1,r):
    cola=queue.newQueue()
    iterador = it.newIterator(cont["crimes"])
    dias_semana = [0,0,0,0,0,0,0]
    while it.hasNext(iterador):
        DiccionarioOrdenado = it.next(iterador)
        lat2 = float(DiccionarioOrdenado["Start_Lat"])
        lon2 = float(DiccionarioOrdenado["Start_Lng"])
        distancia = model.distance(lat1,lat2,lon1,lon2)
        if distancia<r:
            dia =  datetime.datetime.strptime(DiccionarioOrdenado["Start_Time"], '%Y-%m-%d %H:%M:%S').weekday()
            dias_semana[dia]+=1
    semana = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

    k=0
    for i in dias_semana:
        if dias_semana[k]!=0:
            texto="El día " + str(semana[k]) + " hubo " +  str(dias_semana[k]) + " accidentes"
            queue.enqueue(cola,texto)
        k+=1
    texto="En total se presentaron " + str(sum(dias_semana)) + " accidentes en el radio de busqueda"
    queue.enqueue(cola,texto)
    return cola

def f5f6 (accidentesEntreFechas,t11,t12,t21):
    cola=queue.newQueue()
    suma=0
    cats=[]
    iteradorAEF=it.newIterator(accidentesEntreFechas)
    while it.hasNext(iteradorAEF):
        entry=it.next(iteradorAEF)
        offenseIndex=entry["offenseIndex"]
        N=lt.size(entry["lstcrimes"])
        severidadesL = m.keySet(offenseIndex)
        severidadesV = m.valueSet(offenseIndex)
        itesevL=it.newIterator(severidadesL)
        itesevV=it.newIterator(severidadesV)
        while it.hasNext(itesevL):
            llave=it.next(itesevL)
            valor=lt.size(it.next(itesevV)["lstoffenses"])
            nuevaL=[llave]*valor
            cats.extend(nuevaL)
        suma+=N
    if not (t11==None or t12==None):
        texto=(t11 + str(suma) + t12)
        queue.enqueue(cola,texto)
    texto=(t21 + str(statistics.mode(cats)[0][0]))
    queue.enqueue(cola,texto)
    return cola