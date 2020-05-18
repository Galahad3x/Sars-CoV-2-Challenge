#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define min(a,b) \
	({ __typeof__ (a) _a = (a); \
			__typeof__ (b) _b = (b); \
		_a < _b ? _a : _b; })

int gap = 7;
int miss_match[][4] = {{0,2,3,4}, {2,0,5,1}, {3,5,0,1}, {4,3,1,0}};

void sequenceAlignmentDynamic(char sequence1[], char sequence2[], int returnTraceback);
int orderFunction(char character);

int main(int argc, char *argv[]) {
    printf("%s",argv[1]);
	FILE *file1 = fopen(argv[1], "r");
	char sequence1[30000];
	fgets((char *) sequence1, 30000, file1);
	sequence1[strlen(sequence1) - 1] = '\0';
	FILE *file2 = fopen(argv[2], "r");
	char sequence2[30000];
	fgets((char *) sequence2, 30000, file2);
	sequence2[strlen(sequence2) - 1] = '\0';
    printf("Hola bones");
	sequenceAlignmentDynamic(sequence1, sequence2, 0);
}


void sequenceAlignmentDynamic(char sequence1[], char sequence2[], int returnTraceback) {
	if (returnTraceback == 0) {
		int matriu[strlen(sequence1) + 1][strlen(sequence2) + 1];
		char matriuTraceback[strlen(sequence1) + 1][strlen(sequence2) + 1];
		int miss_match_value;
		int current_min;

		for (int i = 0; i < strlen(sequence1); i++) {
			matriu[i + 1][0] = matriu[i][0] + gap;
			matriuTraceback[i + 1][0] = 'u';
		}
		for (int i = 0; i < strlen(sequence2); i++) {
			matriu[0][i + 1] = matriu[0][i] + gap;
    	matriuTraceback[0][i + 1] = 'l';
		}

		for (int i = 0; i < strlen(sequence1) + 1; i++) {
			for (int j = 0; j < strlen(sequence2) + 1; j++) {
				if (sequence1[i] == 'N' || sequence2[j] == 'N') {
					miss_match_value = matriu[i][j];
				} else {
					miss_match_value = matriu[i][j] + miss_match[orderFunction(sequence1[i])][orderFunction(sequence2[j])];
				}
				current_min = min(min(matriu[i + 1][j] + gap, matriu[i][j + 1] + gap), miss_match_value);
				matriu[i + 1][j + 1] = current_min;
				if (current_min == matriu[i][j] + miss_match[orderFunction(sequence1[i])][orderFunction(sequence2[j])]) {
					matriuTraceback[i + 1][j + 1] = 'd';
				} else if (current_min == matriu[i + 1][j] + gap) {
					matriuTraceback[i + 1][j + 1] = 'l';
				} else {
					matriuTraceback[i + 1][ j + 1] = 'u';
				}
			}
		}
		int my_x = strlen(sequence1);
		int my_y = strlen(sequence2);

		char wres_1[] = "";
		char wres_2[] = "";

        char single_char[1];        

		while (matriuTraceback[my_x][my_y] != 'e') {
			if (matriuTraceback[my_x][my_y] == 'd') {
                single_char[0] = sequence2[my_y - 1]; 
				strcpy(wres_2,strcat(single_char, wres_2));
                single_char[0] = sequence1[my_x - 1]; 
				strcpy(wres_1,strcat(single_char, wres_1));
				my_x -= 1;
				my_y -= 1;
			} else if (matriuTraceback[my_x][my_y] == 'l') {
				single_char[0] = sequence2[my_y - 1]; 
				strcpy(wres_2,strcat(single_char, wres_2));
                single_char[0] = '-'; 
				strcpy(wres_1,strcat(single_char, wres_1));
				my_y -= 1;
			} else {
				single_char[0] = sequence1[my_x - 1]; 
				strcpy(wres_1,strcat(single_char, wres_1));
				my_x -= 1;
                single_char[0] = '-'; 
				strcpy(wres_2,strcat(single_char, wres_2));
			}
            printf("%s\n%s\n%i\n",wres_1,wres_2,matriu[strlen(sequence1)][strlen(sequence2)]);
		}
	} else {
		char matriu[] = "";

	}
}

int orderFunction(char character){
	if (character == 'A'){
        return 0;    
    }else if (character == 'G'){
        return 1;
    }else if (character == 'C'){
        return 2;
    }else{
        return 3;
    }
}
