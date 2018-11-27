
#include <stdio.h>


__global__ void add(float *a, float *b, float *c)
{
    int id = threadIdx.x;

    c[id] = a[id] + b[id];
}


int main()
{
    float a[] = {1., 2., 3.};
    float b[] = {4., 5., 6.};
    float c[3];
    float *a_;
    float *b_;
    float *c_;

    int size = 3 * sizeof(float);

    cudaMalloc((void**) &a_, size);
    cudaMalloc((void**) &b_, size);
    cudaMalloc((void**) &c_, size);

    cudaMemcpy(a_, a, size, cudaMemcpyHostToDevice);
    cudaMemcpy(b_, b, size, cudaMemcpyHostToDevice);

    dim3 dimGrid(1, 1, 1);
    dim3 dimBlock(3, 1, 1);
    add <<< dimGrid, dimBlock >>> (a_, b_, c_);

    cudaMemcpy(c, c_, size, cudaMemcpyDeviceToHost);

    cudaFree(a_);
    cudaFree(b_);
    cudaFree(c_);

    printf("%f %f %f\n", c[0], c[1], c[2]);
}
