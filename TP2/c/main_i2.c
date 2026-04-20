// c/main_i2.c

#include "file_reader.h"
#include <stdio.h>
#include <stdlib.h>

extern int process_value_asm(float value);

int main() {
  int size;
  printf("C layer OK\n");

  float *data = read_data("data/gini_values.txt", &size);
  if (!data) {
    perror("Error leyendo los datos");
    return 1;
  }

  float value;
  for (int i = 0; i < size; i++) {
    value = data[i];
    int result = process_value_asm(value);
    printf("%d\n", result);
  }

  free(data);
  return 0;
}
