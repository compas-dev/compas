
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
    double tol,    // Tolerance value.
    int steps,     // Maximum number of steps.
    int summary,   // Print summary at end (1:yes or 0:no).
    int m,         // Number of elements.
    int n,         // Number of nodes.
    int *u,        // Element start node.
    int *v,        // Element end node.
    double *X,     // Nodal co-ordinates.
    double *f0,    // Initial edge forces.
    double *l0,    // Initial edge lengths.
    double *k0,    // Initial edge axial stiffnesses.
    int *ind_c,    // Indices of compression only edges.
    int *ind_t,    // Indices of tension only edges.
    int ind_c_n,   // Length of ind_c.
    int ind_t_n,   // Length of ind_t.
    double *B,     // Constraint conditions Bx, By, Bz.
    double *P,     // Nodal loads Px, Py, Pz.
    double *S,     // Shear forces Sx, Sy, Sz.
    int *rows,     // Rows of Ct.
    int *cols,     // Columns of Ct.
    double *vals,  // Values of Ct.
    int nv,        // Length of rows/cols/vals.
    double *M,     // Mass matrix.
    double factor, // Convergence factor.
    double *V,     // Nodal velocities Vx, Vy, Vz.
    int *inds,     // Indices of beam element start nodes.
    int *indi,     // Indices of beam element intermediate nodes.
    int *indf,     // Indices of beam element finish nodes beams.
    double *EIx,   // Nodal EIx flexural stiffnesses.
    double *EIy,   // Nodal EIy flexural stiffnesses.
    int beams,     // Includes beams:1 or not:0.
    int nb)        // Length of inds/indi/indf.

    {

    int a;
    int b;
    int c;
    int i;
    int j;
    int k;
    int nans[nb];
    int ts;

    double alpha;
    double f[m];
    double fx[m];
    double fy[m];
    double fz[m];
    double frx[n];
    double fry[n];
    double frz[n];
    double kappa;
    double l;
    double La;
    double Lb;
    double Lc;
    double LQn;
    double Lmu;
    double Lc1;
    double Lc2;
    double Mi;
    double Ms;
    double q;
    double res;
    double Rx;
    double Ry;
    double Rz;
    double Rn;
    double Uo;
    double Un;
    double xd;
    double yd;
    double zd;

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
    gsl_matrix *Sa = gsl_matrix_alloc(nb, 3);
    gsl_matrix *Sb = gsl_matrix_alloc(nb, 3);

    ts  = 0;
    Uo  = 0.;
    res = 1000. * tol;

    while (ts <= steps && res > tol)
    {
        #pragma omp parallel for private(i,j,k,xd,yd,zd,l,q)
        for (i = 0; i < m; i++)
        {
            j = 3 * v[i];
            k = 3 * u[i];
            xd = X[j + 0] - X[k + 0];
            yd = X[j + 1] - X[k + 1];
            zd = X[j + 2] - X[k + 2];
            l  = gsl_hypot3(xd, yd, zd);
            f[i] = f0[i] + k0[i] * (l - l0[i]);
            q = f[i] / l;
            fx[i] = xd * q;
            fy[i] = yd * q;
            fz[i] = zd * q;
        }

        if (ind_t_n > 0)
        {
            #pragma omp parallel for private(i)
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
            #pragma omp parallel for private(i)
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
            #pragma omp parallel for private(i,j)
            for (i = 0; i < n; i++)
            {
                j = i * 3;
                S[j + 0] = 0.;
                S[j + 1] = 0.;
                S[j + 2] = 0.;
            }

            for (i = 0; i < nb; i++)
            {
                a = inds[i] * 3;
                b = indi[i] * 3;
                c = indf[i] * 3;

                vector_from_pointer(&X[a], Xs);
                vector_from_pointer(&X[b], Xi);
                vector_from_pointer(&X[c], Xf);
                subtract_vectors(Xi, Xs, Qa);
                subtract_vectors(Xf, Xi, Qb);
                subtract_vectors(Xf, Xs, Qc);
                cross_vectors(Qa, Qb, Qn);
                subtract_vectors(Xf, Xs, mu);
                scale_vector(mu, 0.5);

                La  = length_vector(Qa);
                Lb  = length_vector(Qb);
                Lc  = length_vector(Qc);
                LQn = length_vector(Qn);
                Lmu = length_vector(mu);
                alpha = acos((gsl_pow_2(La) + gsl_pow_2(Lb) - gsl_pow_2(Lc)) / (2. * La * Lb));
                kappa = 2. * sin(alpha) / Lc;

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

                Lc1 = length_vector(c1);
                Lc2 = length_vector(c2);
                Ms  = length_vector_squared(Mc);
                scale_vector(ua, Ms * Lc1 / (La * dot_vectors(Mc, c1)));
                scale_vector(ub, Ms * Lc2 / (Lb * dot_vectors(Mc, c2)));

                for (j = 0; j < 3; j++)
                {
                    gsl_matrix_set(Sa, i, j, gsl_vector_get(ua, j));
                    gsl_matrix_set(Sb, i, j, gsl_vector_get(ub, j));
                }
            }

            #pragma omp parallel for private(i,j)
            for (i = 0; i < nb; i++)
            {
                nans[i] = 0;
                for (j = 0; j < 3; j++)
                {
                    if (gsl_isnan(gsl_matrix_get(Sa, i, j)) || gsl_isnan(gsl_matrix_get(Sb, i, j)))
                    {
                        nans[i] = 1;
                        break;
                    }
                }
            }

            for (i = 0; i < nb; i++)
            {
                a = inds[i] * 3;
                b = indi[i] * 3;
                c = indf[i] * 3;

                if (nans[i] == 0)
                {
                    for (j = 0; j < 3; j++)
                    {
                        S[a + j] += gsl_matrix_get(Sa, i, j);
                        S[b + j] -= (gsl_matrix_get(Sa, i, j) + gsl_matrix_get(Sb, i, j));
                        S[c + j] += gsl_matrix_get(Sb, i, j);
                    }
                }
            }
        }

        #pragma omp parallel for private(i)
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

        Un = 0.;
        Rn = 0.;

        #pragma omp parallel for private(i,j,Rx,Ry,Rz,Mi) reduction(+:Un,Rn)
        for (i = 0; i < n; i++)
        {
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

        if (Un < Uo)
        {
            #pragma omp parallel for private(i,j)
            for (i = 0; i < n; i++)
            {
                j = 3 * i;
                V[j + 0] = 0.;
                V[j + 1] = 0.;
                V[j + 2] = 0.;
            }
        }

        Uo = Un;

        #pragma omp parallel for private(i,j)
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
