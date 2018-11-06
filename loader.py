import numpy as np
import datetime
"""
load dataset
"""

class Loader:
	
	class Payment:
		def __init__(self, date, amount):
			self.date = date
			self.amount = amount
			self.is_salary = 0	#percentage
			self.k_means_error = 0
			self.sender_weight = 0
			
	class Connection:
		def __init__(self):
			self.payments = []
			self.is_salary = 0
			self.one_cl_err = 0
			self.two_cl_err = 0
			self.err_rate = 0
			self.cluster_err_perc = 0
			self.cluster_perc = 0
			self.cluster_dst = 0	#for low and heigh cluster center
			self.cluster_dst_perc = 0
			self.date_amount = []
			self.amounts = []
			self.salaries = []		# for payments that we think are salaries
			self.salary_perc = 0	# percentage that sequence is salary according to payment_process.py

		def add_payment(self, paym):
			self.payments.append(paym)
			
	def adjust_sender_weights(self, sender, receiver):
		if sender + receiver not in self.sender_weights_check:
			if sender not in self.sender_weights.keys():
				self.sender_weights[sender] = 1
			else:
				self.sender_weights[sender] += 1
				if self.sender_weights[sender] > self.max_send:
					self.max_send = self.sender_weights[sender]
		else:
			self.sender_weights_check.add(sender + receiver)
			
	def __init__(self, fname):
		#self.raw_data = np.array(['date','to','sum','from'])
		counter = 0
		self.data = []
		self.payments = dict()
		self.payments_list = dict()
		self.keyset = set()
		self.amounts = list()
		self.sender_weights = dict()
		self.sender_weights_check = set()
		
		self.max_send = 0
		
		with open(fname) as f:
			for line in f:
				if counter % 100000 == 0:
					print(counter)
				#if counter > 11900:
				#	break
				counter += 1
				l = list(line.strip().split('\t'))
				timest =  [int(x) for x in l[0].split('-')]	#split datestring on '-'
				l[0] = datetime.datetime(timest[0], timest[1], timest[2])	# needs 3 integers as argument to make datetime object
				l[2] = int(l[2])	#sum as integer
				self.data.append(l)	#tried dataframe, numpy array, simple list seems to be the fastest
				key_payments = l[1] + '#' + l[3]
				
				self.adjust_sender_weights(l[1], l[3])
				
				if key_payments in self.keyset:		#much faster than asking for keys()
					self.payments[key_payments].append(self.Payment(l[0], l[2]))
					
					self.payments_list[key_payments].add_payment(self.Payment(l[0], l[2]))		#with object Connection
				else:
					self.payments[key_payments] = []
					self.payments[key_payments].append(self.Payment(l[0], l[2]))
					
					self.payments_list[key_payments] = self.Connection()
					self.payments_list[key_payments].add_payment(self.Payment(l[0], l[2]))
					
				self.payments_list[key_payments].date_amount.append([l[0], l[2]])
				self.payments_list[key_payments].amounts.append(l[2])	#for graph easy access to amounts
				self.keyset.add(key_payments)
				
				self.amounts.append(l[2])
		
		print(' max send ' + str(self.max_send))
		
#l = Loader('data_for_applicants.txt')
