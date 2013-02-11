#!/usr/bin/env python
######################################################################
# Andrew Borgman
# 1/26/2012
# Script runs through all raw data from buoy and writes out 
# files with pertinant data to date-time ordered monthly files.
# Also does blunt QC checking to see which months have most
# data coverage in % of seconds covered.

## Todo:
#		> Create a more specific QC program that breaks data 
#		  coverage stats down to a daily level.
#		> Come up with something to test aggregation schemes on
#		  these monthy data sets. 
######################################################################

# Merging all One_Second_Data to monthly files with common headers
import os,sys
from datetime import datetime
import numpy
import glob
from csv import DictReader
from calendar import monthrange

# Log file for data coverage tracking
log_file_name = "/home/borgmaan/ws_gvsu/results/monthly_coverage.tsv"

# Here's our headers
header_str = "DataTimeStamp,ModbusNodeID,SerialNumber,ModbusSpecVersion,ApplicationVersion,MessageCount,TotalRunTime,TotalLaserTime,JulianDay,SecondsSinceMidnight,ModbusMaxRegisters,ModbusNumberOfRangeGates,StatusRG1DataGood,StatusRG2DataGood,StatusRG3DataGood,StatusRG4DataGood,StatusRG5DataGood,StatusRG6DataGood,StatusLaserOn,StatusLowWiperFluid,StatusLaserFaultBLU,StatusLaserFaultRLU,StatusWiping,StatusOnExternalPower,StatusSNRThreshCalPeriod,WindSpeedHorRG1,WindSpeedHor3MinRG1,WindSpeedHor10MinRG1,WindDirHorRG1,WindDirHor3MinRG1,WindDirHor10MinRG1,WindSpeedVertRG1,WindAngleVertRG1,WindSpeedHorRG2,WindSpeedHor3MinRG2,WindSpeedHor10MinRG2,WindDirHorRG2,WindDirHor3MinRG2,WindDirHor10MinRG2,WindSpeedVertRG2,WindAngleVertRG2,WindSpeedHorRG3,WindSpeedHor3MinRG3,WindSpeedHor10MinRG3,WindDirHorRG3,WindDirHor3MinRG3,WindDirHor10MinRG3,WindSpeedVertRG3,WindAngleVertRG3,WindSpeedHorRG4,WindSpeedHor3MinRG4,WindSpeedHor10MinRG4,WindDirHorRG4,WindDirHor3MinRG4,WindDirHor10MinRG4,WindSpeedVertRG4,WindAngleVertRG4,WindSpeedHorRG5,WindSpeedHor3MinRG5,WindSpeedHor10MinRG5,WindDirHorRG5,WindDirHor3MinRG5,WindDirHor10MinRG5,WindSpeedVertRG5,WindAngleVertRG5,WindSpeedHorRG6,WindSpeedHor3MinRG6,WindSpeedHor10MinRG6,WindDirHorRG6,WindDirHor3MinRG6,WindDirHor10MinRG6,WindSpeedVertRG6,WindAngleVertRG6,Pitch,Roll,Heading,PitchRate,RollRate,YawRate,AccelerationX,AccelerationY,AccelerationZ,RangeGateWidth\n"

# Directories
data_dir = "/home/borgmaan/ws_gvsu/Data/One_Second_Data/"
folders = [data_dir + x + "/" for x in os.listdir(data_dir)]

# All month/year combos found in files
months = ['6_2012', '12_2011', '11_2012', '11_2011', '3_2012', '5_2012', '8_2012', '1_2012', '4_2012', '7_2012', '2_2012', '10_2011', '10_2012', '9_2012']

# Agg all of the files in the sub-folders into month specific folders
with open(log_file_name, "w") as log_file:
	
	# Loop through each month
	for month in months:
		print "Analyzing data for ", month

		# Month specific file
		with open("/home/borgmaan/ws_gvsu/results/monthly_files/" + month + ".csv", "w") as outfile:
			
			# Toss that header in there
			outfile.write(header_str)

			# Get number of seconds 
			month_days = monthrange(int(month.split("_")[1]), int(month.split("_")[0]))[1]
			month_seconds = month_days * 24 * 60 * 60

			# Hit each data folder and store any data for month/year in list of dicts to sort :: might blow ram up
			month_data = []
			for f in folders:
				# Grab all of the sub folder files
				folder_files = [f + x for x in os.listdir(f)]
				
				# Aggregate lines of correct length
				for l in folder_files:
					with open(l) as infile:
						for line in infile:
							if not line.startswith("DataDBID"):
								spl = line.split(",")
								if len(spl) == 202:
									#outfile.write(",".join(spl[1:84]) + "\n")
									new_date = datetime.strptime(spl[1], "%Y-%m-%d %H:%M:%S")
									new_date_str = "_".join([str(x) for x in [new_date.month, new_date.year]])
									if new_date_str == month:
										data = ",".join(spl[1:84]) + "\n"
										data_dict = {'date_stamp':new_date, 'line_to_write': data}
										month_data.append(data_dict)

			# Sort list of dicts in date-time and write to file
			month_data.sort(key=lambda item:item['date_stamp'])
			for sec in month_data:
				outfile.write(sec['line_to_write'])

			# Write out rough QC measure
			pct_covered = float(len(month_data)) / float(month_seconds)
			log_file.write("\t".join([str(x) for x in [month,pct_covered]]) + "\n")
