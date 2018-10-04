from __future__ import division

import numpy as np
from sklearn import cluster


class Clustering:
	
	def __init__(self, loaded):
		self.connections = loaded.payments_list
		self.payments = loaded.payments
		self.payments_origin = loaded.payments
		self.keyset = loaded.keyset
		self.amounts = np.array(loaded.amounts).reshape(-1,1)	# needs 2D for kmeans, but have only 1 feature
		self.mean = np.mean(loaded.amounts)
		self.std_paym = np.std(loaded.amounts)
		
	def scale_data(self, data):
		data -= self.mean
		data /= self.std_paym
		return data
		
	def normalize_payments(self):
		for k, v in self.payments.items():
			for p in v:
				p.amount = self.scale_data(p.amount)
				
	def my_kmeans(self, amount, iterate= 10):
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
	
	def k_means_error(self, amount, l_center, h_center, one_center):
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
		
	def do_clustering(self):
		counter = 0
		err_rate_max = 0
		dst_max = 0
		for k, v in self.payments.items():
			amount = list()	#list of payment's height
			counter += 1
			if counter % 10000 == 0:
				print(counter)
			if len(v) > 2:
				#print(k)
				for p in v:
					amount.append(p.amount)
				l_cluster, h_cluster, one_cluster = self.my_kmeans(amount)
				self.connections[k].two_cl_err, self.connections[k].one_cl_err = self.k_means_error(amount, l_cluster, h_cluster, one_cluster)
				err_r = self.connections[k].one_cl_err / self.connections[k].two_cl_err
				
				# c dst part
				c_dst = abs(l_cluster - h_cluster)
				if c_dst > dst_max:
					dst_max = c_dst
					print('dst max ' +str(dst_max))
				self.connections[k].cluster_dst = c_dst
				# end c dst part
				
				if self.connections[k].two_cl_err < self.connections[k].one_cl_err:
					if err_r > err_rate_max:
						err_rate_max = err_r
					self.connections[k].err_rate = err_r		# decisively one cluster, thus minimal value would be added to' err_rate_loc'
		
		print('err r max '  + str(err_rate_max))
		dst_max *=0.8		#eliminate weight of outliers
		err_rate_max *= 0.8
		for k, v in self.connections.items():
			if self.connections[k].two_cl_err < self.connections[k].one_cl_err:
				self.connections[k].cluster_dst_perc = (self.connections[k].cluster_dst / dst_max) * 100
				self.connections[k].cluster_err_perc = (self.connections[k].err_rate / err_rate_max) * 100
				self.connections[k].cluster_perc = (self.connections[k].cluster_dst_perc + self.connections[k].cluster_err_perc)/2
				if self.connections[k].cluster_perc > 50:
					print(self.connections[k].cluster_perc)
					for p in self.payments[k]:
						print(p.amount)
					print('#')
		
		