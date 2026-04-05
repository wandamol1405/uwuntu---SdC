#include "gini.h"
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

    float gini = calculate_gini(data, size);

    printf("GINI index: %f\n", gini);

    free(data);
    return 0;
}