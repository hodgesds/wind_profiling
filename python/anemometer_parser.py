#!/usr/bin/env python
######################################################################
# Andrew Borgman
# 1/31/2012
# Parsing through anemometer data from LIDAR bouy

# Example line[12/07/09 13:51:52]$W5M5A,120709,135152,810201d7496196ee,7,,,,0.000,0.0,0.000,0.0,,0*20
import os,sys
from datetime import datetime

infile_name = "/home/borgmaan/ws_gvsu/results/cup_data/anemometer_data.csv"

with open(infile_name) as infile:
	for line in infile:
		spl = line.replace("[", "").replace("]$W5M5A", "").split(",")

