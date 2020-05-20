import sys

gap = 7
order = { 'A': 0, 'G': 1, 'C': 2, 'T': 3}
mismatch = [[0,2,3,4],
            [2,0,5,1],
            [3,5,0,1],
            [4,3,1,0]]

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
        
        return matriu[len(sequence_1)][len(sequence_2)]

file1 = open(sys.argv[1],"r")
file2 = open(sys.argv[2],"r")

print(sequence_alignment_dynamic(file1.read()[:-1],file2.read()[:-1],gap,order,mismatch,False))
