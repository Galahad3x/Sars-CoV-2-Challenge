import csv
import timeit
import math
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import itertools

os.system("pip3 install selenium &")
os.system("apt-get update &")
os.system("apt install chromium-chromedriver &")
os.system("dpkg --configure -a &")
os.system("cp /usr/lib/chromium-browser /usr/bin &")

gap = 7
order = { 'A': 0, 'G': 1, 'C': 2, 'T': 3}
mismatch = [[0,2,3,4],
            [2,0,5,1],
            [3,5,0,1],
            [4,3,1,0]]

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
csv_datab_route = "all_sequences.csv"
file_route = "time.txt"
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
for data in medians[7:9]:
    get_files(data)
    total_timeit += timeit.timeit("get_files(data)","from __main__ import get_files,data",number=1)

f.write("Total file scraping: \n")
f.write(str(total_timeit) + "\n")
f.write("Average file scraping: \n")
f.write(str(total_timeit/len(medians)) + "\n")

print("DONE")

f.close()
