#!/usr/bin/env python
import os,sys
#cut -f 26,34,42,50,58,66,84 -d , 9_2012.csv
if len(sys.argv) <4:
    print "Usage: python cup_lidar_merger.py outfile cup_month.tsv lidar_month.tsv"
    raise RuntimeError('Ya done broke things')

        
cup_dict = {}
with open(sys.argv[2],'r') as cups:
    for row in cups:
        try:
            # wind data actually on columns 8,10 so taking the average...
            cup_dict[row.split("\t")[0]] = (float(row.split("\t")[8]) + float(row.split("\t")[10]))/2
            #cdict[row.split("\t")[0]] = (float(row.split("\t")[5])) #+ float(row.split("\t")[10]))/2

        except:
            #print float(row.split("\t")[8]) + float(row.split("\t")[10])
            pass
print 'found',len(cup_dict),'cups'
print cup_dict[cup_dict.keys()[0]],cup_dict.keys()[0]

failures = 0
with open(sys.argv[1],'w') as ofile:
    with open(sys.argv[3]) as lidar:
        for row in lidar:
            if 'Serial' not in row:
                # fixe for difference in data storage
                times = row.split(',')[0].replace('-','/').replace("2012",'12')
                try:
                    odata = times + '\t' + row.split(',')[25] + '\t' + row.split(',')[33] + '\t' + row.split(',')[41] + + '\t' + row.split(',')[49] + '\t' + row.split(',')[57] + '\t' + row.split(',')[65] + '\t' + str(cup_dict[times]) + '\n'
                    ofile.write(odata)
                except:
                    failures += 1
                    pass
print failures,'observations failed to merge'
