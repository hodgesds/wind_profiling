# Merging all One_Second_Data to monthly files with common header
import os,sys

# Here's our headers
header_str = "DataTimeStamp,Sensor Serial Number,Sensor Application Version,Sensor Modbus Version,Message Count,Total Run Time,Total Laser Time,Reserved1,Modbus Max Registers,Modbus Range Gates,Modbus Node ID,Modbus Spare1,Laser State,Wiper Fluid State,Laser Fault State - BLU,Laser Fault State - RLU,Wiper State,Power Supply State,SNR State,Spare State 1,Spare State 2,Spare State 3,Timestamp (day),Timestamp (second),RG Width,RG1 Status,RG1 HWS 1s,RG1 HWS 3m,RG1 HWS 10m,RG1 HWD 1s,RG1 HWD 3m,RG1 HWD 10m,RG1 VWS 1s,RG1 VWA 1s,RG2 Status,RG2 HWS 1s,RG2 HWS 3m,RG2 HWS 10m,RG2 HWD 1s,RG2 HWD 3m,RG2 HWD 10m,RG2 VWS 1s,RG2 VWA 1s,RG3 Status,RG3 HWS 1s,RG3 HWS 3m,RG3 HWS 10m,RG3 HWD 1s,RG3 HWD 3m,RG3 HWD 10m,RG3 VWS 1s,RG3 VWA 1s,RG4 Status,RG4 HWS 1s,RG4 HWS 3m,RG4 HWS 10m,RG4 HWD 1s,RG4 HWD 3m,RG4 HWD 10m,RG4 VWS 1s,RG4 VWA 1s,RG5 Status,RG5 HWS 1s,RG5 HWS 3m,RG5 HWS 10m,RG5 HWD 1s,RG5 HWD 3m,RG5 HWD 10m,RG5 VWS 1s,RG5 VWA 1s,RG6 Status,RG6 HWS 1s,RG6 HWS 3m,RG6 HWS 10m,RG6 HWD 1s,RG6 HWD 3m,RG6 HWD 10m,RG6 VWS 1s,RG6 VWA 1s,Pitch (deg),Roll (deg),Heading (deg),Pitch Rate (deg/s),Roll Rate (deg/s),Yaw Rate (deg/s),Acceleration X (g),Acceleration Y (g),Acceleration Z (g),Range Gate Width\n"

# Directories
data_dir = "/home/borgmaan/ws_gvsu/Data/One_Second_Data/"
folders = [data_dir + x + "/" for x in os.listdir(data_dir)]

# Agg all of the files in the sub-folders
for f in folders:
	# Match names
	out_name = data_dir + f.split("/")[-2][4:len(f.split("/")[-2])] + ".csv"
	print "Writing to", out_name
	with open(out_name) as outfile:
		# Write out matching header
		outfile.write(header_str)

		# Grab all of the sub folder files
		folder_files = [f + x for x in os.listdir(f)]
		
		# Aggregate lines of correct length
		for l in folder_files:
			with open(l) as infile:
				for line in infile:
					spl = line.split(",")
					if len(spl) == 202:
						outfile.write(line)
