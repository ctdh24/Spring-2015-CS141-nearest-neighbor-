import sys
import os
import random
import fileinput
import math
import time
from collections import namedtuple

#global variables
pair = namedtuple('pair', ['x_point','y_point'])
array_points = []


#------------------------------------------------
#define helper funtions
def distance_solver(pair1, pair2):
  ret_val = 0.0
  x = pow(pair1[0] - pair2[0],2)
  y = pow(pair1[1] - pair2[1],2)
  ret_val = math.sqrt(x+y)
  return ret_val
#------------------------------------------------
def brute_force(array_of_points, output_file):
  if (len(array_of_points) < 2): return 100000
  dist_small = distance_solver(array_points[0], array_points[1])
  closest_index = pair(0,1)
  for array_it in range(0,len(array_of_points)-1):
      for array_it2 in range(array_it+1,len(array_of_points)-1):
        temp_dist = distance_solver(array_of_points[array_it], array_of_points[array_it2])
        if temp_dist < dist_small:
          dist_small = temp_dist
          closest_index = pair(array_it,array_it2)
  return distance_solver(array_of_points[closest_index[0]], array_of_points[closest_index[1]])


def div_conquer(array_of_points, output_file):
  if len(array_of_points) <= 3: 
    return brute_force(array_of_points, output_file);
  mid = len(array_of_points)/2
  array_of_pointsL = array_of_points[:mid]
  array_of_pointsR = array_of_points[mid:]
  DR = div_conquer(array_of_pointsR, output_file)
  DL = div_conquer(array_of_pointsL, output_file)
  small_dist = min(DL, DR)
  #index_l = 0
  x_val_left = array_of_points[mid][0] - DL
  x_val_right = array_of_points[mid][0] + DR
  while(array_of_points[0][0] < x_val_left):
     array_of_points.remove(array_of_points[0])
  x_right = len(array_of_points) - 1
  while(array_of_points[-1][0] > x_val_right):
     array_of_points.remove(array_of_points[-1])
  array_of_points_block = array_of_points
  sorted(array_of_points_block, key = lambda pair: pair[1])
  small_dist_block = brute_force(array_of_points_block, output_file)
  if small_dist < small_dist_block: 
    return small_dist
  else: return small_dist_block
  
#------------------------------------------------
#read in filename
filename = sys.argv[-1]

#create output file name for use later
outputfile = filename[0:-4] + "_distance.txt"
#os.remove(outputfile)
#open the file and read in inputs.
for line in open(filename):
  fileline = line
  xp = float(fileline.split(' ')[0])
  yp = float(fileline.split(' ')[1])
  array_points.append(pair(x_point = xp, y_point = yp))

#--------timing of the brute force method - testing purposes only--------
# array_points = sorted(array_points, key=lambda pair: pair[0])   # sort
# start_time = time.time()
# a = brute_force(array_points, outputfile)
# end_time = time.time()
# total_time = end_time - start_time
# print "total time brute force = "+ str(total_time)

start_time = time.time()
b = div_conquer(array_points, outputfile)
end_time = time.time()
total_time = end_time - start_time
print "total time divide and conquer = "+ str(total_time)

print str(b)

f = open(outputfile,'w')
f.write(str(b))
f.close()
