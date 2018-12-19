#include <stdio.h>

// This is the bubble sort we all know and love
void bubbleSort(int* arr, int n){
	for ( int i = 0; i < n; i++){
		for (int j = 0; j < n-1; j++){
			if (arr[j] > arr[j+1]){
				int temp = arr[j];
				arr[j] = arr[j+1];
				arr[j+1] = temp;
			}
		}
	}
}

/* this is a block comment to test the deleted block comment feature for one line*/

/* Why not try
Many Lines! */

int main(){
	int workArr[10] = {9, 8, 7, 6, 5, 4, 3, 2, 1, 0};
	for ( int i = 0; i < 10; i++){
		printf("%d ", workArr[i]);
	}
	printf("\n");

	bubbleSort(workArr, 10);
	for ( int i = 0; i < 10; i++){
		printf("%d ", workArr[i]);
	}
	printf("\n");

}
