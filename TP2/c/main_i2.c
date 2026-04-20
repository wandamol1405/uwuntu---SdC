// c/main_i2.c

#include "file_reader.h"
#include <stdio.h>
#include <stdlib.h>

extern int process_value_asm(float value);

int main(void)
{
  int size = 0;

  printf("=== TP2 | Procesamiento de datos ===\n");
  printf("Leyendo archivo: data/gini_values.txt\n");

  float *data = read_data("data/gini_values.txt", &size);
  if (!data)
  {
    fprintf(stderr, "ERROR: no se pudieron leer los datos del archivo.\n");
    return 1;
  }

  printf("Lectura correcta. Cantidad de elementos: %d\n", size);
  printf("====================================\n");
  printf("%-6s | %-12s | %-10s\n", "Index", "Valor", "Resultado");
  printf("--------+--------------+-----------\n");

  for (int i = 0; i < size; i++)
  {
    float value = data[i];
    int result = process_value_asm(value);
    printf("%-6d | %-12.6f | %-10d\n", i, value, result);
  }

  printf("====================================\n");
  printf("Procesamiento finalizado.\n");

  free(data);
  return 0;
}
