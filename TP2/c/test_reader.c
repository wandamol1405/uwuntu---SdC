#include <stdio.h>
#include <stdlib.h>
#include "file_reader.h"

int main() {
    int size;

    float* data = read_data("data/gini_data.txt", &size);

    if (data == NULL) {
        printf("Error reading file\n");
        return 1;
    }

    printf("Valores:\n");

    for (int i = 0; i < size; i++) {
        printf("%f\n", data[i]);
    }

    printf("Total: %d\n", size);

    free(data);
    return 0;
}