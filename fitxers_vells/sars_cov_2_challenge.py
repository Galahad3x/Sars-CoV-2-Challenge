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
- Es pot treballar amb les dades fasta als blocs següents
"""

#Bloc 1

!pip3 install selenium &
!apt-get update &
!apt install chromium-chromedriver &
!dpkg --configure -a &
!cp /usr/lib/chromium-browser /usr/bin &

#Bloc 2

import csv
import timeit
import math
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import itertools

gap = 7
order = { 'A': 0, 'G': 1, 'C': 2, 'T': 3}
mismatch = [[0,2,3,4],
            [2,0,5,1],
            [3,5,0,1],
            [4,3,1,0]]

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

def calculate_score(seq_1,seq_2,gap,order,mismatch):
    score = 0
    for i, char in enumerate(seq_1):
        if char == "-" or seq_2[i] == "-":
            score += gap
        else:
            score += mismatch[order[char]][order[seq_2[i]]]
    return score

#Brute force
def sequence_alignment_brute(sequence_1,sequence_2,gap,order,mismatch):    
    final_len = len(sequence_1) + len(sequence_2) - 1

    new_1 = sequence_1
    while len(new_1) < final_len:
        new_1 += "-"
    new_2 = sequence_2
    while len(new_2) < final_len:
        new_2 += "-"
    
    for char in "ACTGN":
        new_1 = new_1.replace(char,"X")
        new_2 = new_2.replace(char,"X")
    possible_lineups_1 = list(set(["".join(com) for com in itertools.permutations(new_1,final_len)]))
    possible_lineups_2 = list(set(["".join(com) for com in itertools.permutations(new_2,final_len)]))

    possible_pairs = list([list(res) for res in itertools.product(possible_lineups_1,possible_lineups_2)])
    for cont, pair in enumerate(possible_pairs):
        i = 0
        while i < len(pair[0]):
            if pair[0][i] == "-" and pair[1][i] == "-":
                possible_pairs[cont][0] = possible_pairs[cont][0][0:i] + possible_pairs[cont][0][i+1:len(possible_pairs[cont][0])]
                possible_pairs[cont][1] = possible_pairs[cont][1][0:i] + possible_pairs[cont][1][i+1:len(possible_pairs[cont][1])]
            else:
                i += 1
    lineups = []
    for pair in possible_pairs:
        i = 0
        latest_1 = ""
        for ch in pair[0]:
            if ch == "-":
                latest_1 += "-"
            else:
                if sequence_1[i] != 'N':
                    latest_1 += sequence_1[i]
                elif sequence_2[i] != 'N':
                    latest_1 += sequence_2[i]
                else:
                    latest_1 += 'A'
                i += 1
        i = 0
        latest_2 = ""
        for ch in pair[1]:
            if ch == "-":
                latest_2 += "-"
            else:
                if sequence_2[i] != 'N':
                    latest_1 += sequence_2[i]
                elif sequence_1[i] != 'N':
                    latest_1 += sequence_1[i]
                else:
                    latest_1 += 'A'
                i += 1
        lineups.append((latest_1,latest_2))
            
    best_lineup = "",""
    best_score = calculate_score(lineups[0][0],lineups[0][1],gap,order,mismatch)
    best_lineup = sequence_1, lineups[0]
    for lineup in lineups[1:]:
        current_score = calculate_score(lineup[0],lineup[1],gap,order,mismatch)
        if current_score < best_score:
            best_score = current_score
            best_lineup = lineup
            

    return best_lineup[0], best_lineup[1], best_score

#Bloc 7

#Dynamic programming, Needleman-Wunsch method
def sequence_alignment_dynamic(sequence_1,sequence_2,gap,order,mismatch,return_traceback):
    if return_traceback:
        matriu = []

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
                if sequence_1[i] == 'N' or sequence_2[j] == "N":
                    mismatch_value = matriu[i][j]
                else:
                    mismatch_value = matriu[i][j] + mismatch[order[sequence_1[i]]][order[sequence_2[j]]]
                current_min = min(min(matriu[i+1][j] + gap,matriu[i][j+1] + gap),mismatch_value)
                matriu[i+1][j+1] = current_min
                if current_min == matriu[i][j] + mismatch[order[sequence_1[i]]][order[sequence_2[j]]]:
                    mat_traceback[i+1][j+1] = "d"
                elif current_min == matriu[i+1][j] + gap:
                    mat_traceback[i+1][j+1] = "l"
                else:
                    mat_traceback[i+1][j+1] = "u"

        #print("\n".join([str(lin) for lin in matriu]))
        #print("\n".join([str(lin) for lin in mat_traceback]))

        my_x = len(sequence_1)
        my_y = len(sequence_2)
        
        wres_1 = ""
        wres_2 = ""

        print(matriu[len(sequence_1)][len(sequence_2)])

        while mat_traceback[my_x][my_y] != "e":
            if mat_traceback[my_x][my_y] == "d":
                wres_2 = sequence_2[my_y-1] + wres_2
                wres_1 = sequence_1[my_x-1] + wres_1
                my_x -= 1
                my_y -= 1
            elif mat_traceback[my_x][my_y] == "l":
                wres_1 = "-" + wres_1
                wres_2 = sequence_2[my_y-1] + wres_2
                my_y -= 1
            else:
                wres_2 = "-" + wres_2
                wres_1 = sequence_1[my_x-1] + wres_1
                my_x -= 1

        return wres_1,wres_2,matriu[len(sequence_1)][len(sequence_2)]
    else:
        matriu = []

        #Creació matriu
        for _ in range(len(sequence_1) + 1):
            fila = []
            for _ in range(len(sequence_2) + 1):
                fila.append(0)
            matriu.append(fila)

        #Sequence 1 vertical, sequence 2 horitzontal

        matriu[0][0] = 0

        #Omplim la matriu
        for i in range(len(sequence_1)):
            matriu[i+1][0] = matriu[i][0] + gap
        for i in range(len(sequence_2)):
            matriu[0][i+1] = matriu[0][i] + gap

        for i in range(len(sequence_1)):
            for j in range(len(sequence_2)):
                if sequence_1[i] == 'N' or sequence_2[j] == "N":
                    mismatch_value = matriu[i][j]
                else:
                    mismatch_value = matriu[i][j] + mismatch[order[sequence_1[i]]][order[sequence_2[j]]]
                current_min = min(min(matriu[i+1][j] + gap,matriu[i][j+1] + gap),mismatch_value)
                matriu[i+1][j+1] = current_min

        #print("\n".join([str(lin) for lin in matriu]))
        #print("\n".join([str(lin) for lin in mat_traceback]))
        
        print(matriu[len(sequence_1)][len(sequence_2)])
        return matriu[len(sequence_1)][len(sequence_2)]

#Bloc 8

def calculate_pos(matriu,i,j,sequence_1,sequence_2,order,mismatch,gap,traceback,return_traceback):
    if return_traceback:
        #print("\n".join([str(lin) for lin in traceback]))
        if i > 0 and matriu[i-1][j] == -1:
            matriu, traceback = calculate_pos(matriu,i-1,j,sequence_1,sequence_2,order,mismatch,gap,traceback,return_traceback)
        if j > 0 and matriu[i][j-1] == -1:
            matriu, traceback = calculate_pos(matriu,i,j-1,sequence_1,sequence_2,order,mismatch,gap,traceback,return_traceback)
        if i > 0 and j > 0 and matriu[i-1][j-1] == -1:
            matriu, traceback = calculate_pos(matriu,i-1,j-1,sequence_1,sequence_2,order,mismatch,gap,traceback,return_traceback)
        if sequence_1[i] == 'N' or sequence_2[j] == "N":
            mismatch_value = matriu[i-1][j-1]
        else:
            mismatch_value = matriu[i-1][j-1] + mismatch[order[sequence_1[i-1]]][order[sequence_2[j-1]]]
        matriu[i][j] = min(min(matriu[i-1][j] + gap,matriu[i][j-1] + gap),mismatch_value)
        if matriu[i][j] == matriu[i-1][j-1] + mismatch[order[sequence_1[i-1]]][order[sequence_2[j-1]]]:
            traceback[i][j] = "d"
        elif matriu[i][j] == matriu[i][j-1] + gap:
            traceback[i][j] = "u"
        else:
            traceback[i][j] = "l"
        return matriu, traceback
    else:
        if i > 0 and matriu[i-1][j] == -1:
            matriu = calculate_pos(matriu,i-1,j,sequence_1,sequence_2,order,mismatch,gap,traceback,return_traceback)
        if j > 0 and matriu[i][j-1] == -1:
            matriu = calculate_pos(matriu,i,j-1,sequence_1,sequence_2,order,mismatch,gap,traceback,return_traceback)
        if i > 0 and j > 0 and matriu[i-1][j-1] == -1:
            matriu = calculate_pos(matriu,i-1,j-1,sequence_1,sequence_2,order,mismatch,gap,traceback,return_traceback)
        if sequence_1[i] == 'N' or sequence_2[j] == "N":
            mismatch_value = matriu[i-1][j-1]
        else:
            mismatch_value = matriu[i-1][j-1] + mismatch[order[sequence_1[i-1]]][order[sequence_2[j-1]]]
        matriu[i][j] = min(min(matriu[i-1][j] + gap,matriu[i][j-1] + gap),mismatch_value)
        return matriu

#Dynamic programming, Needleman-Wunsch method recursive
def sequence_alignment_dynamic_2(sequence_1,sequence_2,gap,order,mismatch,return_traceback):
    try:
        if return_traceback:
            matriu = []

            #Creació matriu
            mat_traceback = []
            for _ in range(len(sequence_1) + 1):
                fila = []
                for _ in range(len(sequence_2) + 1):
                    fila.append(-1)
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

            cont = 0
            matriu, mat_traceback = calculate_pos(matriu,len(sequence_1),len(sequence_2),sequence_1,sequence_2,order,mismatch,gap,mat_traceback,return_traceback)

            #print("\n".join([str(lin) for lin in matriu]))
            #print("\n".join([str(lin) for lin in mat_traceback]))

            my_x = len(sequence_1)
            my_y = len(sequence_2)
            
            wres_1 = ""
            wres_2 = ""

            print(matriu[len(sequence_1)][len(sequence_2)])

            while mat_traceback[my_x][my_y] != "e":
                if mat_traceback[my_x][my_y] == "d":
                    wres_2 = sequence_2[my_y-1] + wres_2
                    wres_1 = sequence_1[my_x-1] + wres_1
                    my_x -= 1
                    my_y -= 1
                elif mat_traceback[my_x][my_y] == "l":
                    wres_1 = "-" + wres_1
                    wres_2 = sequence_2[my_y-1] + wres_2
                    my_y -= 1
                else:
                    wres_2 = "-" + wres_2
                    wres_1 = sequence_1[my_x-1] + wres_1
                    my_x -= 1

            return wres_1,wres_2,matriu[len(sequence_1)][len(sequence_2)]
        else:
            matriu = []

            #Creació matriu
            for _ in range(len(sequence_1) + 1):
                fila = []
                for _ in range(len(sequence_2) + 1):
                    fila.append(-1)
                matriu.append(fila)

            #Sequence 1 vertical, sequence 2 horitzontal

            matriu[0][0] = 0

            #Omplim la matriu
            for i in range(len(sequence_1)):
                matriu[i+1][0] = matriu[i][0] + gap
            for i in range(len(sequence_2)):
                matriu[0][i+1] = matriu[0][i] + gap

            cont = 0
            matriu = calculate_pos(matriu,len(sequence_1),len(sequence_2),sequence_1,sequence_2,order,mismatch,gap,None,return_traceback)

            print(matriu[len(sequence_1)][len(sequence_2)])
            return matriu[len(sequence_1)][len(sequence_2)]
    except RecursionError:
        print("Maximum recursion depth exceeded")

#Bloc 9

#Dynamic programming, Needleman-Wunsch simple
def sequence_alignment_dynamic_score(sequence_1,sequence_2,gap,order,mismatch):
    top_line = [i*gap for i in range(len(sequence_2) + 1)]
    vertical_seq = [i*gap for i in range(len(sequence_1) + 1)]

    line_c = 0
    col_c = 0

    while line_c <= len(sequence_1):
        print(top_line)
        current_line = []
        current_line.append(vertical_seq[line_c])
        col_c = 1
        while len(current_line) < len(top_line):
            if sequence_1[i] == 'N' or sequence_2[j] == "N":
                mismatch_value = top_line[col_c-1]
            else:
                mismatch_value = top_line[col_c-1] + mismatch[order[sequence_1[line_c-1]]][order[sequence_2[col_c-1]]]
            current_line.append(min(min(current_line[col_c-1] + gap,top_line[col_c] + gap),mismatch_value))
            col_c += 1
        top_line = current_line
        line_c += 1

    return top_line[-1]

print(sequence_alignment_dynamic_score("TACC","ACCG",gap,order,mismatch))

#Bloc 10

#mismatch = [[0,3,3,3],[3,0,3,3],[3,3,0,3],[3,3,3,0]]


for char_len in range(1,30):
    seq_1 = open("Spain.fasta","r").read(char_len*1000)
    seq_2 = open("China.fasta","r").read(char_len*1000)

    print(str(char_len*1000) + " caracters")
    print(timeit.timeit("sequence_alignment_dynamic(seq_1,seq_2,gap,order,mismatch,False)","from __main__ import sequence_alignment_dynamic,seq_1,seq_2,gap,order,mismatch",number=1))
    print(timeit.timeit("sequence_alignment_dynamic_2(seq_1,seq_2,gap,order,mismatch,False)","from __main__ import sequence_alignment_dynamic_2,seq_1,seq_2,gap,order,mismatch",number=1))
    print(timeit.timeit("sequence_alignment_brute(seq_1,seq_2,gap,order,mismatch)","from __main__ import sequence_alignment_brute,seq_1,seq_2,gap,order,mismatch",number=1))
