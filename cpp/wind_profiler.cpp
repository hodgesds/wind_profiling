//g++ -fopenmp wind_profiler.cpp -lrt -O3 -o wind_profiler
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

// Range Gate Heights: 75, 90, 105, 125, 150, 175 meters

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

int main(int argc, char* argv[])
{
    if (argc < 3) 
    {
		cerr << "usage: ./progName infile.csv outfile.csv nthreads\n" << endl;
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
    outfile.open(argv[2]);
    if( !outfile ) 
    { 
        cerr << "Error: output file could not be opened" << endl;
        exit(1);
    }    
    // variable for reading in strings and header checking
    string row = "";
    int nthreads = atoi(argv[3]);
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
            vector<double> known_speeds;
            header_row = row.find("HWS", 0);
            // filter all all header rows...
            if ( header_row == string::npos )
            {
                // if no header we want to estimate
                // read in row as a string
                istringstream row_split( row );
                // start at the first comma split
                split_count = 0;
                while (!row_split.eof())
                {
                    string x;
                    double known_speed;
                    // split on commas               
                    getline( row_split, x, ',' );
                    // grab timestamp from first row....  
                    if (split_count==0)
                    {
                        timestamp = x;
                    }
                    // RG1 Sensor Data
                    if (split_count==26)
                    {
                        istringstream iss(x);
                        // string to double in vector
                        iss >> known_speed;
                        known_speeds.insert(known_speeds.begin(),known_speed);
                        // cout << known_speed << endl;
                        //int i=2;
                        //double results;
                        //#pragma omp parallel for num_threads(nthreads) private(i,results)
                        //for ( i=2; i<=max_height; i++)
                        //{
                        //    double estimated_height = (double) i;
                        //    results = estimate_speed(known_speed, known_height, estimated_height);
                        //    // blocking so threads can write to output file
                        //    #pragma omp critical
                        //    {
                        //        //cout << results << "\t" << estimated_height << "\n";
                        //        outfile << timestamp << "\t" << results << "\t" << estimated_height << "\n";
                        //        //double a;
                        //        //a = results;
                        //    }
                        //}
                    }
                    // RG2 Sensor Data
                    if (split_count==35)
                    {
                        istringstream iss(x);
                        // string to double
                        iss >> known_speed;
                        known_speeds.insert(known_speeds.begin()+1,known_speed);
                    }
                    // RG3 Sensor Data
                    if (split_count==44)
                    {
                        istringstream iss(x);
                        // string to double
                        iss >> known_speed;
                        known_speeds.insert(known_speeds.begin()+2,known_speed);
                    }
                    // RG4 Sensor Data
                    if (split_count==53)
                    {
                        istringstream iss(x);
                        // string to double
                        iss >> known_speed;
                        known_speeds.insert(known_speeds.begin()+3,known_speed);
                    }
                    // RG5 Sensor Data
                    if (split_count==62)
                    {
                        istringstream iss(x);
                        // string to double
                        iss >> known_speed;
                        known_speeds.insert(known_speeds.begin()+4,known_speed);
                    }
                    // RG6 Sensor Data
                    if (split_count==71)
                    {
                        istringstream iss(x);
                        // string to double
                        iss >> known_speed;
                        known_speeds.insert(known_speeds.begin()+5,known_speed);
                        int i = 0;
                        double results;
                        #pragma omp parallel for num_threads(nthreads) private(i,results)
                        for ( i=0; i<=known_speeds.size(); i++)
                        {
                            
                            double estimated_height = (double) i;
                            results = estimate_speed(known_speeds[i], known_height, estimated_height);
                            #pragma omp critical
                            {
                                cout << results << "\t" << estimated_height << "\n";
                                //outfile << timestamp << "\t" << results << "\t" << estimated_height << "\n";
                                //results = 1;
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

