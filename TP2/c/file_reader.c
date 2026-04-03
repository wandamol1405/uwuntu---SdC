#include <stdio.h>
#include <stdlib.h>
#include "file_reader.h"

float* read_data(const char* path, int* size) {

    FILE* file = fopen(path, "r");

    if (file == NULL) {
        perror("Error opening file");
        return NULL;
    }

    int capacity = 10;
    int count = 0;

    float* data = malloc(capacity * sizeof(float));

    if (data == NULL) {
        perror("Memory allocation failed");
        fclose(file);
        return NULL;
    }

    char line[100];

    while (fgets(line, sizeof(line), file)) {

        float value = strtof(line, NULL);

        if (count >= capacity) {
            capacity *= 2;

            float* temp = realloc(data, capacity * sizeof(float));

            if (temp == NULL) {
                perror("Realloc failed");
                free(data);
                fclose(file);
                return NULL;
            }

            data = temp;
        }

        data[count++] = value;
    }

    fclose(file);

    *size = count;

    return data;
}