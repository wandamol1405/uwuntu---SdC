// c/main.c

#include <stdio.h>
#include <stdlib.h>

extern int process_value_asm(float value);

int main()
{
    printf("C layer OK\n");
    FILE *file = fopen("data/gini_values.txt", "r");
    if (!file) {
        perror("Error abriendo el archivo");
        return 1;
    }

    float value;
    while (fscanf(file, "%f", &value) == 1) {
        int result = process_value_asm(value);
        printf("%d\n", result);
    }

    fclose(file);
    return 0;
}
