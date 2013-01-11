# Checking to see if all data from One_Second_Data is in same format
import os,sys

data_dir = "/home/borgmaan/ws_gvsu/Data/One_Second_Data/"

folders = [data_dir + x + "/" for x in os.listdir(data_dir)]

for f in folders:
	folder_files = [f + x for x in os.listdir(f)]
	for l in folder_files:
		with open(l) as infile:
			for line in infile:
				spl = line.split(",")
				if len(spl) != 202:
					print len(spl)
