
#include <gsl/gsl_blas.h>
#include <gsl/gsl_vector.h>


// author:    Andrew Liew <liew@arch.ethz.ch>
// copyright: Copyright 2018, BLOCK Research Group - ETH Zurich
// license:   MIT License
// email:     liew@arch.ethz.ch


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


void scale_vector(gsl_vector *u, double a) {

    gsl_vector_scale(u, a);

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


void cross_vectors(const gsl_vector *u, const gsl_vector *v, gsl_vector *w) {

    double w1 = gsl_vector_get(u, 1) * gsl_vector_get(v, 2) - gsl_vector_get(u, 2) * gsl_vector_get(v, 1);
    double w2 = gsl_vector_get(u, 2) * gsl_vector_get(v, 0) - gsl_vector_get(u, 0) * gsl_vector_get(v, 2);
    double w3 = gsl_vector_get(u, 0) * gsl_vector_get(v, 1) - gsl_vector_get(u, 1) * gsl_vector_get(v, 0);

    gsl_vector_set(w, 0, w1);
    gsl_vector_set(w, 1, w2);
    gsl_vector_set(w, 2, w3);

}
