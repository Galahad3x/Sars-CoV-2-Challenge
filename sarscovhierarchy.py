#!/usr/bin/python3

import sys
import glob
import os
from time import sleep
import folium as fo
import webbrowser

class Cluster:

    def __init__(self,center,members,color):
        self.center = center
        self.members = members
        self.color = color

class Country:

    def __init__(self,name,filename):
        self.name = name
        self.filename = filename
        self.distances = {}

    def compare(self,other):
        print("Comparant " + self.name + " i " + other.name)
        if self.name == other.name:
            return 0
        if other.name in self.distances.keys():
            return self.distances[other.name]
        elif self.name in other.distances.keys():
            self.distances[other.name] = other.distances[self.name]            
            return other.distances[self.name]
        else:
            os.system("./NWS_C " + self.filename + " " + other.filename + "> res.txt")
            sleep(0.1)
            with open("res.txt","r") as r:
                result = int(r.readline())
            self.distances[other.name] = result
            return result


def hierarchical_classification(route):
    print("Hierarchical classification")
    mostra_list = glob.glob(route + "/*.fasta")

def centers(clusters):
    return [clus.center.name for clus in clusters]

def assign_countries(clusters,countries):
    for cluster in clusters:    
        cluster.members = []
    for country in countries:
        minimum_distance = -1
        cluster_index = -1
        for ind, cluster in enumerate(clusters):
            distance = country.compare(cluster.center)
            if distance < minimum_distance or minimum_distance == -1:
                minimum_distance = distance
                cluster_index = ind
        clusters[cluster_index].members.append(country)
    return clusters

def move_centers(clusters):
    for cluster in clusters:
        new_center = cluster.center        
        best_distance = sum([cluster.center.compare(mem) for mem in cluster.members])
        for member in cluster.members:
            current_distance = sum([member.compare(mem) for mem in cluster.members])
            if current_distance < best_distance:
                new_center = mem
        if cluster.center.name != new_center.name:
            print("New cluster center: " + new_center)
        cluster.center = new_center
    return clusters
        
def generate_map(clusters):
    m = fo.Map(
        location=[40.416775, -3.703790],
        tiles='OpenStreetMap',
        zoom_start=2
    )
    filepath = 'map.html'
    folium.Marker(
        location=[45.3288, -121.6625],
        popup='Mt. Hood Meadows',
        icon=folium.Icon(icon='cloud')
    ).add_to(m)
    m.save(filepath)

def k_medoids(route,k):
  colors = ["red","blue","green","purple","orange","darkred","lightred",
"beige","darkblue","darkgreen","cadetblue","darkpurple","white",
"pink","lightblue","lightgreen","gray","black","lightgray"]
    countries = []
    for ffile in glob.glob(route + "/*.fasta"):
        countries.append(Country(ffile.split("/")[-1].split(".")[-2],ffile))
    clusters = []
    for i in range(k):
        try:
            clusters.append(Cluster(countries[i],[countries[i]],colors[i]))
        except IndexError:
            print("ERROR: Selecciona un número més petit de k's")
            return -1
    clusters = assign_countries(clusters,countries)
    clusters = move_centers(clusters)
    while True:
        old_centers = centers(clusters)
        clusters = assign_countries(clusters,countries)
        clusters = move_centers(clusters)
        if old_centers == centers(clusters):
            break
    print("Definitive clusters: ")
    for cluster in clusters:
        print(cluster.center.name,[mem.name for mem in cluster.members])
        print("\n")
    generate_map(clusters)
    return 0

print("*******SARS-COV-2 CHALLENGE*******")
print("MEMBRES DEL GRUP: ")
print("\tJoel Aumedes Serrano")
print("\tArmand Ciutat Camps")
print("\tRoger Castellví Rubinat")
print("\tJoel Farré Cortés")
print("**********************************\n")

#hierarchical_classification(sys.argv[1])

try:
    while True:
        try:
            clusts = input("Escriu un número de centres per a fer k-medoids: ")
            if int(clusts) > 0:
                while k_medoids(sys.argv[1],int(clusts)) != 0:
                    clusts = input("Escriu un número de centres per a fer k-medoids: ")
                break
            else:
                print("ERROR: No es poden fer servir clusters negatius")
        except ValueError:
            pass
except IndexError:
    print("ERROR: No has especificat la ruta amb les mostres")

