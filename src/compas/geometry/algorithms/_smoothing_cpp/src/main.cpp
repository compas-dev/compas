#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <array>
#include <vector>

using namespace std;

extern "C"
{
    typedef void callback_smoothing(int k);

    void smooth_centroid(int v, int *nbrs, int *fixed, double **vertices, int **neighbours, int kmax, callback_smoothing func);
}

void smooth_centroid(int v, int *nbrs, int *fixed, double **vertices, int **neighbours, int kmax, callback_smoothing func) 
{
    int i, j, n, k;
    double cx, cy, cz;
    double c;

    vector<vector<double>> xyz(v, vector<double>(3, 0.0));


    for (k = 0; k < kmax; k++) {

        for (i = 0; i < v; i++) {
            xyz[i][0] = vertices[i][0];
            xyz[i][1] = vertices[i][1];
            xyz[i][2] = vertices[i][2];
        }

        for (i = 0; i < v; i++) {
            cx = 0.0;
            cy = 0.0;
            cz = 0.0;

            c = 0.0;

            for (j = 0; j < nbrs[i]; j++) {
                n = neighbours[i][j];

                cx += xyz[n][0];
                cy += xyz[n][1];
                cz += xyz[n][2];

                c += 1.0;
            }

            if (! fixed[i]) {
                vertices[i][0] = cx / c;
                vertices[i][1] = cy / c;
                vertices[i][2] = cz / c;
            }
        }

        func(k);
    }
}
