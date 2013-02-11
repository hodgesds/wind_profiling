from numpy import *
import os,sys

# Do it with Numpy's power function on arrays
def estimated_speed(known_height,known_speed,estimated_height):
    alpha = 1.0/7
    return known_speed*power(estimated_height/known_height,alpha)
    
# write results
#results = open('sensor_and_estimate diff.txt','w')

with open('mergedData.csv','r') as work:
    for row in work:
        if 'HWS' not in row:
			known_height = []
			known_speed = []
			estimated_height = []
			#for i in range(2,10):
			#    known_height.append(float(3))
			#    known_speed.append(float(row.split(",")[26]))
			#    estimated_height.append(float(i))
			
			# convert to numpy arrays
			#known_height = array(known_height)
			#known_speed = array(known_speed)
			#estimated_height = array(estimated_height)
			
			# perform calculation
			#speed_estimate = estimated_speed(known_height,known_speed,estimated_height)
			
			# RG1
			rg1_known_speed = float(row.split(",")[26])
			rg1_speed_3m = float(row.split(",")[27])
			rg1_speed_10m = float(row.split(",")[28])
			rg1_diff_3m = rg1_speed_3m - estimated_speed(3.0,rg1_known_speed,3.0)
			rg1_diff_10m = rg1_speed_10m - estimated_speed(3.0,rg1_known_speed,10.0)
			
			
			# RG2 Sensors
			rg2_known_speed = float(row.split(",")[35])
			rg2_speed_3m = float(row.split(",")[36])
			rg2_speed_10m = float(row.split(",")[37])
			rg2_diff_3m = rg2_speed_3m - estimated_speed(3.0,rg2_known_speed,3.0)
			rg2_diff_10m = rg2_speed_10m - estimated_speed(3.0,rg2_known_speed,10.0)
			
			# RG3
			rg3_known_speed = float(row.split(",")[44])
			rg3_speed_3m = float(row.split(",")[45])
			rg3_speed_10m = float(row.split(",")[46])
			rg3_diff_3m = rg3_speed_3m - estimated_speed(3.0,rg3_known_speed,3.0)
			rg3_diff_10m = rg3_speed_10m - estimated_speed(3.0,rg3_known_speed,10.0)
			
			# RG4
			rg4_known_speed = float(row.split(",")[53])
			rg4_speed_3m = float(row.split(",")[54])
			rg4_speed_10m = float(row.split(",")[55])
			rg4_diff_3m = rg4_speed_3m - estimated_speed(3.0,rg4_known_speed,3.0)
			rg4_diff_10m = rg4_speed_10m - estimated_speed(3.0,rg4_known_speed,10.0)
			
			# RG5
			rg5_known_speed = float(row.split(",")[62])
			rg5_speed_3m = float(row.split(",")[63])
			rg5_speed_10m = float(row.split(",")[64])
			rg5_diff_3m = rg5_speed_3m - estimated_speed(3.0,rg5_known_speed,3.0)
			rg5_diff_10m = rg5_speed_10m - estimated_speed(3.0,rg5_known_speed,10.0)
			
			# RG6
			rg6_known_speed = float(row.split(",")[62])
			rg6_speed_3m = float(row.split(",")[63])
			rg6_speed_10m = float(row.split(",")[64])
			rg6_diff_3m = rg6_speed_3m - estimated_speed(3.0,rg6_known_speed,3.0)
			rg6_diff_10m = rg6_speed_10m - estimated_speed(3.0,rg6_known_speed,10.0)
			
			
			odata = str(rg1_diff_3m) + "\t" + str(rg1_diff_10m) + str(rg2_diff_3m) + "\t" + str(rg2_diff_10m) + str(rg3_diff_3m) + "\t" + str(rg3_diff_10m) + str(rg4_diff_3m) + "\t" + str(rg4_diff_10m) + str(rg5_diff_3m) + "\t" + str(rg5_diff_10m) + str(rg6_diff_3m) + "\t" + str(rg6_diff_10m) + "\n"
			print odata
            #results.write(odata)
			# write output
			#for i in range(0,speed_estimate.size):
			#    results.write(str( str(estimated_height[i]) + "\t" + str(speed_estimate[i]) + "\n"))
				
#results.close()
