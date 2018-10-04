from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

class Graph_plotting:
	
	def __init__(self, loaded):
		self.payments = loaded.payments
		self.keyset = loaded.keyset
		self.connections = loaded.payments_list
		
	def monthly_salary_perc(self):
		percentages = []
		sum_salary = []
		for k, v in self.connections.items():
			if len(v.salaries) >= 3:
				percentages.append([v.salary_perc, sum(v.salaries[:,1])])
		percentages = np.array(sorted(percentages, key = lambda percentages:percentages[1]))
		#print percentages
		plt.plot(percentages[:,1],percentages[:,0])
		#plt.show()
		plt.close()
		
	def height_payment_salary_perc(self):
		all_amounts = set()
		percentages = []
		for k, v in self.connections.items():
			for p in v.amounts:
				if p < 160000:
					if p not in all_amounts:
						percentages.append(v.salary_perc)
					all_amounts.add(p)
			#diff_size = len(set(v.amounts) - all_amounts)
			#all_amounts |= set(v.amounts)
			#percentages += [v.salary_perc,]*diff_size
		print(len(all_amounts))
		print(len(percentages))
		all_amounts_sorted = sorted(all_amounts)
		plt.plot(all_amounts_sorted, percentages)
		plt.show()
		plt.close()
		
	def payment_grouped_issalary(self):
		cat_range = 10000
		max_r = 120000
		amounts = range(0, max_r, cat_range)
		amounts_dict = {}
		for am in amounts:
			amounts_dict[am] = 0
		for k, v in self.connections.items():
			for am in v.amounts:
				category = round(am / cat_range)*cat_range
				if category < max_r:
					amounts_dict[category] += 1
		for k,v in amounts_dict.items():
			amounts_dict[k] = (v / 427632)*100	#size of data, TODO: pass from loader file
		plt.title('percentage from all payments vs. sum of payment, grouped by 10000')
		plt.xlabel('sum of transaction')
		plt.ylabel('percentage')
		plt.plot(list(amounts_dict.keys()), list(amounts_dict.values()), 'o')
		plt.show()
		plt.close()
		
	def grouped_payment_perc_issalary(self):
		cat_range = 10000
		max_r = 120000
		percentage = {}
		perc2 = dict()
		for k, v in self.connections.items():
			if len(v.salaries) > 0:
				num_of_salaries = len(v.salaries[:,1])
				for salary in v.salaries[:,1]:
					category = round(salary / cat_range)*cat_range
					if category not in percentage.keys():
						percentage[category] = 0
						perc2[category] = 0
					if category < max_r:
						percentage[category] += v.salary_perc
						perc2[category] +=1
		for cat in range(10000, max_r, cat_range):
			if perc2[category] != 0:
				percentage[cat] = percentage[cat] / perc2[cat]
		to_plot = np.array(sorted(list(percentage.items())))
		plt.title('probability of being salary vs. sum of payment')
		plt.xlabel('percentage')
		plt.ylabel('payment')
		plt.plot(to_plot[:,0], to_plot[:,1])
		plt.show()
		plt.close()
		
			
			
			