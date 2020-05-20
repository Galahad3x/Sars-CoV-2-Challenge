#!/usr/bin/python3

import sys
import itertools

gap = 7
order = { 'A': 0, 'G': 1, 'C': 2, 'T': 3}
mismatch = [[0,2,3,4],
            [2,0,5,1],
            [3,5,0,1],
            [4,3,1,0]]

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
                    latest_2 += sequence_2[i]
                elif sequence_1[i] != 'N':
                    latest_2 += sequence_1[i]
                else:
                    latest_2 += 'A'
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

file1 = open(sys.argv[1],"r")
file2 = open(sys.argv[2],"r")

print(sequence_alignment_brute(file1.read()[:-1],file2.read()[:-1],gap,order,mismatch))

