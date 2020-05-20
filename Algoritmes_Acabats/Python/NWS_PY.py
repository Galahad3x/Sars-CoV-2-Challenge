#!/usr/bin/python3

import sys

gap = 7
order = { 'A': 0, 'G': 1, 'C': 2, 'T': 3}
mismatch = [[0,2,3,4],
            [2,0,5,1],
            [3,5,0,1],
            [4,3,1,0]]

def sequence_alignment_dynamic_score(sequence_1,sequence_2,gap,order,mismatch):
    top_line = [i*gap for i in range(len(sequence_2) + 1)]
    current_line = [i*gap for i in range(len(sequence_2) + 1)]

    line_c = 0
    col_c = 0

    while line_c <= len(sequence_1):
        current_line[0] = top_line[0] + gap
        col_c = 1
        while col_c < len(top_line):
            if sequence_1[line_c - 1] == 'N' or sequence_2[col_c-1] == "N":
                mismatch_value = top_line[col_c-1]
            else:
                mismatch_value = top_line[col_c-1] + mismatch[order[sequence_1[line_c-1]]][order[sequence_2[col_c-1]]]
            current_line[col_c] = (min(min(current_line[col_c-1] + gap,top_line[col_c] + gap),mismatch_value))
            col_c += 1
        for i in range(len(top_line)):                
            top_line[i] = current_line[i]
        line_c += 1
        print(line_c)

    print(top_line[-1])
    return top_line[-1]

file1 = open(sys.argv[1],"r")
file2 = open(sys.argv[2],"r")

print(sequence_alignment_dynamic_score(file1.read()[:-1],file2.read()[:-1],gap,order,mismatch))
