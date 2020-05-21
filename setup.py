import os
import sys

print("Instal·lació de llibreries")
os.system("sudo python3 libraries.py")

print("Obteció de mostres")
try:
    os.system("python3 fasta_finder.py " + sys.argv[1])
except IndexError:
    print("No has especificat la localització del fitxer all_sequences.csv")
    
