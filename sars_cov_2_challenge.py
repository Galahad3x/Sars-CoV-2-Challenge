# -*- coding: utf-8 -*-
"""Sars-CoV-2-Challenge.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LGKUyx-X0Ef6GGKBdgcyvfIa2Pbery9n

Bloc 1: Instalació de llibreries  
Bloc 2: Importació de llibreries  
Bloc 3: Per treballar amb fitxers des del Drive  
Bloc 4: Definició de funcions  
Bloc 5: Crida de funcions  
  
Com fer servir:  
- Executar bloc 1 i després bloc 2  
- Executar bloc 4  
SI ES VOL TREBALLAR AL DRIVE:  
+ Executar el bloc 3 i introduïr el codi de la web
+ Canviar les variables "csv_datab_name" i "filename" a la carpeta on hi ha la base de dades  
SI NO:  
+ Canviar les variables "csv_datab_name" i "filename" a la carpeta on hi ha la base de dades  
FINALMENT:
- Executar el bloc 5  
- Es pot treballar amb les dades fasta al bloc 6
"""

#Bloc 1

!pip3 install selenium
!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin

#Bloc 2

import csv
import timeit
import math
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

#Bloc 3

from google.colab import drive
drive.mount('/content/drive')

#Bloc 4

def get_global_data(route):
    #Format global_data: Accession, Length, Location, Date
    global_data = []
    with open(route,newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for i, row in enumerate(reader):
            if i > 3:
                line = ','.join(row).split(",")
                if line[2].endswith(":"):
                    line[2] = line[2][:-1]
                    line[3] = line[4]
                    line = line[:-1]
                if line[2].startswith("\""):
                    line[2] = line[2][1:]
                if line[2] != '':
                    global_data.append(line)

    return global_data

def separate_in_countries(data,mode):
    if mode == 1:
        countries = []
        for row in data:
            if not row[2] in countries:
                countries.append(row[2])
        separated_data = []
        for country in countries:
            country_line = []
            for row in data:
                if row[2] == country:
                    country_line.append(row)
            separated_data.append(country_line)
        return separated_data
    else:
        separated_data = {}
        for row in data:
            if row[2] in separated_data.keys():
                separated_data[row[2]].append(row)
            else:
                separated_data[row[2]] = [row]
        return [separated_data[key] for key in separated_data.keys()]

def country_medians(data):
    medians = []
    for country_data in data:
        country_name = country_data[0][2]
        medians.append((country_name,country_data[math.floor(len(country_data) / 2)][1],country_data[math.floor(len(country_data) / 2)][0]))
    return medians

def get_files(country_data):
    url = "https://www.ncbi.nlm.nih.gov/nuccore/" + str(country_data[2]) + ".1?report=fasta"
    filename = str(country_data[0]) + ".fasta"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver',options=chrome_options)
    driver.get(url)
    sleep(0.2)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    f = open(filename,"w")
    f.write("".join(soup.find(id="viewercontent1").text.split("\n")[1:]))
    f.close()

#Bloc 5

#Ruta Joel A, l'haureu de canviar si ho voleu provar
csv_datab_route = "/content/drive/My Drive/Uni/Practica1-Algoritmica/all_sequences.csv"
file_route = "/content/drive/My Drive/Uni/Practica1-Algoritmica/time.txt"
f = open(file_route,"w")

#O(N) -> N = Numero total de mostres
my_data = get_global_data(csv_datab_route)
f.write("Get global data:\n")
f.write(str(timeit.timeit("get_global_data(csv_datab_route)","from __main__ import csv_datab_route, get_global_data",number=1)) + "\n")

#O(M*N) -> M = Numero total de països
my_countries = separate_in_countries(my_data,2)
f.write("Separate in countries 1:\n")
f.write(str(timeit.timeit("separate_in_countries(my_data,1)","from __main__ import separate_in_countries,my_data",number=1)) + "\n")
f.write("Separate in countries 2:\n")
f.write(str(timeit.timeit("separate_in_countries(my_data,2)","from __main__ import separate_in_countries,my_data",number=1)) + "\n")

#O(M)
medians = country_medians(my_countries)
f.write("Medians:\n")
f.write(str(timeit.timeit("country_medians(my_countries)","from __main__ import country_medians,my_countries",number=1)) + "\n")

#O(M)
total_timeit = 0.0
for data in medians:
    get_files(data)
    total_timeit += timeit.timeit("get_files(data)","from __main__ import get_files,data",number=1)

f.write("Total file scraping: \n")
f.write(str(total_timeit) + "\n")
f.write("Average file scraping: \n")
f.write(str(total_timeit/len(medians)) + "\n")

print("DONE")

f.close()

#Bloc 6

#Brute force
def sequence_alignment_brute(sequence_1,sequence_2):
    #Trobar tots els camins i calcular el seu cost 
    # INEFICIENT !!!
    pass

#Retornarà tupla de strings del estil "NNNGNGNN" on G es Gap i N Nogap
def find_path(mat,punt,endpoint,results):
    if punt == endpoint:
        return results
    else:
        try:
            min_next = min(min(mat[punt[0]+1][punt[1]],mat[punt[0]][punt[1]+1]),mat[punt[0]+1][punt[1]+1])
        except IndexError:
            try:
                min_next = mat[punt[0]+1][punt[1]]
            except IndexError:
                return find_path(mat,(punt[0],punt[1]+1),endpoint,(results[0]+"G",results[1]+"N"))
        if min_next == mat[punt[0]+1][punt[1]+1]:
            #Gap horitzontal
            return find_path(mat,(punt[0]+1,punt[1]+1),endpoint,(results[0]+"N",results[1]+"N")) 
        elif min_next == mat[punt[0]][punt[1]+1]:
            #Gap vertical
            return find_path(mat,(punt[0],punt[1]+1),endpoint,(results[0]+"G",results[1]+"N"))
        else:
            return find_path(mat,(punt[0]+1,punt[1]),endpoint,(results[0]+"N",results[1]+"G"))
            

#Dynamic programming, Needleman-Wunsch method
def sequence_alignment_dynamic(sequence_1,sequence_2):
    gap = 4
    matriu = []

    order = { 'A': 0, 'G': 1, 'C': 2, 'T': 3}
    mismatch = [[0,2,3,4],[2,0,5,1],[3,5,0,1],[4,3,1,0]]
    mismatch = [[0,3,3,3],[3,0,3,3],[3,3,0,3],[3,3,3,0]]

    #Creació matriu
    mat_traceback = []
    for _ in range(len(sequence_1) + 1):
        fila = []
        for _ in range(len(sequence_2) + 1):
            fila.append(0)
        matriu.append(fila)
        mat_traceback.append(fila[:])

    #Sequence 1 vertical, sequence 2 horitzontal

    matriu[0][0] = 0
    mat_traceback[0][0] = "e"

    #Omplim la matriu
    for i in range(len(sequence_1)):
        matriu[i+1][0] = matriu[i][0] + gap
        mat_traceback[i+1][0] = "u"
    for i in range(len(sequence_2)):
        matriu[0][i+1] = matriu[0][i] + gap
        mat_traceback[0][i+1] = "l"

    for i in range(len(sequence_1)):
        for j in range(len(sequence_2)):
            current_min = min(min(matriu[i+1][j] + gap,matriu[i][j+1] + gap),matriu[i][j] + mismatch[order[sequence_1[i]]][order[sequence_2[j]]])
            matriu[i+1][j+1] = current_min
            if current_min == matriu[i][j] + mismatch[order[sequence_1[i]]][order[sequence_2[j]]]:
                mat_traceback[i+1][j+1] = "d"
            elif current_min == matriu[i+1][j] + gap:
                mat_traceback[i+1][j+1] = "l"
            else:
                mat_traceback[i+1][j+1] = "u"

    res = find_path(matriu,(0,0),(len(sequence_1),len(sequence_2)),("",""))

    #print("\n".join([str(lin) for lin in matriu]))
    #print("\n".join([str(lin) for lin in mat_traceback]))

    my_x = len(sequence_1)
    my_y = len(sequence_2)
    
    wres_1 = ""
    wres_2 = ""

    while mat_traceback[my_x][my_y] != "e":
        if mat_traceback[my_x][my_y] == "d":
            wres_1 = sequence_1[my_x-1] + wres_1
            wres_2 = sequence_2[my_y-1] + wres_2
            my_x -= 1
            my_y -= 1
        elif mat_traceback[my_x-1][my_y-1] == "l":
            wres_2 = "-" + wres_2
            wres_1 = sequence_1[my_x-1] + wres_1
            my_x -= 1
        else:
            wres_1 = "-" + wres_1
            wres_2 = sequence_2[my_y-1] + wres_2
            my_y -= 1

    return wres_1,wres_2,matriu[len(sequence_1)][len(sequence_2)]

seq_1 = "ACGGCTC"
seq_2 = "ATGGCCTC"

print(sequence_alignment_dynamic(seq_1,seq_2))

res_1 = ""
    i = 0
    for char in res[0]:
        if char == "N":
            res_1 += sequence_1[i]
            i += 1
        else:
            res_1 += "-"
    
    res_2 = ""
    i = 0
    for char in res[1]:
        if char == "N":
            res_2 += sequence_2[i]
            i += 1
        else:
            res_2 += "-"