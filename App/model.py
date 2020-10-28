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
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
from math import radians, cos, sin, asin, sqrt 
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

Se define la estructura de un catálogo de libros.
El catálogo tendrá  una lista para los libros.

Los autores, los tags y los años se guardaran en
tablas de simbolos.
"""

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------


def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'crimes': None,
                'dateIndex': None,
                'dateIndex2': None,
                'hourIndex': None
                }

    analyzer['crimes'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['dateIndex2'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['hourIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer


# Funciones para agregar informacion al catalogo


def addCrime(analyzer, crime):
    """
    """
    lt.addLast(analyzer['crimes'], crime)
    updateDateIndex(analyzer['dateIndex'], crime)
    updateDateIndex2(analyzer['dateIndex2'], crime)
    updateHourIndex(analyzer['hourIndex'], crime)
    return analyzer


def updateDateIndex(map, crime):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = crime['Start_Time']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, crimedate.date())
    if entry is None:
        datentry = newDataEntry(crime)
        om.put(map, crimedate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, crime)
    return map

def updateDateIndex2(map, crime):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = crime['Start_Time']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, crimedate.date())
    if entry is None:
        datentry = newDataEntry(crime)
        om.put(map, crimedate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex2(datentry, crime)
    return map

def updateHourIndex(map, crime):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = crime['Start_Time'][-8:-3]
    occurreddate = "1900-01-01 " + occurreddate
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M')
    entry = om.get(map, crimedate.time())
    if entry is None:
        datentry = newDataEntry(crime)
        om.put(map, crimedate.time(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, crime)
    return map

def addDateIndex(datentry, crime):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstcrimes']
    lt.addLast(lst, crime)
    offenseIndex = datentry['offenseIndex']
    offentry = m.get(offenseIndex, crime['Severity'])
    if (offentry is None):
        entry = newOffenseEntry(crime['Severity'], crime)
        lt.addLast(entry['lstoffenses'], crime)
        m.put(offenseIndex, crime['Severity'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstoffenses'], crime)
    return datentry

def addDateIndex2(datentry, crime):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstcrimes']
    lt.addLast(lst, crime)
    offenseIndex = datentry['offenseIndex']
    offentry = m.get(offenseIndex, crime['State'])
    if (offentry is None):
        entry = newOffenseEntry(crime['State'], crime)
        lt.addLast(entry['lstoffenses'], crime)
        m.put(offenseIndex, crime['State'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstoffenses'], crime)
    return datentry


def newDataEntry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstcrimes': None}
    entry['offenseIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareOffenses)
    entry['lstcrimes'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def newOffenseEntry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = lt.newList('SINGLELINKED', compareOffenses)
    return ofentry


# ==============================
# Funciones de consulta
# ==============================


def crimesSize(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer['crimes'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['dateIndex'])

def entryFecha(cont,initialDate):
    dia = me.getValue(om.get(cont["dateIndex"],initialDate))["offenseIndex"]
    return dia

def entreTiempos(cont,initialDate,finalDate,dix,k=False):
    if k==False:
        initialDate = om.floor(cont[dix],initialDate)
        finalDate = om.floor(cont[dix],finalDate)
    llaves = om.values(cont[dix],initialDate,finalDate)
    return llaves

def entryFechaAntes(cont,initialDate):
    initialDate = om.floor(cont["dateIndex"],initialDate)
    fechaMenor = om.minKey(cont["dateIndex"])
    llaves = om.values(cont["dateIndex"],fechaMenor,initialDate)
    return llaves

def EntreFechas(cont,initialDate,finalDate):
    return entreTiempos(cont,initialDate,finalDate,"dateIndex")

def EntreFechas2(cont,initialDate,finalDate):
    return entreTiempos(cont,initialDate,finalDate,"dateIndex2")

def EntreHoras(cont,initialDate,finalDate):
    return entreTiempos(cont,initialDate,finalDate,"hourIndex",True)

def distance(lat1, lat2, lon1, lon2): 
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 3956
       
    # calculate the result 
    return(c * r) 

# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareOffenses(offense1, offense2):
    """
    Compara dos tipos de crimenes
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1
