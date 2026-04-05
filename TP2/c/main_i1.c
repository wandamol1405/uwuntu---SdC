// c/main_i1.c

#include "file_reader.h"
#include <stdio.h>
#include <stdlib.h>

// Función de procesamiento (simula ASM)
int process_value(float value) { return (int)value + 1; }

int main() {
  int size;

  float *data = read_data("data/gini_values.txt", &size);

  if (data == NULL) {
    printf("Error reading file\n");
    return 1;
  }

  printf("Processed values:\n");

  for (int i = 0; i < size; i++) {
    int result = process_value(data[i]);
    printf("%d\n", result);
  }

  free(data);
  return 0;
}