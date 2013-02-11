from numpy import *
import os,sys
from power_profile import *

with open('mergedData.csv','r') as work:
    for row in work:
        # Assume RGX HWS 1s as known @ 1 meter, comparing to laser estimates
        # Observed RG1
        rg1_known_speed = row.split(",")[26]
        rg1_known_height = 1
        rg1_speed_3m = row.split(",")[27]
        rg1_height_3m = 3
        rg1_speed_10m = row.split(",")[28]
        rg1_height_10m = 10
        # Observed RG2
        rg2_known_speed = row.split(",")[35]
        rg2_known_height = 1
        rg2_speed_3m = row.split(",")[36]
        rg2_height_3m = 3
        rg2_speed_10m = row.split(",")[37]
        rg2_height_10m = 10
        # Observed RG3
        rg3_known_speed = row.split(",")[44]
        rg3_known_height = 1
        rg3_speed_3m = row.split(",")[45]
        rg3_height_3m = 3
        rg3_speed_10m = row.split(",")[46]
        rg3_height_10m = 10
        # Observed RG4
        rg4_known_speed = row.split(",")[53]
        rg4_known_height = 1
        rg4_speed_3m = row.split(",")[54]
        rg4_height_3m = 3
        rg4_speed_10m = row.split(",")[55]
        rg4_height_10m = 10
        # Observed RG5
        rg5_known_speed = row.split(",")[62]
        rg5_known_height = 1
        rg5_speed_3m = row.split(",")[63]
        rg5_height_3m = 3
        rg5_speed_10m = row.split(",")[64]
        rg5_height_10m = 10
        # Observed RG6
        rg6_known_speed = row.split(",")[62]
        rg6_known_height = 1
        rg6_speed_3m = row.split(",")[63]
        rg6_height_3m = 3
        rg6_speed_10m = row.split(",")[64]
        rg6_height_10m = 10
        # Speed & Power estimates
        # RG1- 3m
        rg1_power_profile_3m = PowerProfile(rg1_known_height, rg1_height_3m , rg1_known_speed, rg1_speed_3m , 1.0/7)
        rg1_speed_estimate_3m = rg1_power_profile_3m.EstimateSpeed()
        rg1_power_estimate_3m = rg1_power_profile_3m.PowerDensity()
        # RG1- 10m
        rg1_power_profile_10m = PowerProfile(rg1_known_height, rg1_height_10m , rg1_known_speed, rg1_speed_10m , 1.0/7)
        rg1_speed_estimate_10m = rg1_power_profile_10m.EstimateSpeed()
        rg1_power_estimate_10m = rg1_power_profile_10m.PowerDensity()
        # RG2- 3m
        rg2_power_profile_3m = PowerProfile(rg2_known_height, rg2_height_3m , rg2_known_speed, rg2_speed_3m , 1.0/7)
        rg2_speed_estimate_3m = rg2_power_profile_3m.EstimateSpeed()
        rg2_power_estimate_3m = rg2_power_profile_3m.PowerDensity()
        # RG2- 10m
        rg2_power_profile_10m = PowerProfile(rg2_known_height, rg2_height_10m , rg2_known_speed, rg2_speed_10m , 1.0/7)
        rg2_speed_estimate_10m = rg2_power_profile_10m.EstimateSpeed()
        rg2_power_estimate_10m = rg2_power_profile_10m.PowerDensity()
        # RG3- 3m
        rg3_power_profile_3m = PowerProfile(rg3_known_height, rg3_height_3m , rg3_known_speed, rg3_speed_3m , 1.0/7)
        rg3_speed_estimate_3m = rg3_power_profile_3m.EstimateSpeed()
        rg3_power_estimate_3m = rg3_power_profile_3m.PowerDensity()
        # RG3- 10m
        rg3_power_profile_10m = PowerProfile(rg3_known_height, rg3_height_10m , rg3_known_speed, rg3_speed_10m , 1.0/7)
        rg3_speed_estimate_10m = rg3_power_profile_10m.EstimateSpeed()
        rg3_power_estimate_10m = rg3_power_profile_10m.PowerDensity()
        # RG4- 3m
        rg4_power_profile_3m = PowerProfile(rg4_known_height, rg4_height_3m , rg4_known_speed, rg4_speed_3m , 1.0/7)
        rg4_speed_estimate_3m = rg4_power_profile_3m.EstimateSpeed()
        rg4_power_estimate_3m = rg4_power_profile_3m.PowerDensity()
        # RG4- 10m
        rg4_power_profile_10m = PowerProfile(rg4_known_height, rg4_height_10m , rg4_known_speed, rg4_speed_10m , 1.0/7)
        rg4_speed_estimate_10m = rg4_power_profile_10m.EstimateSpeed()
        rg4_power_estimate_10m = rg4_power_profile_10m.PowerDensity()
        # RG5- 3m
        rg5_power_profile_3m = PowerProfile(rg5_known_height, rg5_height_3m , rg5_known_speed, rg5_speed_3m , 1.0/7)
        rg5_speed_estimate_3m = rg5_power_profile_3m.EstimateSpeed()
        rg5_power_estimate_3m = rg5_power_profile_3m.PowerDensity()
        # RG5- 10m
        rg5_power_profile_10m = PowerProfile(rg5_known_height, rg5_height_10m , rg5_known_speed, rg5_speed_10m , 1.0/7)
        rg5_speed_estimate_10m = rg5_power_profile_10m.EstimateSpeed()
        rg5_power_estimate_10m = rg5_power_profile_10m.PowerDensity()
        # RG6- 3m
        rg6_power_profile_3m = PowerProfile(rg6_known_height, rg6_height_3m , rg6_known_speed, rg6_speed_3m , 1.0/7)
        rg6_speed_estimate_3m = rg6_power_profile_3m.EstimateSpeed()
        rg6_power_estimate_3m = rg6_power_profile_3m.PowerDensity()
        # RG6- 10m
        rg6_power_profile_10m = PowerProfile(rg6_known_height, rg6_height_10m , rg6_known_speed, rg6_speed_10m , 1.0/7)
        rg6_speed_estimate_10m = rg6_power_profile_10m.EstimateSpeed()
        rg6_power_estimate_10m = rg6_power_profile_10m.PowerDensity()
        
       
