//g++ -fopenmp wind_maker.cpp -lrt -O3
#include <string.h>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <math.h>
#include <iostream>
#include <string>
#include <vector>
#include <omp.h>

using namespace std;
// give openMP a big stacksize to work with...
#define OMP_STACKSIZE 15G

// known height of 3 meters
double known_height = 3;

double estimate_speed(double known_speed, double known_height, double estimated_height)
{
    double estimated_speed;
    // alpha ~1/7 
    double alpha_coef = 1.0 / 7.0;
    estimated_speed = known_speed * pow( (estimated_height/known_height), alpha_coef);
    return estimated_speed; 
}


// cuda version of estimate speed
__global__ void estimate_speed_gpu(double *known_speed, double *known_height, double *estimated_height double *results)
{
    // use __shared___ to declare memory on device shared memory... mucho fasto -> __syncthreads() to synchronize
    // use __constant__  to store constant variable alpha
    // alpha ~1/7 
    __constant__ double alpha_coef = 1.0 / 7.0;

    // thread id's 
    int i = blockDim.x*blockIdx.x + threadIdx.x;
    // blockDim.x *   blockDim.y * blockDim.z * 
    results[i] = known_speed[i] * pow( (estimated_height[i]/known_height[i]), alpha_coef);
}


int main(int argc, char* argv[])
{
    //cudaGetDeviceCount(int *count)
    //cudaSetDevice(int device)
    //cudaGetDevice(int *device)
    //cudaGetDeviceProperties(cudaDeviceProp *prop, int device)
    if (argc != 3) 
    {
		cerr << "usage: ./progName wind_data.csv nthreads\n" << endl;
		exit(-1);
	}
    // open the file
    ifstream wind_file;
    wind_file.open (argv[1], ios::binary);
	if (!wind_file) {
		cerr << "file not found" << endl;
		exit(-1);
	}
    // open results file
    ofstream outfile;
    outfile.open("results.txt");
    if( !outfile ) 
    { 
        cerr << "Error: output file could not be opened" << endl;
        exit(1);
    }    
    // variable for reading in strings and header checking
    string row = "";
    int nthreads = atoi(argv[2]);
    int header_row = 0;
    int split_count = 0;
    char sep = ',';
    int max_height=100;
    string timestamp;
    // loop through the file 
    if (wind_file.is_open()) 
    {
        while (getline(wind_file,row)) 
        {
            header_row = row.find("HWS", 0);
            // filter all all header rows...
            if ( header_row == string::npos )
            {

                istringstream row_split( row );
                split_count = 0;
                while (!row_split.eof())
                {
                    string x;
                    // split on commas               
                    getline( row_split, x, ',' );
                    // grab timestamp from first row....  
                    if (split_count==0)
                    {
                        timestamp = x;
                    }
                    // split on the 26th comma for RG1 HWS
                    if (split_count==26)
                    {
                        double known_speed;
                        istringstream iss(x);
                        // string to double
                        iss >> known_speed;
                        // cout << known_speed << endl;
                        int i=2;
                        double results;
                        //#pragma omp parallel for num_threads(nthreads) private(i,results)
                        for ( i=2; i<=max_height; i++)
                        {
                            double estimated_height = (double) i;

                            // time for cuda code...
                            // use synchron or non...
                            //cudaMemcpyAsync()
                            // non sync transfer
                            //cudaMemcpy()
                            // synchronize gpu with cpu
                            cudaDeviceSynchronize()


                            results = estimate_speed(known_speed, known_height, estimated_height);
                            // blocking so threads can write to output file
                            #pragma omp critical
                            {
                                //cout << results << "\t" << estimated_height << "\n";
                                //outfile << timestamp << "\t" << results << "\t" << estimated_height << "\n";
                                double a;
                                a = results;
                            }
                        }
                    }
                    // increment split count
                    split_count += 1;
                }
            }
        }
    }
    // close up results file
    outfile.close();
    return 0;
}

