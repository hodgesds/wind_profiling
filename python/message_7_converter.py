#!/usr/bin/env python
import os,sys
"""
*Converts the data from the message 7 files to tab separated
*
* [07] 1 sec Data
* Fields
* [01] DataTimeStamp
* [02] MessageID
* [03] Yaw (deg)
* [04] Pitch (deg)
* [05] Roll (deg)
* [06] Current wind speed
* [07] Current interval gust speed
* [08] Current wind speed
* [09] Current interval gust speed
* [10] Current wind direction
* [11] Instantaneous Services Per Second
"""
if len(sys.argv) <3:
    print "Usage: python message_7_converter.py message7_data.csv outfile.tsv"
    raise RuntimeError('Ya done broke things')

with open(sys.argv[1],'r') as cup:
    with open(sys.argv[2],'w') as ofile:
        for row in cup:
            # grab out the time
            time = row.replace('\n','').split("$")[0].replace("]","").replace("[","")
            # split line on commas
            line = row.split(",")
            # time fix
            line.insert(0,time)
            ofile.write('\t'.join(line)+'\n')
