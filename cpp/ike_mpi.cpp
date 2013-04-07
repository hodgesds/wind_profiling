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
#include <cstdlib>
#include <stdlib.h>
#include <omp.h>
#include <sstream>
#include <fstream>
#include <string>
#include <stdlib.h>
#include <vector>
#include <cmath>
#include <cstring>
#include <string.h>
using namespace std;
#define OMP_STACKSIZE 15G
// default stack size for openmp sucks
// type this in bash so you stop getting overflows
// ulimit -s unlimited

double calc_coefficient(double obs_z, double height_z, double obs_ref, double height_ref)
{
    double height_ratio = 0;
    double speed_ratio = 0;
    double alpha = 0;
    height_ratio = height_z / height_ref;
    speed_ratio = obs_z / obs_ref;
    alpha =  log(speed_ratio)/log(height_ratio);
    return alpha;
}

int main(int argc, const char *argv[]) {
    // Get stdin...+9
    if (argc < 3) 
    {
		cerr << "usage: ./progName infile.tsv outfile.tsv nthreads\n" << endl;
		exit(-1);
	}
    ifstream infile(argv[1]);
    cout << argv[1] << endl;
    // open the file
	if (!infile) {
		cerr << "file not found" << endl;
		exit(-1);
	}
    // open output file
    ofstream outfile;
    outfile.open(argv[2]);
    if( !outfile ) 
    { 
        cerr << "Error: output file could not be opened" << endl;
        exit(1);
    }
    // variables for doing some work
    int nthreads = atoi(argv[3]);
    double known_height = 3.0;
    string line;
    string timestamp;
    vector<double> heights; 
    heights.push_back(75.0);
    heights.push_back(90.0);
    heights.push_back(105.0);
    heights.push_back(125.0);
    heights.push_back(150.0);
    heights.push_back(175.0);
    string partial;
    vector<string> bigass_data;
    vector<string> results;
    while(getline(infile, line)) 
    { 
        bigass_data.push_back(line);
        results.push_back(""); // make a empty results vector... wait for the magic.
    }
    int a=0;
    size_t pos = 0;
    int splits = 0;
    int i = 0;
    double k1_speed,k2_speed,o1_speed,r_one,r_two;
    char jimmy_buffer [50];
    string buffer_slip;
    string outkast; // i love the way you move
    string token;
    vector<string> tokens;
    string delimiter = "\t";
    #pragma omp parallel for num_threads(nthreads)  private(a,i,outkast,jimmy_buffer,buffer_slip,r_one,r_two,pos,splits,o1_speed,k1_speed,k2_speed,tokens,token)
    for (a=0; a<bigass_data.size(); ++a)
    {
        
        splits = 0;
        pos = 0;
        while ((pos = bigass_data[a].find(delimiter)) != string::npos) 
        {
            token = bigass_data[a].substr(0, pos);
            splits +=1;
            tokens.push_back(token);
            //cout << token << ' ' << pos << endl;
            bigass_data[a].erase(0, pos + delimiter.length());
        }
        if (splits == 8)
        {
            //cout << tokens[tokens.size()-1] << "-" << tokens[8] << '\n';
            i = 0;
            for (i=1; i<6; ++i)
            {
                o1_speed = atof(tokens[i].c_str() );
                k1_speed = atof(tokens[6].c_str() ); 
                k2_speed = atof(tokens[7].c_str() ); 
                r_one = calc_coefficient( o1_speed, heights[i-1], k1_speed, known_height);
                r_two = calc_coefficient( o1_speed, heights[i-1], k2_speed, known_height);
            }
                sprintf(jimmy_buffer, "\t%f\t%f\n",r_one,r_two);
                buffer_slip = jimmy_buffer;
                outkast = tokens[0] + buffer_slip;
                results[a] = outkast;
                //outfile << tokens[0] << '\t' << r_one << '\t' << r_two << '\n';
        }

        tokens.clear();
    }     
    for (a=0; a<results.size(); ++a)
    {
        outfile << results[a] ;
    }
    
    outfile.close();
    return 0;
}
