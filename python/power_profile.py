import os,sys,numpy as np

"""
As per:
http://en.wikipedia.org/wiki/Wind_profile_power_law

Wind Power Profile
u/ur = (z/zr)^a
where u is the wind speed (in metres per second) at height z (in metres)
and ur is the known wind speed at a reference height zr. 
The exponent (a) is an empirically derived coefficient that varies dependent upon the stability of the atmosphere.
 For neutral stability conditions, a is approximately 1/7, or 0.143.
 In order to estimate the wind speed at a certain height x, the relationship would be rearranged to:
ux = ur(zx/zr)^a
 """

"""
Log Wind Profile:

The equation to estimate the mean wind speed () at height  (meters) above the ground is: 
Uz =  U*/K { ln( (z-d)/d0) + w(z,z0,L) }
where U* is the friction (or shear) velocity (m s-1), K is the Von Karman constant (~0.41), d is the zero plane displacement, z0 is the surface roughness (in meters), w and  is a stability term where L is the Monin-Obukhov stability parameter. Under neutral stability conditions,  and  drops out.
"""
class PowerProfile:
    def __init__(self, known_height, observed_height, known_speed, observed_speed, alpha):
		self.known_height = known_height
		self.observed_height = observed_height
		self.known_speed = known_speed
		self.observed_speed = observed_speed
		self.alpha = alpha
    
    def EstimateSpeed(self):
        return self.known_speed*np.power((self.observed_height/self.known_height),self.alpha)
    
    def PowerDensity(self):
        # ASSUMING METERS FOR HEIGHT!!!
        if self.known_height <= 10:
            if self.known_speed <= 4.4:
                known_power_density = 1
            if self.known_speed > 4.4 and self.known_speed <= 5.1 :
                known_power_density = 2
            if self.known_speed > 5.1 and self.known_speed <= 5.6 :
                known_power_density = 3
            if self.known_speed > 5.6 and self.known_speed <= 6.0 :
                known_power_density = 4
            if self.known_speed > 6.0 and self.known_speed <= 6.4 :
                known_power_density = 5
            if self.known_speed > 6.4 and self.known_speed <= 7.0 :
                known_power_density = 6
            # No upper bound....
            if self.known_speed > 7.0:
                known_power_density = 7
        if self.known_height > 10 and self.known_height <=30:
            if self.known_speed <= 5.1:
                known_power_density = 1
            if self.known_speed > 5.1 and self.known_speed <= 5.9 :
                known_power_density = 2
            if self.known_speed > 5.9 and self.known_speed <= 6.5 :
                known_power_density = 3
            if self.known_speed > 6.5 and self.known_speed <= 7.0 :
                known_power_density = 4
            if self.known_speed > 7.0 and self.known_speed <= 7.4 :
                known_power_density = 5
            if self.known_speed > 7.4 and self.known_speed <= 8.2 :
                known_power_density = 6
            # No upper bound....
            if self.known_speed > 8.2:
                known_power_density = 7
        if self.known_height >50:
            if self.known_speed <= 5.6:
                known_power_density = 1
            if self.known_speed > 5.6 and self.known_speed <= 6.4 :
                known_power_density = 2
            if self.known_speed > 6.4 and self.known_speed <= 7.0 :
                known_power_density = 3
            if self.known_speed > 7.0 and self.known_speed <= 7.5 :
                known_power_density = 4
            if self.known_speed > 7.5 and self.known_speed <= 8.0 :
                known_power_density = 5
            if self.known_speed > 8.0 and self.known_speed <= 8.8 :
                known_power_density = 6
            # No upper bound....
            if self.known_speed > 8.8:
                known_power_density = 7
        
        # Observed Power Density
        if self.observed_height <= 10:
            if self.observed_speed <= 4.4:
                observed_power_density = 1
            if self.observed_speed > 4.4 and self.observed_speed <= 5.1 :
                observed_power_density = 2
            if self.observed_speed > 5.1 and self.observed_speed <= 5.6 :
                observed_power_density = 3
            if self.observed_speed > 5.6 and self.observed_speed <= 6.0 :
                observed_power_density = 4
            if self.observed_speed > 6.0 and self.observed_speed <= 6.4 :
                observed_power_density = 5
            if self.observed_speed > 6.4 and self.observed_speed <= 7.0 :
                observed_power_density = 6
            # No upper bound....
            if self.observed_speed > 7.0:
                observed_power_density = 7
        if self.observed_height > 10 and self.observed_height <=30:
            if self.observed_speed <= 5.1:
                observed_power_density = 1
            if self.observed_speed > 5.1 and self.observed_speed <= 5.9 :
                observed_power_density = 2
            if self.observed_speed > 5.9 and self.observed_speed <= 6.5 :
                observed_power_density = 3
            if self.observed_speed > 6.5 and self.observed_speed <= 7.0 :
                observed_power_density = 4
            if self.observed_speed > 7.0 and self.observed_speed <= 7.4 :
                observed_power_density = 5
            if self.observed_speed > 7.4 and self.observed_speed <= 8.2 :
                observed_power_density = 6
            # No upper bound....
            if self.observed_speed > 8.2:
                observed_power_density = 7
        if self.observed_height >50:
            if self.observed_speed <= 5.6:
                observed_power_density = 1
            if self.observed_speed > 5.6 and self.observed_speed <= 6.4 :
                observed_power_density = 2
            if self.observed_speed > 6.4 and self.observed_speed <= 7.0 :
                observed_power_density = 3
            if self.observed_speed > 7.0 and self.observed_speed <= 7.5 :
                observed_power_density = 4
            if self.observed_speed > 7.5 and self.observed_speed <= 8.0 :
                observed_power_density = 5
            if self.observed_speed > 8.0 and self.observed_speed <= 8.8 :
                observed_power_density = 6
            # No upper bound....
            if self.observed_speed > 8.8:
                observed_power_density = 7
        return known_power_density,observed_power_density
   
   
    # TODO: log estimate
    
    #def LogEstimateSpeed(self):
    #    
    
