
#include <gsl/gsl_math.h>
#include <gsl/gsl_vector.h>
#include <math.h>
#include <stdio.h>

void drx_solver_c(double tol, int steps, int summary, int m, int n, int *u, int *v, double *X, double *f0, double *l0, double *k0, int *ind_c, int *ind_t, int ind_c_n, int ind_t_n, double *B, double *P, double *S, int *rows, int *cols, double *vals, int nv, double *M, double factor, double *V, int *inds, int *indi, int *indf, double *EIx, double *EIy, int beams, int nb) {

    int a, b, c, i, j, k, ts;

    double f[m], fx[m], fy[m], fz[m];
    double frx[n], fry[n], frz[n];
    double l;
    double Mi;
    double q;
    double res;
    double Rx, Ry, Rz, Rn;
    double Un, Uo;
    double xd, yd, zd;

    gsl_vector * Xs = gsl_vector_alloc(3);
    gsl_vector * Xi = gsl_vector_alloc(3);
    gsl_vector * Xf = gsl_vector_alloc(3);
    gsl_vector * Qa = gsl_vector_alloc(3);
    gsl_vector * Qb = gsl_vector_alloc(3);
    gsl_vector * Qc = gsl_vector_alloc(3);

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
            l = gsl_hypot3(xd, yd, zd);
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

        if (beams) {
            for (i = 0; i < nb; i++) {
                a = inds[i] * 3;
                b = indi[i] * 3;
                c = indf[i] * 3;
                for (j = 0; j < 3; j++) {
                    gsl_vector_set(Xs, j, X[a + j]);
                    gsl_vector_set(Xi, j, X[b + j]);
                    gsl_vector_set(Xf, j, X[c + j]);
                }
                gsl_vector_memcpy(Qa, Xi);
                gsl_vector_sub(Qa, Xs);
            //     Qb = Xf - Xi
            //     Qc = Xf - Xs
            //     Qn = cross(Qa, Qb)
            //     mu = 0.5 * (Xf - Xs)
            //     La = length(Qa)
            //     Lb = length(Qb)
            //     Lc = length(Qc)
            //     LQn = length(Qn)
            //     Lmu = length(mu)
            //     a = arccos((La**2 + Lb**2 - Lc**2) / (2 * La * Lb))
            //     k = 2 * sin(a) / Lc
            //     ex = Qn / LQn
            //     ez = mu / Lmu
            //     ey = cross(ez, ex)
            //     K = k * Qn / LQn
            //     Kx = dot(K, ex) * ex
            //     Ky = dot(K, ey) * ey
            //     Mc = EIx[i] * Kx + EIy[i] * Ky
            //     cma = cross(Mc, Qa)
            //     cmb = cross(Mc, Qb)
            //     ua = cma / length(cma)
            //     ub = cmb / length(cmb)
            //     c1 = cross(Qa, ua)
            //     c2 = cross(Qb, ub)
            //     Lc1 = length(c1)
            //     Lc2 = length(c2)
            //     Ms = Mc[0]**2 + Mc[1]**2 + Mc[2]**2
            //     Sa = ua * Ms * Lc1 / (La * dot(Mc, c1))
            //     Sb = ub * Ms * Lc2 / (Lb * dot(Mc, c2))
            //     # print(isnan(Sa))
            //     if isnan(Sa[0]) or isnan(Sb[0]):
            //         pass
            //     else:
            //         S[inds[i], :] += Sa
            //         S[indi[i], :] -= Sa + Sb
            //         S[indf[i], :] += Sb
            printf("%f %f %f\n", gsl_vector_get(Qa, 0), gsl_vector_get(Qa, 1), gsl_vector_get(Qa, 2));
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
            Rn += gsl_hypot3(Rx, Ry, Rz);
            Mi = M[i] * factor;
            V[j + 0] += Rx / Mi;
            V[j + 1] += Ry / Mi;
            V[j + 2] += Rz / Mi;
            Un += Mi * (gsl_pow_2(V[j + 0]) + gsl_pow_2(V[j + 1]) + gsl_pow_2(V[j + 2]));
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
