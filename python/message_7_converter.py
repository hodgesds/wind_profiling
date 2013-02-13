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
    print "Usage: python message_7_converter.py message7_data.txt outdir"
    raise RuntimeError('Ya done broke things')

# big dict, big data
big_dict = {}
with open(sys.argv[1],'r') as cup:
    for row in cup:
        # grab out the time
        time = row.replace('\n','').split("$")[0].replace("]","").replace("[","")
        # split line on commas
        line = row.split(",")
        # make the big dict
        big_dict[time] = line

sorted(big_dict, key=big_dict.get)
for key,value in big_dict.items():
    print key,value
    raw_input()
#ofile.write('\t'.join(line)+'\n')
