from __future__ import division
import numpy as np
import datetime

class Payment_process:
	
	
	def __init__(self, loaded):
		self.payments = loaded.payments
		self.keyset = loaded.keyset
		self.connections = loaded.payments_list
		
	def sort_payments(self):
		for key, value in self.payments.items():
			self.payments[key].sort(key=lambda x: x.date)
			
	def sort_connections(self, data):
		return sorted(data, key = lambda data:data[0])	#sort by date
			
	def normalize_data(self, data):
		data -= np.mean(data, keepdims = True)
		data = [int(i) for i in data]
		data /= np.std(data, keepdims = True)
		return data
	
	def scale_data(self, data):
		return (data - np.min(data))/np.ptp(data)
	
	def scale_data_from_dict(self, data, divide=None, scale=None):
		min_d = float(np.min([i for i in data.values()]))
		ptp_d = np.ptp(list(data.values()))	# range of values
		for k,v in data.items():
			data_k_fl = float(data[k])
			data[k] = (data_k_fl - min_d)/ptp_d
			if divide:
				data[k] = data_k_fl/divide
			if scale:
				data[k] = data_k_fl*scale
		return data
	
	def process3(self):
		for k, v in self.connections.items():
			if len(v.date_amount) >= 2:
				#data = self.sort_connections(v.date_amount)
				dates = [d[0].day for d in v.date_amount]
				dates_mean = np.mean(dates)
				dates_std = np.std(dates)
				for date, amount in v.date_amount:
					diff = abs(date.day - dates_mean)
					if (diff > 8 or dates_std > 7) or not (7700 < amount < 116000) or not (25 < dates_mean < 35):
						# probably random dates or case for clustering
						# probably not salary
						pass
					else:
						v.salaries.append([date, amount])
			if len(v.salaries) > 0:
				#print(v.salaries)
				v.salaries = np.array(v.salaries)
				#v.salaries[:,1] = self.normalize_connections()		# normalize amounts for p_amount3() Not working now ->also no problem
				#print(v.salaries)
		self.process3_amounts()
		
	def process3_amounts(self):
		for k, v in self.connections.items():
			if len(v.salaries) >= 3:	#must have at least 3 payments to be 'salary'
				err_income = np.std(v.salaries[:,1])/np.mean(v.salaries[:,1])
				if err_income < 1:
					v.salary_perc = (1 - err_income)*100
				else:
					pass	#too big differences in salary, eg. one month comes 'year' of salary according to other months
				
				#for d,am in v.salaries:
				#	print(str(d) + " : " + str(am))
				#print('##')
	
	def process(self):
		counter = 0
		all_err_dates = dict()
		all_err_income = dict()
		all_err = dict()
		for key, p in self.payments.items():
			if len(p) > 4:	# at leat N salaries
				delta_dates = []
				income_list = [p[0].amount,]
				for pay_ind in range(0, len(p) - 1):
					delta = p[pay_ind + 1].date - p[pay_ind].date
					delta_dates.append(delta.days)
					income_list.append(p[pay_ind + 1].amount)
				dates_norm = self.normalize_data(delta_dates)
				err_income = np.std(income_list)/np.mean(income_list)
				err_dates = abs(np.mean(delta_dates) - 30.411)	#avg num off days in month
				if err_dates < 5 and 7700 < np.mean(income_list) < 115000:		# max error of 5 days, otherwise not a salary, salary sum must be reasonable
					all_err_dates[key] = err_dates
					all_err_income[key] = err_income
					all_err[key] = (err_income*10 + err_dates/4)		#weighting of errors
				else:
					#print('not considered income:' + str(np.mean(income_list)) + ' date err:' + str(err_dates))
					pass
		return all_err_dates, all_err_income, all_err
	
	def process_errors(self, all_err_dates, all_err_income, all_err):
		all_err_sc = self.scale_data_from_dict(all_err)
		for k,v in all_err_sc.items():
			#print(1 - v*4)
			#for i in self.payments[k]:
			#	print(i.amount)
			self.connections[k].is_salary = 1 - v
		#print('avg ' + str(np.mean(all_err_income_sc.values())))
		#print('avg dates' + str(np.mean(all_err_dates_sc.values())))
