
#include <geometry/basic_c.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_vector.h>
#include <math.h>
#include <stdio.h>


// author:    Andrew Liew <liew@arch.ethz.ch>
// copyright: Copyright 2018, BLOCK Research Group - ETH Zurich
// license:   MIT License
// email:     liew@arch.ethz.ch


void drx_solver_c(
    double tol,
    int steps,
    int summary,
    int m,
    int n,
    int *u,
    int *v,
    double *X,
    double *f0,
    double *l0,
    double *k0,
    int *ind_c,
    int *ind_t,
    int ind_c_n,
    int ind_t_n,
    double *B,
    double *P,
    double *S,
    int *rows,
    int *cols,
    double *vals,
    int nv,
    double *M,
    double factor,
    double *V,
    int *inds,
    int *indi,
    int *indf,
    double *EIx,
    double *EIy,
    int beams,
    int nb)

    {

    int i;
    int j;
    int k;

    double f[m];
    double fx[m];
    double fy[m];
    double fz[m];
    double frx[n];
    double fry[n];
    double frz[n];

    gsl_vector *Xs = gsl_vector_alloc(3);
    gsl_vector *Xi = gsl_vector_alloc(3);
    gsl_vector *Xf = gsl_vector_alloc(3);
    gsl_vector *Qa = gsl_vector_alloc(3);
    gsl_vector *Qb = gsl_vector_alloc(3);
    gsl_vector *Qc = gsl_vector_alloc(3);
    gsl_vector *Qn = gsl_vector_alloc(3);
    gsl_vector *mu = gsl_vector_alloc(3);
    gsl_vector *ex = gsl_vector_alloc(3);
    gsl_vector *ey = gsl_vector_alloc(3);
    gsl_vector *ez = gsl_vector_alloc(3);
    gsl_vector *K  = gsl_vector_alloc(3);
    gsl_vector *Kx = gsl_vector_alloc(3);
    gsl_vector *Ky = gsl_vector_alloc(3);
    gsl_vector *Mc = gsl_vector_alloc(3);
    gsl_vector *ua = gsl_vector_alloc(3);
    gsl_vector *ub = gsl_vector_alloc(3);
    gsl_vector *c1 = gsl_vector_alloc(3);
    gsl_vector *c2 = gsl_vector_alloc(3);

    int    ts = 0;
    double Uo = 0.;
    double res = 1000. * tol;

    while (ts <= steps && res > tol)
    {
        for (i = 0; i < m; i++)
        {
            j = 3 * v[i];
            k = 3 * u[i];
            double xd = X[j + 0] - X[k + 0];
            double yd = X[j + 1] - X[k + 1];
            double zd = X[j + 2] - X[k + 2];
            double l  = gsl_hypot3(xd, yd, zd);

            f[i] = f0[i] + k0[i] * (l - l0[i]);
            double q = f[i] / l;
            fx[i] = xd * q;
            fy[i] = yd * q;
            fz[i] = zd * q;
        }

        if (ind_t_n > 0)
        {
            for (i = 0; i < ind_t_n; i++)
            {
                if (f[i] < 0)
                {
                    fx[i] = 0;
                    fy[i] = 0;
                    fz[i] = 0;
                }
            }
        }

        if (ind_c_n > 0)
        {
            for (i = 0; i < ind_c_n; i++)
            {
                if (f[i] > 0)
                {
                    fx[i] = 0;
                    fy[i] = 0;
                    fz[i] = 0;
                }
            }
        }

        if (beams)
        {
            for (i = 0; i < n; i++)
            {
                j = i * 3;
                S[j + 0] = 0.;
                S[j + 1] = 0.;
                S[j + 2] = 0.;
            }

            for (i = 0; i < nb; i++)
            {
                int a = inds[i] * 3;
                int b = indi[i] * 3;
                int c = indf[i] * 3;

                vector_from_pointer(&X[a], Xs);
                vector_from_pointer(&X[b], Xi);
                vector_from_pointer(&X[c], Xf);
                subtract_vectors(Xi, Xs, Qa);
                subtract_vectors(Xf, Xi, Qb);
                subtract_vectors(Xf, Xs, Qc);
                cross_vectors(Qa, Qb, Qn);
                subtract_vectors(Xf, Xs, mu);
                scale_vector(mu, 0.5);

                double La  = length_vector(Qa);
                double Lb  = length_vector(Qb);
                double Lc  = length_vector(Qc);
                double LQn = length_vector(Qn);
                double Lmu = length_vector(mu);
                double alpha = acos((gsl_pow_2(La) + gsl_pow_2(Lb) - gsl_pow_2(Lc)) / (2. * La * Lb));
                double kappa = 2. * sin(alpha) / Lc;

                gsl_vector_memcpy(ex, Qn);
                gsl_vector_memcpy(ez, mu);
                scale_vector(ex, 1./LQn);
                scale_vector(ez, 1./Lmu);
                cross_vectors(ez, ex, ey);
                gsl_vector_memcpy(K, Qn);
                scale_vector(K, kappa/LQn);
                gsl_vector_memcpy(Kx, ex);
                gsl_vector_memcpy(Ky, ey);
                scale_vector(Kx, dot_vectors(K, ex));
                scale_vector(Ky, dot_vectors(K, ey));
                scale_vector(Kx, EIx[i]);
                scale_vector(Ky, EIy[i]);
                add_vectors(Kx, Ky, Mc);
                cross_vectors(Mc, Qa, ua);
                cross_vectors(Mc, Qb, ub);
                normalize_vector(ua);
                normalize_vector(ub);
                cross_vectors(Qa, ua, c1);
                cross_vectors(Qb, ub, c2);

                double Lc1 = length_vector(c1);
                double Lc2 = length_vector(c2);
                double Ms  = length_vector_squared(Mc);
                scale_vector(ua, Ms * Lc1 / (La * dot_vectors(Mc, c1)));
                scale_vector(ub, Ms * Lc2 / (Lb * dot_vectors(Mc, c2)));

                int nans = 0;

                for (j = 0; j < 3; j++)
                {
                    if (gsl_isnan(gsl_vector_get(ua, j)) || gsl_isnan(gsl_vector_get(ub, j)))
                    {
                        nans = 1;
                        break;
                    }
                }

                if (nans == 0)
                {
                    for (j = 0; j < 3; j++)
                    {
                        S[a + j] += gsl_vector_get(ua, j);
                        S[b + j] -= (gsl_vector_get(ua, j) + gsl_vector_get(ub, j));
                        S[c + j] += gsl_vector_get(ub, j);
                    }
                }

            }
        }

        for (i = 0; i < n; i++)
        {
            frx[i] = 0;
            fry[i] = 0;
            frz[i] = 0;
        }

        for (i = 0; i < nv; i++)
        {
            frx[rows[i]] += vals[i] * fx[cols[i]];
            fry[rows[i]] += vals[i] * fy[cols[i]];
            frz[rows[i]] += vals[i] * fz[cols[i]];
        }

        double Un = 0.;
        double Rn = 0.;

        for (i = 0; i < n; i++)
        {
            j = 3 * i;
            double Rx = (P[j + 0] - S[j + 0] - frx[i]) * B[j + 0];
            double Ry = (P[j + 1] - S[j + 1] - fry[i]) * B[j + 1];
            double Rz = (P[j + 2] - S[j + 2] - frz[i]) * B[j + 2];
            double Mi = M[i] * factor;
            Rn += gsl_hypot3(Rx, Ry, Rz);
            V[j + 0] += Rx / Mi;
            V[j + 1] += Ry / Mi;
            V[j + 2] += Rz / Mi;
            Un += Mi * (gsl_pow_2(V[j + 0]) + gsl_pow_2(V[j + 1]) + gsl_pow_2(V[j + 2]));
        }

        if (Un < Uo)
        {
            for (i = 0; i < n; i++)
            {
                j = 3 * i;
                V[j + 0] = 0.;
                V[j + 1] = 0.;
                V[j + 2] = 0.;
            }
        }

        Uo = Un;

        for (i = 0; i < n; i++)
        {
            j = 3 * i;
            X[j + 0] += V[j + 0];
            X[j + 1] += V[j + 1];
            X[j + 2] += V[j + 2];
        }

        res = Rn / n;
        ts++;

    }

    if (summary == 1)
    {
        printf("Step: %i, Residual: %f\n", ts - 1, res);
    }

}
