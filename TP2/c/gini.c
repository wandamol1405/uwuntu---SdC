#include <stdio.h>
#include <math.h>
#include "gini.h"

float calculate_gini(float* data, int size) {

    if (size == 0) return 0.0;

    // 1. Calcular media
    float sum = 0.0;
    for (int i = 0; i < size; i++) {
        sum += data[i];
    }

    float mean = sum / size;

    if (mean == 0) return 0.0;

    // 2. Doble sumatoria
    float diff_sum = 0.0;

    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            diff_sum += fabs(data[i] - data[j]);
        }
    }

    // 3. Fórmula final
    float gini = diff_sum / (2 * size * size * mean);

    return gini;
}