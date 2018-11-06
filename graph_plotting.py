from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

class Graph_plotting:
	
	def __init__(self, loaded):
		self.payments = loaded.payments
		self.keyset = loaded.keyset
		self.connections = loaded.payments_list		# payments list contains Connections
		self.weights = loaded.sender_weights
		
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
		
	def sender_weights_histogram(self):
		histo_weights = dict()
		colors = {0: "red", 1: "black", 2: "blue", 3:"green"}
		paint = []
		for k, v in self.connections.items():
			for payment in v.payments:
				key_for_weights = k[:k.find('#')]
				if self.weights[key_for_weights] not in histo_weights.keys():
					histo_weights[self.weights[key_for_weights]] = 1
				else:
					histo_weights[self.weights[key_for_weights]] += 1
		print('histo histo_weights')
		
		x = []
		y = []
		weights_np = np.array(list(histo_weights.keys())).reshape(-1,1)
		#print(weights_np)
		kmeans = KMeans(n_clusters=4, random_state=0).fit(weights_np)
		for k,v in histo_weights.items():
			x.append(k)
			cluster = int(kmeans.predict(k))
			paint.append(colors[cluster])
			y.append(v)
			
		plt.xticks([i for i in range(0 ,max(x), 100)])
		plt.yticks([i for i in range(0,max(y), 5000)])
		plt.xlabel('number of transactions from account')
		plt.ylabel('num of accounts with given num of transactions')
		plt.scatter(x,y, c = paint)
		plt.show()
		#plt.savefig('account_weights.png')
