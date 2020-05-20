#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int min(int a,int b);
void sequenceAlignmentSimple(char sequence1[], char sequence2[], int returnTraceback);
int orderFunction(char character);
void reverse(char *s);
int string_length(char *pointer);


int main(int argc, char *argv[]) {
	FILE *file1 = fopen(argv[1], "r");
	char sequence1[30000];
	fgets(sequence1, 30000, file1);
	sequence1[strlen(sequence1) - 1] = '\0';
	FILE *file2 = fopen(argv[2], "r");
	char sequence2[30000];
	fgets(sequence2, 30000, file2);
	sequence2[strlen(sequence2) - 1] = '\0';
	sequenceAlignmentSimple(sequence1, sequence2, 0);
}


void sequenceAlignmentSimple(char sequence1[], char sequence2[], int returnTraceback) {
    int gap = 7;
    int miss_match[][4] = {{0,2,3,4}, {2,0,5,1}, {3,5,0,1}, {4,3,1,0}};
    int top_line[strlen(sequence2) + 1];
    int current_line[strlen(sequence2) + 1];
    int miss_match_value;
    int current_min;

    top_line[0] = 0;

	for (int i = 1; i < strlen(sequence2) + 1; i++) {
		top_line[i] = top_line[i-1] + gap;
	}

	for (int i = 0; i < strlen(sequence1); i++) {
        printf("%i\n",i);
        current_line[0] = top_line[0]+gap;
		for (int j = 0; j < strlen(sequence2); j++) {
			if (sequence1[i] == 'N' || sequence2[j] == 'N') {
				miss_match_value = top_line[j];
			} else {
				miss_match_value = top_line[j] + miss_match[orderFunction(sequence1[i])][orderFunction(sequence2[j])];
			}
			current_min = min(min(current_line[j] + gap, top_line[j + 1] + gap), miss_match_value);
			current_line[j + 1] = current_min;
		}
        for (int j = 0; j < strlen(sequence2) + 1; j++){
            top_line[j] = current_line[j];
        }
	}
    printf("%i\n",top_line[strlen(sequence2)]);
}

int min(int a,int b) {
    if(a < b) {
        return a;
    }
    return b;
}

int orderFunction(char character) {
	if (character == 'A') {
        return 0;    
    } else if (character == 'G') {
        return 1;
    } else if (character == 'C') {
        return 2;
    } else {
        return 3;
    }
}
