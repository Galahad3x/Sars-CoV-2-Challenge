import os
import sys
import glob

print("Instal·lació de llibreries")
os.system("sudo python3 libraries.py")

print("Activació algoritmes i fitxers")
for alg in glob.glob("*.py"):
    os.system("chmod 0755 " + alg)

for alg in glob.glob("/Algoritmes_Acabats/Python/*.py"):
    os.system("chmod 0755 " + alg)

print("Obtenció de mostres")
try:
    os.system("python3 fasta_finder.py " + sys.argv[1])
except IndexError:
    print("No has especificat la localització del fitxer all_sequences.csv")
    
