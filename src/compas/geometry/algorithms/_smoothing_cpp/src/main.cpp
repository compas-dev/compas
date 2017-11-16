#include <vector>

// cd _smoothing_cpp
// g++ -shared -fPIC src/main.cpp -o smoothing.so

using namespace std;

extern "C"
{
    typedef void callback(int k);

    void smooth_centroid(int v, int *nbrs, int *fixed, double **vertices, int **neighbours, int kmax, callback func);
}

void smooth_centroid(int v, int *nbrs, int *fixed, double **vertices, int **neighbours, int kmax, callback func) 
{
    int k;
    int i;
    int j, n;
    double cx, cy, cz;

    vector< vector<double> > xyz(v, vector<double>(3, 0.0));

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
                n = neighbours[i][j];

                cx += xyz[n][0];
                cy += xyz[n][1];
                cz += xyz[n][2];
            }

            vertices[i][0] = cx / nbrs[i];
            vertices[i][1] = cy / nbrs[i];
            vertices[i][2] = cz / nbrs[i];
        }

        func(k);
    }
}
