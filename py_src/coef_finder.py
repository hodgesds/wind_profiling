#!/usr/bin/env python

# Andrew Borgman
# Serial version of wind power profile law coefficient finder
# Use both anenometer values and data from 6 sensors to come up with 
# consensus coefficient estimate for each observation.
# Here's the sesor heights:
# Average Horizontal Wind Speed 75m
# Average Horizontal Wind Speed 90m
# Average Horizontal Wind Speed 105m
# Average Horizontal Wind Speed 125m
# Average Horizontal Wind Speed 150m
# Average Horizontal Wind Speed 175m
# '12/01/05 18:39:20\t7.2\t7.8\t8.2\t8\t7.6\t7.7\t5.219\t5.476\n'
# 22,740,021 obs.
# File processed in: 1126
# Parallel --> File processed in: 125

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

	return all_vals

	# Too much variability to do this... return and report all individual results...
	#all_vals = np.array([coef_75_1, coef_75_2, coef_90_1, coef_90_2, coef_105_1, coef_105_2, coef_125_1, coef_125_2, coef_150_1, coef_150_2, coef_175_1, coef_175_2])
	#mean_coeff = stats.nanmean(all_vals)
	#sd_coeff = stats.nanstd(all_vals)

def main(argv):
	"""
		Input files should be tab delimeted file with 1 second data for 
		all sensors in it
	"""
	infile_dir = "/home/borgmaan/merged_cup_lidar/"
	outfile_dir = "/home/borgmaan/coef_results/"

	if infile_dir != "" and infile_dir != "":

		# Timer
		start = time.time()

		# Grab all of the files
		merged_files = [infile_dir + x for x in os.listdir(infile_dir)]

		# Storage and tracking 
		results = []; ctr = 0

		# Rip through files 
		for f in merged_files:
			with open(f) as infile:
				for line in infile:
					spl = line.replace("\n", "").split("\t")
					all_results = process_line([float(x) for x in spl[1:]])
					tmp = [spl[0]]
					tmp.extend(all_results)
					results.append([str(x) for x in tmp])

					ctr += 1
					if ctr % 1000000 == 0:
						print "Processed %d records in: %d" % (ctr, (time.time() - start))

			# Write results to file
			outfile_name = outfile_dir + f.split("/")[-1]
			with open(outfile_name,"w") as outfile:
				outfile.write("Time\tcoef_75_1\tcoef_75_2\tcoef_90_1\tcoef_90_2\tcoef_105_1\tcoef_105_2\tcoef_125_1\tcoef_125_2\tcoef_150_1\tcoef_150_2\tcoef_175_1\tcoef_175_2\n")
				
				for result in results:
					outfile.write("\t".join(result) + "\n")

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