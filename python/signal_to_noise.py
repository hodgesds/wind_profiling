#!/usr/bin/env python
# Andrew Borgman
# 1/11/13
# Computing coefficient of variation for different aggregation levels.
# CV serves as baseline signal to noise ratio for screening purposes
##################################################################### 
import os,sys
import numpy
import glob

data = '/home/andrew/Desktop/windData/mergedData.csv'
dest = '/home/borgmaan/ws_gvsu/results/'

def stddev(numbers):
	""" Computes standard deviation of 
		a list of numbers ... slowly
	"""
	n = len(numbers)
	listSum = sum(numbers)
	squares = []
	for num in numbers:
		squares.append(num * num)
	sum_of_squares = sum(squares)
	return sqrt(sum_of_squares / n - (listSum / n) ** 2)

#Getting averages for different windows 5,10,15... second averages (from 5 seconds to 10 minutes:
u = [5]
for x in u:
	print(str(x))
	#To track time
	currentTime = 0
	lastTime = 0	
	currentDay = 0
	lastDay = 0
	
	dat = open(data)
	outfile = open(dest + str(x) + 'SecondAverage.csv','w')
	header = dat.readline().replace('\r\n','').split(',')
	
	#Grabbing index of columns we care about and writing them out
	goodCols = header[22:(len(header)-1)]
	numCols = len(goodCols)
	outfile.write('N,STDEV,' + ','.join(goodCols) + '\n')
	
	#For aggregating
	agg = []
	for z in range(numCols):
		agg.append([])
	#Running through the file and computing sliding-window averages for specified window length
	i = 0
	lag = False
	for line in dat:
		spl = line.split(',')
		spl = spl[22:(len(spl)-1)]
		currentDay = float(spl[0])
		#Accounting for seconds resetting at midnight
		if currentDay != lastDay:
			print currentDay , lastDay
			lastDay = currentDay
			if i != 0:
				lag = True
		
		#If we are 
		if lag:
			currentTime = currentTime + float(spl[1])
			lagTime = float(spl[1])
		else:
			currentTime = float(spl[1])
		
		if i == 0:
			lastTime = float(spl[1])
			for j in range(len(spl)):
				agg[j].append(float(spl[j]))
		
		else:
			if (currentTime - lastTime) < x:
				for j in range(len(spl)):
					agg[j].append(float(spl[j]))
			else:
				print('Time difference was: ' + str((currentTime - lastTime)) + '\n' + 'Current time is: ' + str(currentTime) + '\n' + 'Last time was: ' + str(lastTime))  
				
				#Resetting last obervation
				lastTime = currentTime
				if lag:
					lastTime = lagTime
				
				#Calculating metrics
				#N and STDEV values are for RG1 HWS 1s
				length = len(agg[4])
				try:
					sd = stddev(agg[4])
				except:
					sd = 0
				averages = []
				for l in agg:
					try:
						averages.append(str(sum(l) / len(l)))
					except:
						averages.append('NA')
				#Resetting aggregator list
				agg = []
				for z in range(numCols):
					agg.append([])
				#Making sure we have observations for all variables
				if(len(averages) == numCols):
					outfile.write(str(length) + ',' + str(sd) + ',' +','.join(averages) + '\n')
			
				#Resetting list
				for j in range(len(spl)):
					agg[j].append(float(spl[j]))
				
				#Resetting lag
				lag = False
				
		i += 1
	
	outfile.close()
	
