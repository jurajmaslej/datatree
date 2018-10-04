from __future__ import division
import numpy as np

def my_kmeans( amount, iterate= 10):
	l_mean = np.mean(amount)
	l_max = np.max(amount)
	l_min = np.min(amount)
	high_center = l_mean + (l_max - l_mean)/2
	low_center = l_mean - (l_mean - l_min)/2
	one_center = l_mean 	#do we have one cluster?
	#print('low center ' + str(low_center))
	#print('high center ' + str(high_center))
	diff_high = 0		# how much should center be moved
	diff_low = 0
	for j in range(0,iterate):
		diff_high = 0
		diff_low = 0
		diff_one = 0
		for i in amount:
			low = abs(i - low_center)
			high =  abs(i - high_center)
			one = abs(i - one_center)
			#print ('i: ' + str(i))
			if low > high:
				diff_high += i - high_center # important if positive or negative
			else:
				diff_low += i - low_center
			diff_one += i - one_center
		low_center += diff_low/len(amount)*0.5
		high_center += diff_high/len(amount)*0.5
		one_center += diff_one/len(amount)*0.5 
	#print('low ' + str(low_center))
	#print('high ' + str(high_center))
	return (low_center, high_center, one_center)

def k_means_error( amount, l_center, h_center, one_center):
	error = 0
	one_error = 0
	for p in amount:
		dist_from_low = abs(l_center - p)
		dist_from_high = abs(h_center- p)
		dist_from_one = abs(one_center - p)
		if dist_from_high < dist_from_low:
			error += dist_from_high
		else:
			error += dist_from_low
		one_error += dist_from_one 
	return (error, one_error)

amount = [1,2,3,10,12,14]
amount = range(10)
amount = [0.184000418461,
0.190720315585,
0.178037432827,
0.185366551393,
0.18440656609,
0.185495780184
]
l_cluster, h_cluster, one_cluster = my_kmeans(amount)
print('clusters: low, high, one')
print(l_cluster)
print(h_cluster)
print(one_cluster)
two_cl_err, one_cl_err = k_means_error(amount, l_cluster, h_cluster, one_cluster)
print('two cl ' + str(two_cl_err))
print('one cl ' + str(one_cl_err))
#my_kmeans([1,2,3,10,12,14], iterate = 10)
#my_kmeans([1,2,3,10,12,14], iterate = 20)