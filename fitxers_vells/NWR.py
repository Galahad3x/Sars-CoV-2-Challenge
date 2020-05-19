import sys

gap = 7
order = { 'A': 0, 'G': 1, 'C': 2, 'T': 3}
mismatch = [[0,2,3,4],
            [2,0,5,1],
            [3,5,0,1],
            [4,3,1,0]]

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
            
            matriu = calculate_pos(matriu, len(sequence_1), len(sequence_2), sequence_1, sequence_2, order, mismatch, gap, None, return_traceback)

            print(matriu[len(sequence_1)][len(sequence_2)])
            return matriu[len(sequence_1)][len(sequence_2)]
    except RecursionError:
        print("Maximum recursion depth exceeded")


file1 = open(sys.argv[1],"r")
file2 = open(sys.argv[2],"r")

print(sequence_alignment_dynamic_2(file1.read()[:-1],file2.read()[:-1],gap,order,mismatch,False))
