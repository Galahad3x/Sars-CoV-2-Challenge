#!/usr/bin/python3

import sys
import glob
import os
from time import sleep
import folium as fo
import webbrowser
import threading
import signal
import csv
import subprocess
import inspect
import pygame

def quit_all(signum,stack):
    print("Exiting by CNTRL+C")
    os.system("killall -9 NWS_C")
    os.system("killall -9 -e sarscovhierarch")
    raise SystemExit

signal.signal(signal.SIGINT,quit_all)
#os.system("killall -9 NWS_C")

countries = []
trees = []

class Cluster:

    def __init__(self,center,members,color):
        self.center = center
        self.members = members
        self.color = color

class Country:

    def read_distances(self,dists):
        try:
            with open('saved_distances.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in spamreader:
                    if row[0].split(",")[0] == self.name:
                        dists[row[0].split(",")[1]] = int(row[0].split(",")[2])
                    elif row[0].split(",")[1] == self.name:
                        dists[row[0].split(",")[0]] = int(row[0].split(",")[2])
            return dists
        except FileNotFoundError:
            return dists

    def __init__(self,name,filename,coordinates):
        self.name = name
        self.filename = filename
        self.distances = self.read_distances({})
        self.distances[self.name] = 0
        self.coordinates = coordinates
        self.grouped = 0

    def find_distance(self,other_name):
        found = False
        for other in countries:
            if other_name == other.name:
                self.compare(other)
                found = True
                break
        if not found:
            for cont in other_name.replace("(","").replace(")","").split(","):
                self.find_distance(cont)
            parens = 0
            new_name = list(other_name)
            for ind,char in enumerate(other_name):
                if char == "(":
                    parens += 1
                elif char == ")":
                    parens -= 1
                elif char == "," and parens == 1:
                    new_name[ind] = "_"
                    break
            new_nam = "".join(new_name)
            self.find_distance(new_nam.split("_")[0][1:])
            self.find_distance(new_nam.split("_")[1][:-1])
            self.distances[other_name] = (self.distances[new_nam.split("_")[0][1:]] + self.distances[new_nam.split("_")[1][:-1]])//2

    def compare(self,other):
        #print("Comparant " + self.name + " i " + other.name)
        if self.name == other.name:
            self.distances[other.name] = 0
            return 0
        if other.name in self.distances.keys():
            #print("Comparat " + self.name + " i " + other.name)
            return self.distances[other.name]
        elif self.name in other.distances.keys():
            if type(other) == Country:
                self.distances[other.name] = other.distances[self.name]
            #print("Comparat " + self.name + " i " + other.name)
            return other.distances[self.name]
        else:
            if type(other) == Country:
                respr = subprocess.run(["./NWS_C",self.filename,other.filename],capture_output=True)
                result = int(respr.stdout.decode())
                with open('saved_distances.csv', 'a', newline='') as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow([self.name,other.name,str(result)])
                self.distances = self.read_distances(self.distances)
                #print("Comparat " + self.name + " i " + other.name)
                return result
            else:
                self.distances[other.name] = (self.compare(other.leftCh) + self.compare(other.rightCh))//2
                return (self.compare(other.leftCh) + self.compare(other.rightCh))//2
            

class Tree:
    
    def mix_distances(self,dists):
        leftDistances = self.leftCh.distances
        rightDistances = self.rightCh.distances
        total_dists = list(set([*leftDistances,*rightDistances]))
        try:
            total_dists.remove(self.leftCh.name)
            total_dists.remove(self.rightCh.name)
        except ValueError:
            pass
        dists[self.name] = 0
        for country in total_dists:
            if country in leftDistances.keys() and country in rightDistances.keys():
                dists[country] = (leftDistances[country] + rightDistances[country])//2
            elif country in leftDistances.keys():
                self.rightCh.find_distance(country)
                self.calculate_tree_distance(country)
                try:
                    rightt = self.rightCh.distances[country]
                except KeyError:
                    rightt = 0
                    self.rightCh.distances[country] = 0
                dists[country] = (leftDistances[country] + rightt)//2
            elif country in rightDistances.keys():
                self.leftCh.find_distance(country)
                self.calculate_tree_distance(country)
                try:
                    leftt = self.leftCh.distances[country]
                except KeyError:
                    leftt = 0
                    self.leftCh.distances[country] = 0
                dists[country] = (leftt + rightDistances[country])//2
        return dists

    def calculate_tree_distance(self,tree_name):
        try:
            for tree in trees:
                if tree.name == tree_name:
                    self.calculate_tree_distance(tree.leftCh.name)
                    self.calculate_tree_distance(tree.rightCh.name)
                    self.distances[tree.name] = (self.distances[tree.leftCh.name] + self.distances[tree.rightCh.name])//2
        except AttributeError:
            pass

    def find_distance(self,country):
        self.leftCh.find_distance(country)
        self.rightCh.find_distance(country)
        self.distances = self.mix_distances(self.distances)
#        self.root.distances = self.mix_distances(self.distances)
        self.grouped = 0

    def compare(self,other):
        if other.name in self.distances.keys():
            return self.distances[other.name]
        else:
            self.distances[other.name] = (self.leftCh.compare(other) + self.rightCh.compare(other))//2
            return self.distances[other.name]       

    def __init__(self,leftCh,rightCh):
        self.name = "(" + leftCh.name + "," + rightCh.name + ")"
        self.leftCh = leftCh
        self.rightCh = rightCh
        self.distances = self.mix_distances({})
#        self.root = Country(self.name,"",self.distances,[])


def read_coords(llista):
    coords = {}
    with open(llista,"r") as llis:
        for line in llis.readlines():
            coords[line.split(",")[0]] = [float(spl) for spl in line.split(",")[1:3]]
    return coords

colors = ["red","blue","green","purple","orange","darkred","lightred",
"beige","darkblue","darkgreen","cadetblue","darkpurple","white",
"pink","lightblue","lightgreen","gray","black","lightgray"]
coordinates = read_coords("llista.txt")
for ffile in glob.glob(sys.argv[1] + "/*.fasta"):
    country_name = ffile.split("/")[-1].split(".")[-2]
    countries.append(Country(country_name,ffile,coordinates[country_name]))

def hierarchical_classification(pendent_countries):
    global trees
    next_lap = []
    grouped = []
    for country in pendent_countries:
        country.grouped = 0
    for country in pendent_countries:
        min_country = None
        for country2 in pendent_countries:
            distance = country.compare(country2)
            if country.name != country2.name and (min_country == None or distance <= country.compare(min_country)):
                min_country = country2
        min_country2 = None
        for country2 in pendent_countries:
            distance = min_country.compare(country2)
            if country2.name != min_country.name and (min_country2 == None or distance <= min_country.compare(min_country2)):
                min_country2 = country2
        if country.name == min_country2.name and country not in grouped and min_country2 not in grouped:
            # print("Grouped " + country.name + " with " + min_country.name)
            country.grouped = 1
            min_country2.grouped = 1
            grouped.append(country)
            grouped.append(min_country)
            theTree = Tree(country,min_country)
            next_lap.append(theTree)
            trees.append(theTree)
    for country in pendent_countries:
        if country not in grouped:
            next_lap.append(country)
    if len(next_lap) != 1:
        return hierarchical_classification(next_lap)
    else:
        return next_lap[0]

def tree_height(tree):
    if len(tree.split(",")) == 2:
        return 2
    elif len(tree.split(",")) == 1:
        return 1
    else:
        new_tree = list(tree)
        parens = 0
        for ind, char in enumerate(new_tree):
            if char == "(":
                parens += 1
            elif char == ")":
                parens -= 1
            elif char == "," and parens == 1:
                new_tree[ind] = "_"
        new_tree = "".join(new_tree)
        return 1 + max(tree_height(new_tree.split("_")[0][1:]),tree_height(new_tree.split("_")[1][:-1]))


def graphic_representation_2(tree, width, x_offset, level, level_h,size,scr,prev_c):
    my_height = tree_height(tree)
    my_coords = (int(x_offset + width//2),int((level*level_h) + 5))
    pygame.draw.line(scr, (0,0,0), my_coords, prev_c, 3)
    pygame.draw.circle(scr, (255,100,100), prev_c , size)
    if my_height == 1:
        pygame.draw.circle(scr, (255,100,100), my_coords , size)
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render(tree[:5], True, (0,0,0), (255,100,100))
        textRect = text.get_rect()
        textRect.center = my_coords
        scr.blit(text,textRect)
    if my_height != 1:
        new_tree = list(tree)
        parens = 0
        for ind, char in enumerate(new_tree):
            if char == "(":
                parens += 1
            elif char == ")":
                parens -= 1
            elif char == "," and parens == 1:
                new_tree[ind] = "_"
        new_tree = "".join(new_tree)
        if max(tree_height(new_tree.split("_")[0][1:]),tree_height(new_tree.split("_")[1][:-1])) == tree_height(new_tree.split("_")[0][1:]):        
            height_difference = tree_height(new_tree.split("_")[0][1:])/tree_height(new_tree.split("_")[1][:-1])
            graphic_representation_2(new_tree.split("_")[0][1:],
                                    (width//(height_difference+1))*height_difference,
                                    x_offset,level+1,
                                    level_h,size,scr,my_coords)
            graphic_representation_2(new_tree.split("_")[1][:-1],
                                    width - (width//(height_difference+1))*height_difference,
                                    x_offset + width//2,level+1,level_h,size,scr,my_coords)
        else:
            height_difference = tree_height(new_tree.split("_")[1][:-1])/tree_height(new_tree.split("_")[0][1:])
            graphic_representation_2(new_tree.split("_")[0][1:],
                                    width - (width//(height_difference+1))*height_difference,
                                    x_offset,level+1,
                                    level_h,size,scr,my_coords)
            graphic_representation_2(new_tree.split("_")[1][:-1],
                                    (width//(height_difference+1))*height_difference,
                                    x_offset + width//2,level+1,
                                    level_h,size,scr,my_coords)

def graphic_representation(tree, width, height):
    pygame.init()
    screen = pygame.display.set_mode([width, height])
    
    pygame.display.set_caption('Hierarchical Classification')

    screen.fill((100, 100, 100))

    real_width = width - 10
    real_height = height - 10
    
    circle_size = (real_width//len(countries))-15

    tree_h = tree_height(tree)
    level_height = real_height//tree_h

    graphic_representation_2(tree,real_width,5,0,level_height,circle_size,screen,(5+real_width//2,5))

    pygame.display.flip()

    while True:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()            
                    break
            sleep(0.2)
        except pygame.error:
            break

def text_representation(hier,lvl):
    starters = "".join(["|" for _ in range(lvl)])
    print(starters + "" + hier)
    if tree_height(hier) != 1:
        new_tree = list(hier)
        parens = 0
        for ind, char in enumerate(new_tree):
            if char == "(":
                parens += 1
            elif char == ")":
                parens -= 1
            elif char == "," and parens == 1:
                new_tree[ind] = "_"
        new_tree = "".join(new_tree)
        text_representation(new_tree.split("_")[0][1:],lvl+1)
        text_representation(new_tree.split("_")[1][:-1],lvl+1)


def centers(clusters):
    return [clus.center.name for clus in clusters]


def center_calculation(cntry, clusters, index):
    try:
        minimum_distance = -1
        cluster_index = -1
        for ind, cluster in enumerate(clusters):
            distance = cntry.compare(cluster.center)
            if distance < minimum_distance or minimum_distance == -1:
                minimum_distance = distance
                cluster_index = ind
        clusters[cluster_index].members.append(cntry)
    except ValueError:
        quit_all(0,0)
    

def assign_countries(clusters,countries):
    try:
        for cluster in clusters:    
            cluster.members = []
        for inx, country in enumerate(countries):
            minimum_distance = -1
            cluster_index = -1
            for ind, cluster in enumerate(clusters):
                distance = country.compare(cluster.center)
                if distance < minimum_distance or minimum_distance == -1:
                    minimum_distance = distance
                    cluster_index = ind
            clusters[cluster_index].members.append(country)
        return clusters
    except SystemExit:
        quit_all(0,0)

def move_centers(clusters):
    for cluster in clusters:
        new_center = cluster.center        
        best_distance = sum([cluster.center.compare(mem) for mem in cluster.members])
        for member in cluster.members:
            current_distance = sum([member.compare(mem) for mem in cluster.members])
            if current_distance < best_distance:
                new_center = member
        if cluster.center.name != new_center.name:
            print("New cluster center: " + new_center.name)
        cluster.center = new_center
    return clusters
        
def generate_map(clusters):
    m = fo.Map(
        location=[40.416775, -3.703790],
        tiles='OpenStreetMap',
        zoom_start=2
    )
    for cluster in clusters:
        for country in cluster.members:
            if country.name == cluster.center.name:
                fo.Marker(
                    location = country.coordinates,
                    popup=country.name,
                    icon=fo.Icon(color=cluster.color, icon='glyphicon-star')
                ).add_to(m)
            else:
                fo.Marker(
                    location = country.coordinates,
                    popup=country.name,
                    icon=fo.Icon(color=cluster.color, icon='glyphicon-map-marker')
                ).add_to(m)
    filepath = 'map.html'
    m.save(filepath)

def k_medoids(route,k):
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
        print(cluster.center.distances)
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

userin = input("Què vols fer? K|k: k-medoids, H|h: Hierarchical classification: ")

if userin == 'k' or userin == 'K':
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
elif userin == 'h' or userin == 'H':
    try:
        hier = hierarchical_classification(countries).name
        text_representation(hier,0)
        graphic_representation(hier,1360,768)
    except ValueError:
        pass
