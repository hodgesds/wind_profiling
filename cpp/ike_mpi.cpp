//
// Andrew Borgman
// Serial version of wind power profile law coefficient finder
// Use both anenometer values and data from 6 sensors to come up with 
// consensus coefficient estimate for each observation.
// Here's the sesor heights:
// Average Horizontal Wind Speed 75m
// Average Horizontal Wind Speed 90m
// Average Horizontal Wind Speed 105m
// Average Horizontal Wind Speed 125m
// Average Horizontal Wind Speed 150m
// Average Horizontal Wind Speed 175m
// '12/01/05 18:39:20\t7.2\t7.8\t8.2\t8\t7.6\t7.7\t5.219\t5.476\n'
// 22,740,021 obs.

//g++ -fopenmp hw7_3.cpp 
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <sys/types.h>
#include <dirent.h>
#include <errno.h>
#include <vector>
#include <sstream>
#include <string>
#include <fstream>
#include <math.h>
 #include <string.h>
using namespace std;
#define OMP_STACKSIZE 15G
// default stack size for openmp sucks
// type this in bash so you stop getting overflows
// ulimit -s unlimited

// known height of 3 meters
double known_height = 3.0;

float calc_coefficient(float obs_z, float height_z, float obs_ref, float height_ref)
{
    float height_ratio,speed_ratio,alpha;
    height_ratio = height_z / height_ref;
    speed_ratio = obs_z / obs_ref;
    alpha =  log(speed_ratio)/log(height_ratio);
	return alpha;
}



int main(int argc, const char *argv[]) {
    // Get stdin...
    if (argc < 3) 
    {
		cerr << "usage: ./progName infile.tsv outfile.tsv nthreads\n" << endl;
		exit(-1);
	}
    ifstream infile(argv[1]);
    // open the file
	if (!infile) {
		cerr << "file not found" << endl;
		exit(-1);
	}
    // open output file
    //ofstream outfile;
    //outfile.open(argv[2]);
    //if( !outfile ) 
    //{ 
    //    cerr << "Error: output file could not be opened" << endl;
    //    exit(1);
    //}
    // variables for doing some work
    int nthreads = atoi(argv[3]);
    string line;
    vector<std::string> line_data;
    string timestamp;
    vector<double> heights; 
    heights.push_back(75.0);
    heights.push_back(90.0);
    heights.push_back(105.0);
    heights.push_back(125.0);
    heights.push_back(150.0);
    heights.push_back(175.0);
    double results;
    while (getline(infile, line, '\t'))
    {
        line_data.push_back(line);
        timestamp = line_data[0];
        cout << heights[0] << "\n";
        int i=0;
        #pragma omp parallel for num_threads(nthreads) private(i,results)
        for (i=0; i<6; ++i)
        {
            results = calc_coefficient( atof(line_data[i+1].c_str()), heights[i], atof(line_data[7].c_str()), known_height);
            //#pragma omp critical
            //{
            //    cout << results  << "\n";
            //    //outfile << timestamp << "\t" << results << "\t" << estimated_height << "\n";
            //    //results = 1;
            //}
        }
    }     
    //outfile.close();
    return 0;
}
