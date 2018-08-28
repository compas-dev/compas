
#include <stdio.h>
// #include <stdlib.h>

#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif

// #define MEM_SIZE (128)
// #define MAX_SOURCE_SIZE (0x100000)

// __kernel void hello(__global char* string)
// {
//     string[0]  = 'H';
//     string[1]  = 'e';
//     string[2]  = 'l';
//     string[3]  = 'l';
//     string[4]  = 'o';
//     string[5]  = ',';
//     string[6]  = ' ';
//     string[7]  = 'W';
//     string[8]  = 'o';
//     string[9]  = 'r';
//     string[10] = 'l';
//     string[11] = 'd';
//     string[12] = '!';
//     string[13] = '\0';
// }


int main()
{
    cl_device_id *devices;
// cl_context context = NULL;
// cl_command_queue command_queue = NULL;
// cl_mem memobj = NULL;
// cl_program program = NULL;
// cl_kernel kernel = NULL;
    cl_platform_id platform = NULL;
    cl_uint num_devices = 0;

    char dname[40];
    char dvendor[40];

    int i;

    unsigned long dmemory;

// char string[MEM_SIZE];

// FILE *fp;
// char fileName[] = "./hello.cl";
// char *source_str;
// size_t source_size;

// /* Load the source code containing the kernel*/
// fp = fopen(fileName, "r");
// if (!fp) {
// fprintf(stderr, "Failed to load kernel.\n");
// exit(1);
// }
// source_str = (char*)malloc(MAX_SOURCE_SIZE);
// source_size = fread(source_str, 1, MAX_SOURCE_SIZE, fp);
// fclose(fp);

    clGetPlatformIDs(1, &platform, NULL);

    clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 10, NULL, &num_devices);
    devices = (cl_device_id*) malloc(sizeof(cl_device_id) * num_devices);
    clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, num_devices, devices, NULL);

    for (i = 0; i < num_devices; i++)
    {
        clGetDeviceInfo(devices[i], CL_DEVICE_NAME, sizeof(dname), &dname, NULL);
        clGetDeviceInfo(devices[i], CL_DEVICE_VENDOR, sizeof(dvendor), &dvendor, NULL);
        clGetDeviceInfo(devices[i], CL_DEVICE_GLOBAL_MEM_SIZE, sizeof(dmemory), &dmemory, NULL);

        printf("Device:%i - %s (%s) - Memory:%i MB\n", i, dname, dvendor, (int)(dmemory / 1.e6));
    }

// /* Create OpenCL context */
// context = clCreateContext(NULL, 1, &device_id, NULL, NULL, &ret);

// /* Create Command Queue */
// command_queue = clCreateCommandQueue(context, device_id, 0, &ret);

// /* Create Memory Buffer */
// memobj = clCreateBuffer(context, CL_MEM_READ_WRITE,MEM_SIZE * sizeof(char), NULL, &ret);

// /* Create Kernel Program from the source */
// program = clCreateProgramWithSource(context, 1, (const char **)&source_str,
// (const size_t *)&source_size, &ret);

// /* Build Kernel Program */
// ret = clBuildProgram(program, 1, &device_id, NULL, NULL, NULL);

// /* Create OpenCL Kernel */
// kernel = clCreateKernel(program, "hello", &ret);

// /* Set OpenCL Kernel Parameters */
// ret = clSetKernelArg(kernel, 0, sizeof(cl_mem), (void *)&memobj);

// /* Execute OpenCL Kernel */
// ret = clEnqueueTask(command_queue, kernel, 0, NULL,NULL);

// /* Copy results from the memory buffer */
// ret = clEnqueueReadBuffer(command_queue, memobj, CL_TRUE, 0,
// MEM_SIZE * sizeof(char),string, 0, NULL, NULL);

// /* Display Result */
// puts(string);

// /* Finalization */
// ret = clFlush(command_queue);
// ret = clFinish(command_queue);
// ret = clReleaseKernel(kernel);
// ret = clReleaseProgram(program);
// ret = clReleaseMemObject(memobj);
// ret = clReleaseCommandQueue(command_queue);
// ret = clReleaseContext(context);

// free(source_str);

    return 0;
}
