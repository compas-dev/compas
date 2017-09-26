// compile with
// g++ -shared -fPIC test.cpp -o test.so

#include <stdio.h>
#include <math.h>

#define DLLEXPORT extern "C"
// #define DLLEXPORT extern "C" __declspec(dllexport)

typedef void callback1(int i);

typedef void callback2(int i, double l);

DLLEXPORT void test(int k, callback1 func);

DLLEXPORT int length(int m, double **vertices, double *lengths, callback2 func);



void test(int k, callback1 func)
{
    int i;

    for (i = 0; i < k; i++) {

        func(i);
    }
}


int length(int m, double **vertices, double *lengths, callback2 func) {

    int i;
    double x, y, z;
    double l;

    for (i = 0; i < m; i++) {

        x = vertices[i][0];
        y = vertices[i][1];
        z = vertices[i][2];
        l = sqrt(pow(x, 2.0) + pow(y, 2.0) + pow(z, 2.0));

        lengths[i] = l;

        func(i, l);
    }

    return 0;
}
