
#include <math.h>
#include <stdio.h>

void drx_solver_c(double tol, int steps, int summary, int m, int n, int *u, int *v, double *X, double *f0, double *l0, double *k0, int *ind_c, int *ind_t, int ind_c_n, int ind_t_n, double *B, double *P, double *S, int *rows, int *cols, double *vals, int nv, double *M, double factor, double *V) {

    int i;
    int j;
    int k;
    int ts;

    double f[m];
    double fx[m];
    double fy[m];
    double fz[m];
    double frx[n];
    double fry[n];
    double frz[n];
    double l;
    double Mi;
    double q;
    double res;
    double Rx;
    double Ry;
    double Rz;
    double Rn;
    double Un;
    double Uo;
    double xd;
    double yd;
    double zd;

    ts = 0;
    Uo = 0.;
    res = 1000. * tol;

    while ((ts <= steps) && (res > tol)) {

        for (i = 0; i < m; i++) {
            j = 3 * v[i];
            k = 3 * u[i];
            xd = X[j + 0] - X[k + 0];
            yd = X[j + 1] - X[k + 1];
            zd = X[j + 2] - X[k + 2];
            l = sqrt(pow(xd, 2) + pow(yd, 2) + pow(zd, 2));
            f[i] = f0[i] + k0[i] * (l - l0[i]);
            q = f[i] / l;
            fx[i] = xd * q;
            fy[i] = yd * q;
            fz[i] = zd * q;
        }

        if (ind_t_n > 0) {
            for (i = 0; i < ind_t_n; i++) {
                if (f[i] < 0) {
                    fx[i] = 0;
                    fy[i] = 0;
                    fz[i] = 0;
                }
            }
        }

        if (ind_c_n > 0) {
            for (i = 0; i < ind_c_n; i++) {
                if (f[i] > 0) {
                    fx[i] = 0;
                    fy[i] = 0;
                    fz[i] = 0;
                }
            }
        }

        for (i = 0; i < n; i++) {
            frx[i] = 0;
            fry[i] = 0;
            frz[i] = 0;
        }

        for (i = 0; i < nv; i++) {
            frx[rows[i]] += vals[i] * fx[cols[i]];
            fry[rows[i]] += vals[i] * fy[cols[i]];
            frz[rows[i]] += vals[i] * fz[cols[i]];
        }

        Un = 0.;
        Rn = 0.;

        for (i = 0; i < n; i++) {
            j = 3 * i;
            Rx = (P[j + 0] - S[j + 0] - frx[i]) * B[j + 0];
            Ry = (P[j + 1] - S[j + 1] - fry[i]) * B[j + 1];
            Rz = (P[j + 2] - S[j + 2] - frz[i]) * B[j + 2];
            Rn += sqrt(pow(Rx, 2) + pow(Ry, 2) + pow(Rz, 2));
            Mi = M[i] * factor;
            V[j + 0] += Rx / Mi;
            V[j + 1] += Ry / Mi;
            V[j + 2] += Rz / Mi;
            Un += Mi * (pow(V[j + 0], 2) + pow(V[j + 1], 2) + pow(V[j + 2], 2));
        }

        if (Un < Uo) {
            for (i = 0; i < n; i++) {
                j = 3 * i;
                V[j + 0] = 0.;
                V[j + 1] = 0.;
                V[j + 2] = 0.;
            }
        }

        Uo = Un;

        for (i = 0; i < n; i++) {
            j = 3 * i;
            X[j + 0] += V[j + 0];
            X[j + 1] += V[j + 1];
            X[j + 2] += V[j + 2];
        }

        res = Rn / n;
        ts++;

    }

    if (summary == 1) {
        printf("Step: %i, Residual: %f\n", ts - 1, res);
    }

}
