
#include <gsl/gsl_blas.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_vector.h>


// author:    Andrew Liew <liew@arch.ethz.ch>
// copyright: Copyright 2018, BLOCK Research Group - ETH Zurich
// license:   MIT License
// email:     liew@arch.ethz.ch


int i, j;


// ==========================================================================================================
// One vector
// ==========================================================================================================

void vector_from_pointer(double *ptr, gsl_vector *w) {

    gsl_vector_set(w, 0, *(ptr + 0));
    gsl_vector_set(w, 1, *(ptr + 1));
    gsl_vector_set(w, 2, *(ptr + 2));

}


double length_vector(gsl_vector *u) {

    double L = gsl_blas_dnrm2(u);

    return L;

}


double length_vector_squared(gsl_vector *u) {

    double a;

    a = 0.;

    for (i = 0; i < 3; i++) {
        a += gsl_pow_2(gsl_vector_get(u, i));
    }

    return a;

}


void scale_vector(gsl_vector *u, double a) {

    gsl_vector_scale(u, a);

}


void normalise_vector(gsl_vector *u) {

    gsl_vector_scale(u, 1./length_vector(u));

}


// ==========================================================================================================
// Two vectors
// ==========================================================================================================

void add_vectors(const gsl_vector *u, const gsl_vector *v, gsl_vector *w) {

    gsl_vector_memcpy(w, u);
    gsl_vector_add(w, v);

}


void subtract_vectors(const gsl_vector *u, const gsl_vector *v, gsl_vector *w) {

    gsl_vector_memcpy(w, u);
    gsl_vector_sub(w, v);

}


double dot_vectors(const gsl_vector *u, const gsl_vector *v) {

    double a;

    a = 0.;

    for (i = 0; i < 3; i++) {
        a += gsl_vector_get(u, i) * gsl_vector_get(v, i);
    }

    return a;

}


void cross_vectors(const gsl_vector *u, const gsl_vector *v, gsl_vector *w) {

    double w1 = gsl_vector_get(u, 1) * gsl_vector_get(v, 2) - gsl_vector_get(u, 2) * gsl_vector_get(v, 1);
    double w2 = gsl_vector_get(u, 2) * gsl_vector_get(v, 0) - gsl_vector_get(u, 0) * gsl_vector_get(v, 2);
    double w3 = gsl_vector_get(u, 0) * gsl_vector_get(v, 1) - gsl_vector_get(u, 1) * gsl_vector_get(v, 0);

    gsl_vector_set(w, 0, w1);
    gsl_vector_set(w, 1, w2);
    gsl_vector_set(w, 2, w3);

}
