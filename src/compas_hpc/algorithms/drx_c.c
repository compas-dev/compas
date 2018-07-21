
#include <math.h>
#include <stdio.h>

int drx_solver_c(double tol, int steps, int summary, int m, int n, int *u, int *v, double *X, double *f0, double *l0, double *k0, int *ind_c, int *ind_t, int ind_c_n, int ind_t_n) {

    int j;
    int ts = 0;

    double f[m];
    double fx[m];
    double fy[m];
    double fz[m];
    double q;
    double res = 1000. * tol;
    double Uo = 0.;

    while ((ts <= steps) && (res > tol)) {

        for (int i = 0; i < m; i++) {

            double xd = X[3 * v[i] + 0] - X[3 * u[i] + 0];
            double yd = X[3 * v[i] + 1] - X[3 * u[i] + 1];
            double zd = X[3 * v[i] + 2] - X[3 * u[i] + 2];
            double l = sqrt(pow(xd, 2) + pow(yd, 2) + pow(zd, 2));

            f[i] = f0[i] + k0[i] * (l - l0[i]);
            q = f[i] / l;
            fx[i] = xd * q;
            fy[i] = yd * q;
            fz[i] = zd * q;

            if (ind_t_n > 0) {
                for (j = 0; j < ind_t_n; j++) {
                    printf("%i\n", ind_t[j]);
                }
            }

            if (ind_c_n > 0) {
                for (j = 0; j < ind_c_n; j++) {
                    printf("%i\n", ind_c[j]);
                }
            }

            // printf("%f\n", l);
        }

        ts++;

    }

    return 0;

}
