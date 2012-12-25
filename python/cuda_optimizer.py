import pycuda.autoinit
import pycuda.driver as cuda
from math import *
from numpy import *
import os,sys

def Optimize_Blocks():
    # Get memory info
    print "Memory info:"
    (free,total)=cuda.mem_get_info()
    print round(100.0*free/total,2),"% free of",round(total*1.0/pow(1024,3),4),"Gb"
    # Find the largest numpy array
    mem_list = [1.0]
    np_array_size  = 1
    opts = 0
    counter = 0
    while opts < free:
        opts = free*1.0/sys.getsizeof(mem_list)*counter
        counter += 1
        print free,opts,sys.getsizeof(mem_list)*counter
    print "Max list size:",counter
    #while np_array_size < free:
    #    mem_list = mem_list.append(1.0)
    #    np_array_size = sys.getsizeof(mem_list)
    #np = array(np)
    print "Max Numpy array size:",sys.getsizeof(np)
    # Create lists to store multiple device info
    threads_per_block = []
    grid_dim_x = []
    
    # Loop through devices
    for devicenum in range(cuda.Device.count()):
        # Initialize the device
        device=cuda.Device(devicenum)
        
        # Get dictionary of device info
        attrs=device.get_attributes()
        
        # Get max threads per block info
        tpb = attrs[pycuda._driver.device_attribute.MAX_THREADS_PER_BLOCK]
        if tpb not in threads_per_block:
            threads_per_block.append(tpb)
        
        # Get max grid dimension
        mgd = attrs[pycuda._driver.device_attribute.MAX_GRID_DIM_X]
        if mgd not in grid_dim_x:
            grid_dim_x.append(mgd)
    
    
    print "You should use the following code in your Python code:"
    print "block_size =", str(min(threads_per_block))
    print "blocks =", str(min(grid_dim_x)/min(threads_per_block))
