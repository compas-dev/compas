#include <vector>

// cd _smoothing_cpp
// g++ -shared -fPIC src/main.cpp -o smoothing.so

typedef void callback(int k);
extern "C" void smooth_centroid(int v, int *nbrs, int *fixed, double **vertices, int **neighbors, int kmax, callback func);


void smooth_centroid(int v, int *nbrs, int *fixed, double **vertices, int **neighbors, int kmax, callback func) 
{
    int k;
    int i;
    int j, n;
    double cx, cy, cz;

    double xyz[v][3];

    for (k = 0; k < kmax; k++) {

        for (i = 0; i < v; i++) {
            xyz[i][0] = vertices[i][0];
            xyz[i][1] = vertices[i][1];
            xyz[i][2] = vertices[i][2];
        }

        for (i = 0; i < v; i++) {

            if (fixed[i]) {
                continue;
            }

            cx = 0.0;
            cy = 0.0;
            cz = 0.0;

            for (j = 0; j < nbrs[i]; j++) {
                n = neighbors[i][j];

                cx += xyz[n][0];
                cy += xyz[n][1];
                cz += xyz[n][2];
            }

            vertices[i][0] = cx / (float)nbrs[i];
            vertices[i][1] = cy / (float)nbrs[i];
            vertices[i][2] = cz / (float)nbrs[i];
        }

        func(k);
    }
}
