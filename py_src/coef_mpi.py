#!/usr/bin/env python

# Andrew Borgman
# MPI Parallel version of wind power profile law coefficient finder
# Run command mpiexec -np 96 --hostfile hosts ./coef_mpi.py

import os,sys
from datetime import datetime
import getopt
import math
import numpy as np
from scipy import stats
from operator import itemgetter
import time
from csv import DictReader
import math
from mpi4py import MPI

def calc_coefficient(obs_z, height_z, obs_ref, height_ref):
	"""
		Takes two observations at two heights and returns
		an empirical wind power coefficient
	"""
	try:
		height_ratio = height_z / height_ref
		speed_ratio = obs_z / obs_ref

		alpha = math.log(speed_ratio, height_ratio)

	except:
		alpha = np.nan

	return alpha

def process_line(vals = []):
	"""
		Takes a line of data, calculates the empirical 
		wind power coefficient, alpha, using the two
		anenometer measures and all of the LIDAR sensors 
	"""

	coef_75_1 = calc_coefficient(vals[0], 75.0, vals[6], 3.5)
	coef_75_2 = calc_coefficient(vals[0], 75.0, vals[7], 3.5)

	coef_90_1 = calc_coefficient(vals[1], 90.0, vals[6], 3.5)
	coef_90_2 = calc_coefficient(vals[1], 90.0, vals[7], 3.5)

	coef_105_1 = calc_coefficient(vals[2], 105.0, vals[6], 3.5)
	coef_105_2 = calc_coefficient(vals[2], 105.0, vals[7], 3.5)

	coef_125_1 = calc_coefficient(vals[3], 125.0, vals[6], 3.5)
	coef_125_2 = calc_coefficient(vals[3], 125.0, vals[7], 3.5)

	coef_150_1 = calc_coefficient(vals[4], 150.0, vals[6], 3.5)
	coef_150_2 = calc_coefficient(vals[4], 150.0, vals[7], 3.5)

	coef_175_1 = calc_coefficient(vals[5], 175.0, vals[6], 3.5)
	coef_175_2 = calc_coefficient(vals[5], 175.0, vals[7], 3.5)


	all_vals = [coef_75_1, coef_75_2, coef_90_1, coef_90_2, coef_105_1, coef_105_2, coef_125_1, coef_125_2, coef_150_1, coef_150_2, coef_175_1, coef_175_2]

	# Too much variability to do this... return and report all individual results...
	#all_vals = np.array([coef_75_1, coef_75_2, coef_90_1, coef_90_2, coef_105_1, coef_105_2, coef_125_1, coef_125_2, coef_150_1, coef_150_2, coef_175_1, coef_175_2])
	#mean_coeff = stats.nanmean(all_vals)
	#sd_coeff = stats.nanstd(all_vals)

	return all_vals

def main(argv):
	"""
		Input files should be tab delimeted file with 1 second data for 
		all sensors in it
	"""
	infile_dir = "/home/borgmaan/merged_cup_lidar/"
	outfile_dir = "/home/borgmaan/coef_results_mpi/"

	if infile_dir != "" and infile_dir != "":

		# Timer
		start = time.time()

		# Getting python MPI tools initiated
		comm = MPI.COMM_WORLD
		rank = comm.Get_rank()
		size = comm.Get_size()
		name = MPI.Get_processor_name()
		MASTER = 0

		# Grab all of the files
		merged_files = [infile_dir + x for x in os.listdir(infile_dir)]

		# Storage and tracking 
		results = []

		# Rip through files 
		for f in merged_files:

			# Individual results for each processor
			indiv_results = []

			# Number of records in the file
			num_recs = int(os.popen("wc -l %s" % f).read().split()[0])

			# Grab lines to be analyzed by this proc and analyze
			my_lines = set(range(rank, num_recs, size))

			# Run through file processing lines mapped to that processor			
			with open(f) as infile:
				for i,line in enumerate(infile):

					if i in my_lines:
						spl = line.replace("\n", "").split("\t")
						all_results = process_line([float(x) for x in spl[1:]])
						tmp = [spl[0]]
						tmp.extend(all_results)
						indiv_results.append([str(x) for x in tmp])

			# Write results to node specific file
			outfile_name = outfile_dir + f.split("/")[-1].replace(".tsv", "") + "_" + str(rank) + ".tsv"

			with open(outfile_name, "w") as outfile:
				outfile.write("Time\tcoef_75_1\tcoef_75_2\tcoef_90_1\tcoef_90_2\tcoef_105_1\tcoef_105_2\tcoef_125_1\tcoef_125_2\tcoef_150_1\tcoef_150_2\tcoef_175_1\tcoef_175_2\n")
				
				for result in indiv_results:
					try:
						outfile.write("\t".join(result) + "\n")
					except:
						pass

			# Reset storage
			results = []

		print "File processed in: %d" % (time.time() - start)

		return True


if __name__ == "__main__":
	if main(sys.argv[1:]):
		print "File processed successfully..."
		pass
	else:
		print "You broke some shit, dude..."
