import sys
import os

def replace_nuc(first_file):
    the_file = first_file[:]
    the_file = the_file.replace("U","T")
    the_file = the_file.replace("W","AT")
    the_file = the_file.replace("S","CG")
    the_file = the_file.replace("M","AC")
    the_file = the_file.replace("K","GT")
    the_file = the_file.replace("R","AG")
    the_file = the_file.replace("Y","CT")
    the_file = the_file.replace("B","CGT")
    the_file = the_file.replace("D","AGT")
    the_file = the_file.replace("H","ACT")
    the_file = the_file.replace("V","ACG")
    return the_file

my_file = open(sys.argv[1],"r").read()[:-1]

print(my_file)
my_file = replace_nuc(my_file)
print(my_file)

new_filename = sys.argv[1].split(".")[0] + "2." + sys.argv[1].split(".")[1] 

with open(new_filename,"w") as f:
    f.write(my_file)

os.system("cp " + new_filename + " " + sys.argv[1] + "")
os.system("rm -rf " + new_filename)
