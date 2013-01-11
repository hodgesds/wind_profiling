# Merging all One_Second_Data to monthly files with common header
import os,sys

# Here's our headers
header_str = "DataDBID,DataTimeStamp,ModbusNodeID,SerialNumber,ModbusSpecVersion,ApplicationVersion,MessageCount,TotalRunTime,TotalLaserTime,JulianDay,SecondsSinceMidnight,ModbusMaxRegisters,ModbusNumberOfRangeGates,StatusRG1DataGood,StatusRG2DataGood,StatusRG3DataGood,StatusRG4DataGood,StatusRG5DataGood,StatusRG6DataGood,StatusLaserOn,StatusLowWiperFluid,StatusLaserFaultBLU,StatusLaserFaultRLU,StatusWiping,StatusOnExternalPower,StatusSNRThreshCalPeriod,WindSpeedHorRG1,WindSpeedHor3MinRG1,WindSpeedHor10MinRG1,WindDirHorRG1,WindDirHor3MinRG1,WindDirHor10MinRG1,WindSpeedVertRG1,WindAngleVertRG1,WindSpeedHorRG2,WindSpeedHor3MinRG2,WindSpeedHor10MinRG2,WindDirHorRG2,WindDirHor3MinRG2,WindDirHor10MinRG2,WindSpeedVertRG2,WindAngleVertRG2,WindSpeedHorRG3,WindSpeedHor3MinRG3,WindSpeedHor10MinRG3,WindDirHorRG3,WindDirHor3MinRG3,WindDirHor10MinRG3,WindSpeedVertRG3,WindAngleVertRG3,WindSpeedHorRG4,WindSpeedHor3MinRG4,WindSpeedHor10MinRG4,WindDirHorRG4,WindDirHor3MinRG4,WindDirHor10MinRG4,WindSpeedVertRG4,WindAngleVertRG4,WindSpeedHorRG5,WindSpeedHor3MinRG5,WindSpeedHor10MinRG5,WindDirHorRG5,WindDirHor3MinRG5,WindDirHor10MinRG5,WindSpeedVertRG5,WindAngleVertRG5,WindSpeedHorRG6,WindSpeedHor3MinRG6,WindSpeedHor10MinRG6,WindDirHorRG6,WindDirHor3MinRG6,WindDirHor10MinRG6,WindSpeedVertRG6,WindAngleVertRG6,Pitch,Roll,Heading,PitchRate,RollRate,YawRate,AccelerationX,AccelerationY,AccelerationZ,RangeGateWidth\n"

# Directories
data_dir = "/home/borgmaan/ws_gvsu/Data/One_Second_Data/"
folders = [data_dir + x + "/" for x in os.listdir(data_dir)]

# Agg all of the files in the sub-folders
for f in folders:
	# Match names
	out_name = data_dir + f.split("/")[-2][4:len(f.split("/")[-2])] + ".csv"
	print "Writing to", out_name
	with open(out_name, "w") as outfile:
		outfile.write(header_str)
		# Grab all of the sub folder files
		folder_files = [f + x for x in os.listdir(f)]
		
		# Aggregate lines of correct length
		for l in folder_files:
			with open(l) as infile:
				for line in infile:
					if not line.startswith("DataDBID"):
						spl = line.split(",")
						if len(spl) == 202:
							outfile.write(",".join(spl[0:85] + "\n")
